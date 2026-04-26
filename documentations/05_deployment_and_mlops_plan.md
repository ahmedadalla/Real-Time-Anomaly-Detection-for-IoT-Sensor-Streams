# 05 - Deployment and MLOps Plan

This section converts current offline work into a production-ready roadmap.

## Target Runtime Architecture
1. Streaming ingestion
- Azure Event Hubs (or Kafka) receives sensor events
- Raw events land in Blob/Data Lake for replay and audit

2. Online feature service
- Apply same scaler and feature order as training
- Build rolling windows (`window_size=12`) for inference

3. Model inference service
- Containerized PyTorch service (USAD and/or LSTM)
- REST endpoint for single/batch windows
- Return score + anomaly flag + threshold metadata

4. Alerting
- Azure Monitor / Logic Apps rules on anomaly events
- Severity routing by confidence and affected subsystem

5. Monitoring dashboard
- Power BI or Grafana for live anomaly rate, precision proxy, and drift indicators

## MLOps Controls
- Experiment tracking: MLflow
- Versioning: dataset hash, feature schema, scaler, model, threshold
- CI/CD: unit tests + model validation gates before deployment
- Drift monitoring: feature distribution drift + score drift
- Retraining trigger: scheduled and drift-based

## Immediate Action Backlog
- Build `src/` package from notebook logic (reusable preprocessing + inference)
- Add model-serving API (`FastAPI`)
- Add Dockerfile and deployment manifests
- Add online/offline parity tests for preprocessing
- Add synthetic load test for latency and throughput
