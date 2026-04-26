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

## Comparative Observations
- Both models successfully separate normal and attack windows in offline evaluation.
- USAD shows very strong ranking quality (high ROC-AUC) in current test setup.
- LSTM autoencoder also provides high overall accuracy with a simple reconstruction pipeline.

## Gaps and Next Improvements
- Add Isolation Forest baseline for milestone completeness.
- Add cross-run variance analysis (seeds/folds).
- Produce a unified comparison table: precision, recall, F1, ROC-AUC, latency, memory.
- Calibrate threshold strategy for deployment (cost-sensitive alerting).
