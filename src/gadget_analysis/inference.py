"""Bivariate inference: Pearson correlation, simple regression, normality."""

from math import sqrt

import polars as pl
from scipy import stats


def pearson(x: pl.Series, y: pl.Series) -> dict[str, float]:
    """Pearson correlation coefficient and its two-sided p-value."""
    r, p = stats.pearsonr(x.to_list(), y.to_list())
    return {"r": float(r), "p": float(p)}


def regression(x: pl.Series, y: pl.Series) -> dict[str, float]:
    """Simple linear regression Y = intercept + slope * X with t and F."""
    x_values = x.to_list()
    result = stats.linregress(x_values, y.to_list())
    r = float(result.rvalue)
    r2 = r * r
    degrees_of_freedom = len(x_values) - 2
    t = r * sqrt(degrees_of_freedom / (1 - r2))
    return {
        "slope": float(result.slope),
        "intercept": float(result.intercept),
        "stderr": float(result.stderr),
        "r2": r2,
        "t": t,
        "f": t * t,
        "p": float(result.pvalue),
    }


def normality(series: pl.Series) -> dict[str, float]:
    """Shapiro-Wilk normality test."""
    w, p = stats.shapiro(series.to_list())
    return {"w": float(w), "p": float(p)}
