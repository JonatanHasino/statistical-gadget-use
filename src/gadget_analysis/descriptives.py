"""Descriptive statistics and distribution shape for score series."""

from statistics import quantiles

import polars as pl
from scipy import stats


def describe(series: pl.Series) -> dict[str, float | int]:
    """Return n, mean, median, sample SD, min, max, quartiles, skew, kurtosis."""
    values = series.to_list()
    q1, _, q3 = quantiles(values, n=4, method="inclusive")
    return {
        "n": len(values),
        "mean": float(stats.tmean(values)),
        "median": float(series.median()),
        "sd": float(series.std(ddof=1)),
        "min": int(series.min()),
        "max": int(series.max()),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "skewness": float(stats.skew(values)),
        "kurtosis": float(stats.kurtosis(values)),
    }
