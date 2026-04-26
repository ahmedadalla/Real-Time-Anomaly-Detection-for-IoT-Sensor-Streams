# 02 - Work Completed by Milestone

This status is mapped to the milestone brief in `Docs/Project Idea.pdf`.

## Milestone 1 - Data Collection, Preprocessing, and Exploration
### Required
- Ingest and store IoT streams
- Preprocess time series (windowing, smoothing, feature extraction)
- EDA and anomaly pattern analysis

### Completed in Repository
- Dataset acquisition and cleaning workflow exists in `notebooks/Data_loading_cleaning.ipynb`
- Cleaned outputs generated:
  - `Data/raw_data/merged_data.csv`
  - `Data/raw_data/normal_data.csv`
  - `Data/raw_data/attack_data.csv`
- Feature engineering and preprocessing workflow exists in `notebooks/preprocessing_feature_engineering.ipynb`
- Exported preprocessed assets exist in `Data/swat_preprocessed/`
  - `X_train.npy`, `X_val.npy`, `X_test.npy`, `y_test.npy`
  - `config.json`, `feature_columns.json`, `scaler.pkl`
- EDA notebook and report asset exist:
  - `notebooks/EDA.ipynb`
  - `Docs/EDA.pdf`

### Pending
- Production-grade streaming ingestion (Event Hubs/Kafka)
- Cloud data lake architecture and operational data contracts

## Milestone 2 - Model Development and Evaluation
### Required
- Evaluate anomaly models (Autoencoder, Isolation Forest, LSTM-based)
- Evaluate precision/recall and real-time simulation
- Hyperparameter optimization

### Completed in Repository
- LSTM autoencoder workflow in `notebooks/LSTM.ipynb`
- USAD workflow in `notebooks/USAD.ipynb`
- Model artifacts exported in `Data/models/`
  - `lstm_autoencoder.pth`
  - `usad_swat_weights.pth`
  - `usad_swat_model_full.pth`
- Metrics are reported in notebook outputs (classification report, confusion matrix, ROC-AUC)

### Pending
- Isolation Forest baseline in current repository
- Structured hyperparameter search tracking
- Standardized benchmark table across all candidate models

## Milestone 3 - Cloud Deployment and Integration
### Completed
- Not yet implemented in this repository

### Planned
- Streaming inference service
- REST endpoint for sensor events
- Alerting integration

## Milestone 4 - MLOps and Monitoring Dashboard
### Completed
- Partial EDA visualization assets

### Planned
- MLflow or equivalent experiment tracking
- Drift-aware retraining triggers
- Live operational dashboard

## Milestone 5 - Final Documentation and Presentation
### Completed
- This `documentations/` package and updated project README

### Pending
- Final end-to-end live demo execution script
- Future enhancements roadmap with effort estimates
