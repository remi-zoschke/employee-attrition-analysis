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


def recode_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recode Attrition from Yes/No to a binary target variable.

    Args:
        df: cleaned DataFrame
    Returns:
        DataFrame with AttritionNum (0/1) replacing Attrition
    """
    df = df.copy()
    df["AttritionNum"] = (df["Attrition"] == "Yes").astype(int)

    return df.drop(columns=["Attrition"])
