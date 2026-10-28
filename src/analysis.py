import numpy as np
import pandas as pd
import shap
import statsmodels.api as sm
from scipy.stats import chi2_contingency, f_oneway, ttest_ind
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder


def ttest_tests(df: pd.DataFrame, vars: list[str]) -> pd.DataFrame:
    """
    T-tests between continuous variables and attrition.
    Includes Cohen's d to measure effect size.

    Args:
        df: DataFrame
        vars: list of continuous variable names
    Returns:
        DataFrame with t-statistic, p_value, Cohen's d and recommendation
    """
    results = []
    for var in vars:
        group_yes = df[df["AttritionNum"] == 1][var]
        group_no = df[df["AttritionNum"] == 0][var]
        t_stat, p_value = ttest_ind(group_yes, group_no)
        pooled_std = float(np.sqrt((group_yes.std() ** 2 + group_no.std() ** 2) / 2))
        cohens_d = abs(float((group_yes.mean() - group_no.mean()) / pooled_std))
        results.append(
            {
                "variable": var,
                "mean_yes": round(float(group_yes.mean()), 2),
                "mean_no": round(float(group_no.mean()), 2),
                "t_stat": round(float(t_stat), 2),
                "p_value": float(f"{p_value:.2e}"),
                "cohens_d": round(cohens_d, 3),
                "keep": p_value < 0.05 and cohens_d >= 0.2,
            }
        )
    return pd.DataFrame(results).sort_values("cohens_d", ascending=False)


def chi2_tests(df: pd.DataFrame, vars: list[str]) -> pd.DataFrame:
    """
    Chi2 tests between a list of categorical variables and attrition.
    Includes Cramér's V to measure effect size.

    Args:
        df: DataFrame
        vars: list of categorical variable names
    Returns:
        DataFrame with chi2, p_value, dof, cramers_v and recommendation
    """
    results = []
    for var in vars:
        ct = pd.crosstab(df[var], df["AttritionNum"])
        chi2, p_value, dof, _ = chi2_contingency(ct)
        n = ct.sum().sum()
        cramers_v = float(np.sqrt(chi2 / (n * (min(ct.shape) - 1))))
        significant = p_value < 0.05
        strong = cramers_v >= 0.1
        results.append(
            {
                "variable": var,
                "chi2": round(float(chi2), 2),
                "p_value": float(f"{p_value:.2e}"),
                "dof": dof,
                "cramers_v": round(cramers_v, 3),
                "keep": significant and strong,
            }
        )
    return pd.DataFrame(results).sort_values("cramers_v", ascending=False)


def correlation_matrix(
    df: pd.DataFrame, vars: list[str], threshold: float = 0.7
) -> pd.DataFrame:
    """
    Compute correlation matrix and flag pairs above threshold.

    Args:
        df: DataFrame
        vars: list of continuous variable names
        threshold: correlation threshold for multicollinearity

    Returns:
        DataFrame with variable pairs and their correlation
    """
    corr = df[vars].corr().round(2)
    pairs = []
    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            r = corr.iloc[i, j]
            if abs(r) >= threshold:
                pairs.append(
                    {
                        "var_1": vars[i],
                        "var_2": vars[j],
                        "correlation": r,
                    }
                )
    return pd.DataFrame(pairs).sort_values("correlation", ascending=False)


def anova_tests(
    df: pd.DataFrame, cat_vars: list[str], num_vars: list[str]
) -> pd.DataFrame:
    """
    ANOVA tests between categorical and continuous variables.

    Args:
        df: DataFrame
        cat_vars: list of categorical variable names
        num_vars: list of continuous variable names
    Returns:
        DataFrame with F-statistic and p_value for all combinations
    """
    results = []
    for num_var in num_vars:
        for cat_var in cat_vars:
            groups = [
                df[df[cat_var] == level][num_var].values
                for level in df[cat_var].unique()
            ]
            f_stat, p_value = f_oneway(*groups)
            results.append(
                {
                    "cat_var": cat_var,
                    "num_var": num_var,
                    "f_stat": round(float(f_stat), 2),
                    "p_value": float(f"{p_value:.2e}"),
                    "significant": p_value < 0.05,
                }
            )
    return pd.DataFrame(results).sort_values("f_stat", ascending=False)


def logistic_regression_explain(
    df: pd.DataFrame,
    continuous: list[str],
    categorical: list[str],
) -> tuple:
    """
    Fit an explanatory logistic regression model.

    Args:
        df: DataFrame with AttritionNum and selected features
        continuous: list of continuous variable names
        categorical: list of categorical variable names

    Returns:
        Tuple of (model result, odds ratios DataFrame)
    """
    X = df[continuous + categorical].copy()
    X["MonthlyIncome"] = X["MonthlyIncome"] / 1000

    X = pd.get_dummies(X, columns=categorical, drop_first=True).astype(float)
    X = sm.add_constant(X)

    y = df["AttritionNum"]

    model = sm.Logit(y, X)
    result = model.fit(disp=0)

    odds = pd.DataFrame(
        {
            "variable": result.params.index,
            "coefficient": result.params.values.round(3),
            "odds_ratio": np.exp(result.params).values.round(3),
            "p_value": result.pvalues.values.round(4),
        }
    )
    odds = odds[odds["variable"] != "const"]

    return result, odds


def logistic_regression_predict(
    df: pd.DataFrame,
    continuous: list[str],
    categorical: list[str],
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple:
    """
    Fit a predictive logistic regression.

    Args:
        df: DataFrame with AttritionNum and features
        continuous: list of continuous variable names
        categorical: list of categorical variable names
        test_size: proportion of test set
        random_state: seed for reproducibility

    Returns:
        Tuple of (pipeline, X_test, y_test, y_pred, y_pred_proba)
    """
    X = df[continuous + categorical]
    y = df["AttritionNum"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", MinMaxScaler(), continuous),
            (
                "cat",
                OneHotEncoder(drop="if_binary", handle_unknown="ignore"),
                categorical,
            ),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(random_state=random_state, class_weight="balanced"),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]

    return pipeline, X_test, y_test, y_pred, y_pred_proba


def compute_shap_values(pipeline, X_test: pd.DataFrame) -> tuple:
    """
    Compute SHAP values from a fitted pipeline.

    Args:
        pipeline: fitted sklearn pipeline
        X_test: test features DataFrame

    Returns:
        Tuple of (shap_values, feature_names)
    """
    classifier = pipeline.named_steps["classifier"]
    X_test_transformed = pipeline.named_steps["preprocessor"].transform(X_test)

    explainer = shap.LinearExplainer(classifier, X_test_transformed)
    shap_values = explainer.shap_values(X_test_transformed)

    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    feature_names = [
        name.replace("num__", "").replace("cat__", "") for name in feature_names
    ]

    return shap_values, feature_names
