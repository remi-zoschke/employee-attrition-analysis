"""Global project configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "ibm_hr_attrition.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "meridian_pharma_hr_attrition.parquet"

# Modeling
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Replacement cost ratios (SHRM)
COST_MIN_RATIO = 0.5
COST_MAX_RATIO = 2.0
