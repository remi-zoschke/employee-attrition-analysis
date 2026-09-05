"""Prepare the Meridian Pharma HR attrition dataset."""
from pathlib import Path

from src.config import PROCESSED_DATA_PATH, RAW_DATA_PATH
from src.data_loader import (
    clean_data,
    engineer_features,
    load_raw_data,
    recode_target,
    reorder_columns,
    save_processed,
)


def prepare_data(
    raw_path: str | Path,
    output_path: str | Path | None = None,
) -> None:
    """Load, clean, and transform the raw dataset into a processed Parquet file.

    Args:
        raw_path: Path to the raw CSV file.
        output_path: Optional path to save the processed Parquet file.
    """
    df = load_raw_data(raw_path)
    df = clean_data(df)
    df = recode_target(df)
    df = engineer_features(df)
    df = reorder_columns(df)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_processed(df, output_path)
        print(f"Processed {len(df)} records -> {output_path}")


if __name__ == "__main__":
    prepare_data(raw_path=RAW_DATA_PATH, output_path=PROCESSED_DATA_PATH)