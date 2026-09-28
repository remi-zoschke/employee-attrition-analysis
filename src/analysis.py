import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind


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
