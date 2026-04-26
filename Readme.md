# Real-Time Anomaly Detection for IoT Sensor Streams

Real-time anomaly and cyber-attack detection for industrial water treatment systems using multivariate time-series sensor data.

## Overview

This project targets cyber-physical security in modern water treatment facilities. The repository includes:
- Data collection/cleaning notebooks
- Preprocessing and feature engineering pipeline
- Two anomaly detection models (LSTM Autoencoder and USAD)
- Saved datasets and model artifacts

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
- `documentations/`
	- Milestone-based project documentation package

## Setup

1. Create and activate a Python environment (recommended Python 3.10+).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

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

Planned next:
- Streaming ingestion
- Deployment API for online inference
- Alerting and monitoring dashboard
- MLOps automation (tracking, drift detection, retraining)