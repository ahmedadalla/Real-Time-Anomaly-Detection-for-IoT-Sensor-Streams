# Real-Time Anomaly Detection for IoT Sensor Streams

## Documentation Scope
This document aligns project documentation with the milestone-based requirements from `Docs/Project Idea.pdf`, using implemented work found in this repository.

## Project Idea Summary
Build a real-time anomaly detection system for IoT sensor streams that can:
- Detect anomalies online
- Scale in production
- Trigger alerts and dashboard updates

## Problem and Objective
From `Docs/problem_formula.pdf` and `Docs/Problem Formulation.docx`:
- Problem: detect cyber-attacks and anomalies from multivariate industrial sensor data under real-time constraints.
- Objective: maximize recall while preserving precision and operational availability.

## What Has Been Implemented

### Data and EDA
- Data loading and cleaning notebook: `notebooks/Data_loading_cleaning.ipynb`
- EDA notebook: `notebooks/EDA.ipynb`
- Processed raw data available under `Data/raw_data/`

### Preprocessing and Feature Engineering
- Notebook: `notebooks/preprocessing_feature_engineering.ipynb`
- Exported arrays and metadata under `Data/swat_preprocessed/`
- Current config:
  - train_ratio=0.9, val_ratio=0.05, test_ratio=0.05
  - window_size=12, step_size=1
  - smoothing=false, stabilization_hours=1

### Modeling
- LSTM autoencoder notebook: `notebooks/LSTM.ipynb`
- USAD notebook: `notebooks/USAD.ipynb`
- Saved model files under `Data/models/`

### Results Snapshot
- LSTM notebook reports test accuracy around 0.97
- USAD notebook reports:
  - threshold from validation: about 0.0014934739
  - test accuracy around 0.96
  - ROC-AUC around 0.9994

## Milestone Status

### Milestone 1 (Data + Preprocessing + EDA)
Status: mostly completed in offline form.

### Milestone 2 (Modeling + Evaluation)
Status: completed for LSTM and USAD workflows.
Gap: Isolation Forest baseline and standardized hyperparameter search are pending.

### Milestone 3 (Cloud Deployment + Integration)
Status: not yet implemented in this repository.

### Milestone 4 (MLOps + Dashboard)
Status: planning stage, partial EDA visuals available.

### Milestone 5 (Final Documentation + Presentation)
Status: this documentation package is prepared; final live demo script remains to be finalized.

## Proposed Next Phase
1. Refactor notebooks into production modules.
2. Expose inference as FastAPI service.
3. Containerize and deploy with cloud stream input.
4. Add experiment tracking and drift monitoring.
5. Build live dashboard and alerting workflows.
