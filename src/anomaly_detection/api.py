from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from .config import load_runtime_config
from .inference import predict_window
from .model_loader import load_model, load_scaler
from .preprocessing import extract_timestamp, normalize_reading
from .storage import CSVStore
from .window_buffer import WindowBuffer


runtime_config = load_runtime_config()
scaler = load_scaler()
model = load_model()
window_buffer = WindowBuffer(runtime_config.window_size)
store = CSVStore()

app = FastAPI(
    title="IoT Sensor Anomaly Detection API",
    version="0.1.0",
    description="Lightweight API for live SWaT-style IoT anomaly detection.",
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _coerce_reading(payload: dict[str, Any]) -> tuple[str, dict[str, float]]:
    timestamp = extract_timestamp(payload) or _now()
    try:
        reading = normalize_reading(payload, runtime_config.feature_columns)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return timestamp, reading


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>IoT Anomaly Dashboard</title>
        <style>
          :root { color-scheme: dark; font-family: Arial, sans-serif; }
          body { margin: 0; background: #101418; color: #f3f7fb; }
          main { max-width: 1100px; margin: 0 auto; padding: 28px; }
          h1 { margin: 0 0 6px; font-size: 28px; }
          .subtle { color: #9fb0c0; margin-bottom: 24px; }
          .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
          .panel { background: #18212a; border: 1px solid #2b3a46; border-radius: 8px; padding: 16px; }
          .label { color: #9fb0c0; font-size: 12px; text-transform: uppercase; }
          .value { font-size: 24px; margin-top: 8px; font-weight: 700; }
          table { width: 100%; border-collapse: collapse; margin-top: 18px; }
          th, td { text-align: left; border-bottom: 1px solid #2b3a46; padding: 10px 8px; }
          th { color: #9fb0c0; font-weight: 600; }
          .alert { color: #ff8f70; font-weight: 700; }
          .normal { color: #71e0a3; font-weight: 700; }
          @media (max-width: 800px) { .grid { grid-template-columns: 1fr 1fr; } }
        </style>
      </head>
      <body>
        <main>
          <h1>IoT Anomaly Dashboard</h1>
          <div class="subtle">Live backend status and recent USAD predictions</div>
          <section class="grid">
            <div class="panel"><div class="label">Service</div><div class="value" id="status">...</div></div>
            <div class="panel"><div class="label">Model</div><div class="value" id="model">...</div></div>
            <div class="panel"><div class="label">Window</div><div class="value" id="window">...</div></div>
            <div class="panel"><div class="label">Buffered</div><div class="value" id="buffered">...</div></div>
          </section>
          <section class="panel" style="margin-top: 16px;">
            <div class="label">Recent Predictions</div>
            <table>
              <thead><tr><th>Timestamp</th><th>Score</th><th>Label</th><th>Model</th></tr></thead>
              <tbody id="results"><tr><td colspan="4">Waiting for predictions...</td></tr></tbody>
            </table>
          </section>
        </main>
        <script>
          async function refresh() {
            const health = await fetch('/health').then(r => r.json());
            document.getElementById('status').textContent = health.status;
            document.getElementById('model').textContent = health.model;
            document.getElementById('window').textContent = health.window_size;
            document.getElementById('buffered').textContent = health.buffered_readings;

            const data = await fetch('/results?limit=20').then(r => r.json());
            const rows = data.results || [];
            document.getElementById('results').innerHTML = rows.length ? rows.map(item => {
              const label = Number(item.anomaly_label) === 1 ? 'Anomaly' : 'Normal';
              const cls = Number(item.anomaly_label) === 1 ? 'alert' : 'normal';
              return `<tr><td>${item.timestamp}</td><td>${Number(item.anomaly_score).toFixed(6)}</td><td class="${cls}">${label}</td><td>${item.model_name}</td></tr>`;
            }).join('') : '<tr><td colspan="4">Waiting for predictions...</td></tr>';
          }
          refresh();
          setInterval(refresh, 3000);
        </script>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "model": getattr(model, "name", type(model).__name__),
        "threshold": getattr(model, "threshold", None),
        "window_size": runtime_config.window_size,
        "sensor_feature_count": len(runtime_config.feature_columns),
        "model_input_features_per_step": getattr(scaler, "n_features_in_", len(runtime_config.feature_columns)),
        "buffered_readings": window_buffer.count,
    }


@app.post("/sensor")
def receive_sensor_reading(payload: dict[str, Any]) -> dict[str, object]:
    timestamp, reading = _coerce_reading(payload)
    store.save_reading(timestamp, reading)

    prediction: dict[str, object] | None = None
    if window_buffer.append(reading):
        result = predict_window(
            window_buffer.current_window(),
            runtime_config.feature_columns,
            scaler,
            model,
            timestamp=timestamp,
        )
        prediction = store.save_prediction(result)

    return {
        "accepted": True,
        "timestamp": timestamp,
        "buffered_readings": window_buffer.count,
        "window_ready": window_buffer.ready,
        "prediction": prediction,
    }


@app.post("/predict")
def predict_complete_window(payload: Any) -> dict[str, object]:
    window_payload = payload.get("window") if isinstance(payload, dict) else payload
    if not isinstance(window_payload, list):
        raise HTTPException(status_code=422, detail="Request body must be a window list or {'window': [...]}")
    if len(window_payload) != runtime_config.window_size:
        raise HTTPException(
            status_code=422,
            detail=f"Window must contain exactly {runtime_config.window_size} readings",
        )

    normalized_window: list[dict[str, float]] = []
    timestamp = None
    for item in window_payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=422, detail="Each window item must be an object")
        timestamp, reading = _coerce_reading(item)
        normalized_window.append(reading)

    result = predict_window(
        normalized_window,
        runtime_config.feature_columns,
        scaler,
        model,
        timestamp=timestamp,
    )
    prediction = store.save_prediction(result)
    return {"prediction": prediction}


@app.get("/results")
def recent_results(limit: int = Query(default=20, ge=1, le=50)) -> dict[str, object]:
    return {"results": store.recent_predictions(limit=limit)}
