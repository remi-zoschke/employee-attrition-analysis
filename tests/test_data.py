import pytest

from src.analysis import (
    chi2_tests,
    logistic_regression_explain,
    logistic_regression_predict,
    ttest_tests,
)
from src.data_loader import clean_data, engineer_features, load_raw_data, recode_target


@pytest.fixture
def df():
    """Load and prepare test DataFrame."""
    raw = load_raw_data("data/raw/ibm_hr_attrition.csv")
    cleaned = clean_data(raw)
    recoded = recode_target(cleaned)
    return recoded


class TestDataPipeline:
    """Tests for data loading and cleaning."""

    def test_clean_data_removes_columns(self):
        df = load_raw_data("data/raw/ibm_hr_attrition.csv")
        df_clean = clean_data(df)
        assert "EmployeeCount" not in df_clean.columns
        assert "StandardHours" not in df_clean.columns

    def test_engineer_features_creates_columns(self):
        df = load_raw_data("data/raw/ibm_hr_attrition.csv")
        df_clean = clean_data(df)
        df_feat = engineer_features(df_clean)
        assert "AgeGroup" in df_feat.columns
        assert "IncomeGroup" in df_feat.columns

    def test_clean_data_row_count(self):
        df = load_raw_data("data/raw/ibm_hr_attrition.csv")
        df_clean = clean_data(df)
        assert len(df_clean) == 1470


class TestAnalysis:
    """Tests for statistical analysis functions."""

    def test_ttest_returns_expected_columns(self, df):
        result = ttest_tests(df, ["Age", "MonthlyIncome"])
        assert "variable" in result.columns
        assert "p_value" in result.columns
        assert "cohens_d" in result.columns
        assert len(result) == 2

    def test_chi2_returns_expected_columns(self, df):
        result = chi2_tests(df, ["OverTime", "Gender"])
        assert "variable" in result.columns
        assert "p_value" in result.columns
        assert "cramers_v" in result.columns
        assert len(result) == 2


class TestModeling:
    """Tests for modeling functions."""

    def test_logistic_regression_explain_returns_tuple(self, df):
        _result, odds = logistic_regression_explain(
            df,
            continuous=["MonthlyIncome", "Age"],
            categorical=["OverTime"],
        )
        assert odds is not None
        assert "odds_ratio" in odds.columns
        assert "p_value" in odds.columns

    def test_logistic_regression_predict_returns_tuple(self, df):
        _pipeline, _X_test, y_test, y_pred, y_pred_proba = logistic_regression_predict(
            df,
            continuous=["MonthlyIncome", "Age"],
            categorical=["OverTime"],
        )
        assert len(y_pred) == len(y_test)
        assert len(y_pred_proba) == len(y_test)
