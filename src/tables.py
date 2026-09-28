"""Formatted tables for statistical test results."""

import pandas as pd
import polars as pl
from great_tables import GT, loc, style


def create_ttest_table(df: pd.DataFrame, labels: dict | None = None) -> GT:
    """
    Create a formatted t-test results table.

    Args:
        df: DataFrame from ttest_tests function
        labels: optional dict to translate variable names

    Returns:
        Great Tables object
    """
    df = df.reset_index(drop=True).copy()
    if labels:
        df["variable"] = df["variable"].map(labels).fillna(df["variable"])
    df_pl = pl.from_pandas(df)

    return (
        GT(df_pl)
        .tab_header(title="Tests de Student")
        .cols_label(
            variable="Variable",
            mean_yes="Moy. partants",
            mean_no="Moy. restants",
            t_stat="Statistique t",
            p_value="p-value",
            cohens_d="Cohen's d",
        )
        .cols_hide(columns=["keep", "t_stat"])
        .cols_align(align="center")
        .cols_align(align="left", columns="variable")
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.column_labels(),
        )
        .fmt_number(columns=["mean_yes", "mean_no"], decimals=1, use_seps=False)
        .fmt_number(columns="t_stat", decimals=2)
        .fmt_number(columns="p_value", decimals=4)
        .fmt_number(columns="cohens_d", decimals=2)
        .tab_style(
            style=style.fill(color="#DCFCE7"),
            locations=loc.body(rows=pl.col("keep") == True),
        )
        .tab_style(
            style=style.fill(color="#F3F4F6"),
            locations=loc.body(rows=pl.col("keep") == False),
        )
    )


def create_chi2_table(df: pd.DataFrame, labels: dict | None = None) -> GT:
    """
    Create a formatted chi2 results table.

    Args:
        df: DataFrame from chi2_tests function
        labels: optional dict to translate variable names

    Returns:
        Great Tables object
    """
    df = df.reset_index(drop=True).copy()
    if labels:
        df["variable"] = df["variable"].map(labels).fillna(df["variable"])
    df_pl = pl.from_pandas(df)

    return (
        GT(df_pl)
        .tab_header(title="Variables catégorielles — significativité")
        .cols_label(
            variable="Variable",
            chi2="Chi2",
            p_value="p-value",
            dof="ddl",
            cramers_v="V de Cramér",
        )
        .cols_hide(columns=["keep", "chi2", "dof"])
        .cols_align(align="center")
        .cols_align(align="left", columns="variable")
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.column_labels(),
        )
        .fmt_number(columns="chi2", decimals=1)
        .fmt_number(columns="p_value", decimals=4)
        .fmt_number(columns="cramers_v", decimals=3)
        .fmt_integer(columns="dof")
        .tab_style(
            style=style.fill(color="#DCFCE7"),
            locations=loc.body(rows=pl.col("keep") == True),
        )
        .tab_style(
            style=style.fill(color="#F3F4F6"),
            locations=loc.body(rows=pl.col("keep") == False),
        )
    )
