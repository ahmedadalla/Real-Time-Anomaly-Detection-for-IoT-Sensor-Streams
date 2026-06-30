from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "Data"
PREPROCESSED_DIR = DATA_DIR / "swat_preprocessed"
MODELS_DIR = DATA_DIR / "models"
RUNTIME_DIR = DATA_DIR / "runtime"
RAW_DATA_DIR = DATA_DIR / "raw_data"

CONFIG_PATH = PREPROCESSED_DIR / "config.json"
FEATURE_COLUMNS_PATH = PREPROCESSED_DIR / "feature_columns.json"
SCALER_PATH = PREPROCESSED_DIR / "scaler.pkl"
DEFAULT_MODEL_PATH = MODELS_DIR / "isolation_forest_tuned.joblib"
USAD_WEIGHTS_PATH = MODELS_DIR / "usad_swat_weights.pth"
NORMAL_DATA_PATH = RAW_DATA_DIR / "normal_data.csv"
READINGS_CSV_PATH = RUNTIME_DIR / "sensor_readings.csv"
PREDICTIONS_CSV_PATH = RUNTIME_DIR / "prediction_results.csv"
