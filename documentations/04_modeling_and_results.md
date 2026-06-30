# 04 - Modeling and Results

## Implemented Models

### 1) LSTM Autoencoder
Notebook: `notebooks/LSTM.ipynb`

Pipeline summary:
- Load preprocessed windows (`X_train`, `X_val`, `X_test`, `y_test`)
- Build LSTM autoencoder in PyTorch
- Train with reconstruction loss (MSE)
- Compute reconstruction errors on val/test
- Set threshold from validation distribution (97th percentile)
- Predict anomaly if error > threshold
- Report classification metrics and confusion matrix

Saved artifact:
- `Data/models/lstm_autoencoder.pth`

Reported notebook metrics snapshot:
- Accuracy: ~0.97 on test windows

### 2) USAD (UnSupervised Anomaly Detection)
Notebook: `notebooks/USAD.ipynb`

Pipeline summary:
- Load preprocessed arrays and flatten windows
- Build encoder + dual decoder architecture in PyTorch
- Train with USAD objective across epochs
- Compute validation anomaly scores
- Set threshold from validation scores (95th percentile)
- Evaluate on test data using classification report and ROC-AUC

Saved artifacts:
- `Data/models/usad_swat_weights.pth`
- `Data/models/usad_swat_model_full.pth`

Reported notebook metrics snapshot:
- Validation-derived threshold: ~0.0014934739
- Accuracy: ~0.96 on test windows
- ROC-AUC: ~0.9994

### 3) Isolation Forest
Notebook: `notebooks/Isolation_Forest.ipynb`

Pipeline summary:
- Load preprocessed SWAT tensors and flatten the windowed features
- Sweep contamination values to tune the Isolation Forest baseline
- Select the best contamination value using the validation/test classification metrics
- Report confusion matrix and classification report for the tuned run

Saved artifacts:
- `Data/models/isolation_forest_model.joblib`
- `Data/models/isolation_forest_tuned.joblib`

Reported notebook metrics snapshot:
- Best contamination: 0.01
- Accuracy: 0.8137 on test windows
- Precision: 0.8365
- Recall: 0.6974
- F1-score: 0.7606

## Comparative Observations
- The models successfully separate normal and attack windows in offline evaluation.
- USAD shows very strong ranking quality (high ROC-AUC) in current test setup.
- LSTM autoencoder also provides high overall accuracy with a simple reconstruction pipeline.
- Isolation Forest now provides a documented classical baseline with a tuned contamination sweep and lower but interpretable test performance.

## Standardized Benchmark Table

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| LSTM Autoencoder | ~0.97 | Not reported in the current summary | Not reported in the current summary | Not reported in the current summary | Not reported in the current summary | Threshold set from the validation reconstruction-error distribution |
| USAD | ~0.96 | Not reported in the current summary | Not reported in the current summary | Not reported in the current summary | ~0.9994 | Strong ranking quality on the current test setup |
| Isolation Forest | 0.8137 | 0.8365 | 0.6974 | 0.7606 | Not reported in the current summary | Best contamination = 0.01 |

## Gaps and Next Improvements
- Add cross-run variance analysis (seeds/folds).
- Extend the standardized benchmark table with latency and memory.
- Calibrate threshold strategy for deployment (cost-sensitive alerting).
