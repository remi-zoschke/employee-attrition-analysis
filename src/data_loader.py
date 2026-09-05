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


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
     Create new features and recode existing variables for analysis.

    Args:
        df: cleaned DataFrame
    Returns:
        DataFrame with engineered features
    """
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[18, 25, 35, 45, 60],
        labels=["18-25", "26-35", "36-45", "46-60"],
    )

    df["TenureGroup"] = pd.cut(
        df["YearsAtCompany"],
        bins=[-1, 2, 10, 40],
        labels=["0-2 ans", "3-10 ans", "11+ ans"],
    )

    df["EducationField"] = df["EducationField"].replace("Human Resources", "Other")

    df["IncomeGroup"] = pd.cut(
        df["MonthlyIncome"],
        bins=[1000, 3000, 5000, 8500, 20000],
        labels=["Bas", "Moyen", "Élevé", "Très élevé"],
    )

    df["StockOptionGroup"] = df["StockOptionLevel"].map(
        {0: "0", 1: "1", 2: "2+", 3: "2+"}
    )

    df["ManagerTenureGroup"] = pd.cut(
        df["YearsWithCurrManager"],
        bins=[-1, 0, 3, 17],
        labels=["0", "1-3 ans", "4+ ans"],
    )

    return df


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorder columns for readability: target first, then raw variables,
    then derived/grouped variables placed next to their source.

    Args:
        df: DataFrame with engineered features
    Returns:
        DataFrame with reordered columns
    """
    column_order = [
        "AttritionNum",
        "Age",
        "AgeGroup",
        "Gender",
        "MaritalStatus",
        "Education",
        "EducationField",
        "Department",
        "JobRole",
        "JobLevel",
        "BusinessTravel",
        "DistanceFromHome",
        "MonthlyIncome",
        "IncomeGroup",
        "PercentSalaryHike",
        "StockOptionLevel",
        "StockOptionGroup",
        "OverTime",
        "TotalWorkingYears",
        "YearsAtCompany",
        "TenureGroup",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
        "YearsWithCurrManager",
        "ManagerTenureGroup",
        "NumCompaniesWorked",
        "TrainingTimesLastYear",
        "EnvironmentSatisfaction",
        "JobSatisfaction",
        "JobInvolvement",
        "WorkLifeBalance",
        "RelationshipSatisfaction",
        "PerformanceRating",
    ]

    return df[column_order]


def save_processed(df: pd.DataFrame, path: str) -> None:
    """
    Save the fully processed DataFrame to Parquet format.

    Args:
        df: processed DataFrame
        path: output path
    """
    df.to_parquet(path, index=True)


def load_processed(path: str) -> pd.DataFrame:
    """
    Load the processed dataset from Parquet.

    Args:
        path: path to the parquet file
    Returns:
        Processed DataFrame
    """
    return pd.read_parquet(path)
