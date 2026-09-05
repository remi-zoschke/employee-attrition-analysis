import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    """
    Load raw IBM HR attrition dataset.

    Args:
        path: path to the CSV file
    Returns:
        Raw DataFrame
    """
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove useless variables from IBM HR attrition dataset.

    Args:
        df: raw DataFrame
    Returns:
        Cleaned DataFrame without constant and redundant columns
    """
    cols_to_drop = [
        "EmployeeCount",
        "Over18",
        "StandardHours",
        "DailyRate",
        "HourlyRate",
        "MonthlyRate",
    ]

    df = df.set_index("EmployeeNumber").drop(columns=cols_to_drop)

    return df
