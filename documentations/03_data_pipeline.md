# 03 - Data Pipeline

## Data Sources and Labels
The preprocessing flow assumes SWaT process data with normal/attack labels.

Generated raw datasets:
- `Data/raw_data/merged_data.csv`
- `Data/raw_data/normal_data.csv`
- `Data/raw_data/attack_data.csv`

Original label mapping used in cleaning:
- Normal -> 0
- Attack -> 1

## Preprocessing Workflow
Implemented in `notebooks/preprocessing_feature_engineering.ipynb`.

Main steps:
1. Load normal and attack datasets
2. Drop common constant columns
3. Normalize timestamp/index consistency and fill gaps
4. Optional smoothing (`smoothing` flag in config)
5. Split normal data into train/val/test partitions
6. Build test set by combining normal_test with attack data
7. Fit scaler on train only, then transform val/test
8. Create sliding windows and window-level labels
9. Persist arrays and metadata

## Current Configuration
From `Data/swat_preprocessed/config.json`:
- train_ratio: 0.9
- val_ratio: 0.05
- test_ratio: 0.05
- window_size: 12
- step_size: 1
- smoothing: false
- smoothing_window: 5
- stabilization_hours: 1

## Generated Tensor Shapes
Reported by preprocessing notebook output:
- X_train: (1245136, 12, 47)
- X_val: (69163, 12, 47)
- X_test: (120184, 12, 47)
- y_test: (120184,)
- Test anomaly ratio: 0.4245157425

## Feature Set
Feature names are saved in `Data/swat_preprocessed/feature_columns.json` (46 sensor features).

## Pipeline Outputs
- Arrays: `X_train.npy`, `X_val.npy`, `X_test.npy`, `y_test.npy`
- Metadata: `config.json`, `feature_columns.json`
- Scaler artifact: `scaler.pkl`

## Notes for Production
To align with real-time use:
- Replace offline CSV reads with streaming windows
- Validate schema and units per sensor source
- Keep scaler and feature order versioned with model versions
