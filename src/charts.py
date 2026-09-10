"""Plotly charts for interactive visualizations."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Attrition Analytics Theme Colors
ATTRITION_COLORS = {"Oui": "#F87171", "Non": "#34D399"}
PRIMARY_COLOR = "#4682B4"


def create_donut_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    total: int | None = None,
) -> go.Figure:
    """
    Create a donut chart.

    Args:
        df: DataFrame
        values: column name for values
        names: column name for labels
        title: chart title
        total: optional total to display in center

    Returns:
        Plotly figure
    """
    fig = px.pie(
        df,
        values=values,
        names=names,
        title=f"<b>{title}</b>",
        color=names,
        color_discrete_map=ATTRITION_COLORS,
        hole=0.45,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont_size=18,
        hovertemplate="%{label}: %{percent}",
        marker={"line": {"color": "white", "width": 3}},
    )
    fig.update_layout(
        showlegend=False,
        title_x=0.5,
        title_font_size=22,
        title_xanchor="center",
        margin={"t": 30, "b": 40, "l": 40, "r": 40},
        annotations=[
            {
                "text": f"{total}<br>employés" if total else "",
                "x": 0.5,
                "y": 0.5,
                "font_size": 20,
                "showarrow": False,
            }
        ],
    )

    return fig
