# Real-Time Anomaly Detection for IoT Sensor Streams

Real-time anomaly and cyber-attack detection for industrial water treatment systems using multivariate time-series sensor data.

## Overview

This project targets cyber-physical security in modern water treatment facilities. The repository includes:
- Data collection/cleaning notebooks
- Preprocessing and feature engineering pipeline
- Two anomaly detection models (LSTM Autoencoder and USAD)
- Saved datasets and model artifacts
- Lightweight FastAPI backend for live-style anomaly detection
- Simple browser dashboard and sensor simulator

Primary objective:
- Detect attacks with high recall while preserving practical precision and low-latency feasibility.

## Repository Structure

- `notebooks/`
	- `Data_loading_cleaning.ipynb`
	- `EDA.ipynb`
	- `preprocessing_feature_engineering.ipynb`
	- `LSTM.ipynb`
	- `USAD.ipynb`
- `Data/raw_data/`
	- `merged_data.csv`, `normal_data.csv`, `attack_data.csv`
- `Data/swat_preprocessed/`
	- `X_train.npy`, `X_val.npy`, `X_test.npy`, `y_test.npy`
	- `config.json`, `feature_columns.json`, `scaler.pkl`
- `Data/models/`
	- `lstm_autoencoder.pth`
	- `usad_swat_weights.pth`
	- `usad_swat_model_full.pth`
- `src/anomaly_detection/`
	- FastAPI backend, preprocessing, model loading, inference, CSV storage, and simulator
- `documentations/`
	- Milestone-based project documentation package

## Setup

1. Create and activate a Python environment. Python 3.10+ is recommended.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Live Backend

The live backend uses the saved USAD model artifacts. It does not retrain the model.

Start the API:

```bash
python -m uvicorn src.anomaly_detection.api:app --host 127.0.0.1 --port 8000
```

Open the dashboard:

- `http://127.0.0.1:8000/`

Useful API URLs:

- `GET /health` - service status, model name, window size, and feature counts
- `POST /sensor` - send one sensor reading; prediction starts automatically once the rolling window reaches 12 readings
- `POST /predict` - send a complete 12-reading window for direct prediction
- `GET /results` - recent prediction results

Example health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected model in the response:

```json
{
  "status": "ok",
  "model": "USAD",
  "threshold": 0.0014934739,
  "window_size": 12
}
```

## Run the Sensor Simulator

In a second terminal, keep the API running and start the simulator:

```bash
python -m src.anomaly_detection.simulator --api-url http://127.0.0.1:8000 --interval 1 --anomaly-every 25
```

The simulator sends realistic SWaT-style sensor readings to `POST /sensor`.
By default, it replays rows from `Data/raw_data/normal_data.csv` after the configured 1-hour stabilization period. This keeps normal windows close to the distribution used during preprocessing.
Every `--anomaly-every` readings, it injects abnormal values.

Optional simulator flags:

- `--skip-rows 3600` - choose how many CSV rows to skip before replay starts
- `--random` - use synthetic random readings instead of CSV replay

Refresh the dashboard to see recent prediction results.

## Runtime Output

The backend stores live-demo data as CSV files:

- `Data/runtime/sensor_readings.csv`
- `Data/runtime/prediction_results.csv`

`Data/runtime/` is ignored by git because these files are generated while running the app.

## Recommended Notebook Execution Order

1. `notebooks/Data_loading_cleaning.ipynb`
2. `notebooks/EDA.ipynb`
3. `notebooks/preprocessing_feature_engineering.ipynb`
4. `notebooks/LSTM.ipynb`
5. `notebooks/USAD.ipynb`

This order matches the data and artifact dependencies between notebooks.

## Data and Preprocessing Notes

Preprocessing outputs include:
- Window size: `12`
- Split ratios: train `0.90`, val `0.05`, test `0.05`
- Feature set saved in `Data/swat_preprocessed/feature_columns.json`

Generated tensor shapes reported by preprocessing notebook:
- `X_train: (1245136, 12, 47)`
- `X_val: (69163, 12, 47)`
- `X_test: (120184, 12, 47)`
- `y_test: (120184,)`

## Models

### LSTM Autoencoder
- Notebook: `notebooks/LSTM.ipynb`
- Trained on normal windows with reconstruction loss
- Uses validation reconstruction error percentile for thresholding

### USAD
- Notebook: `notebooks/USAD.ipynb`
- Encoder + dual-decoder architecture
- Threshold computed from validation score distribution
- Current backend model for live inference
- Runtime threshold: `0.0014934739`

## Backend Notes

The API preserves the saved preprocessing behavior:

- Feature order is loaded from `Data/swat_preprocessed/feature_columns.json`
- Window size is loaded from `Data/swat_preprocessed/config.json`
- The trained scaler is loaded from `Data/swat_preprocessed/scaler.pkl`
- USAD weights are loaded from `Data/models/usad_swat_weights.pth`

Incoming API payloads only need the 46 real sensor features. The saved scaler/model were trained with 47 values per timestep, including `label`, so the backend adds `label=0` internally during preprocessing to match the saved artifacts.

## Reported Evaluation Snapshot

From notebook outputs currently stored in this repository:
- LSTM notebook reports test accuracy around `0.97`
- USAD notebook reports:
	- threshold around `0.0014934739`
	- test accuracy around `0.96`
	- ROC-AUC around `0.9994`

## Documentation

A full milestone-aligned documentation package is available in:
- `documentations/project_documentation.md`
- `documentations/README.md`

## Current Scope vs. Next Phase

Implemented now:
- Offline data processing, model training, and evaluation
- FastAPI backend for USAD inference
- Rolling-window sensor ingestion
- CSV logging for readings and prediction results
- Lightweight browser dashboard
- Sensor simulator

Planned next:
- Alerting and monitoring dashboard
- MLOps automation (tracking, drift detection, retraining)
- Containerization and cloud deployment
