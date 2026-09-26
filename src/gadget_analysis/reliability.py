"""Scale reliability and the already-reversed-data guard."""

import polars as pl
from scipy import stats


def cronbach_alpha(df: pl.DataFrame, items: list[str]) -> float:
    """Cronbach's alpha for the given item columns."""
    k = len(items)
    item_variances = sum(df[item].var(ddof=1) for item in items)
    total = df.select(pl.sum_horizontal(items)).to_series()
    return float((k / (k - 1)) * (1 - item_variances / total.var(ddof=1)))


def item_total_correlations(df: pl.DataFrame, items: list[str]) -> dict[str, float]:
    """Correlation of each item with the sum of the remaining items."""
    result: dict[str, float] = {}
    for item in items:
        rest = [other for other in items if other != item]
        rest_sum = df.select(pl.sum_horizontal(rest)).to_series().to_list()
        r, _ = stats.pearsonr(df[item].to_list(), rest_sum)
        result[item] = float(r)
    return result


def validate_reversed(df: pl.DataFrame, items: list[str]) -> None:
    """Raise if any item correlates negatively with its scale's remainder.

    Negative correlations indicate raw (not yet reverse-scored) answers to
    negatively worded items, which the pipeline must never silently sum.
    """
    for item, r in item_total_correlations(df, items).items():
        if r <= 0:
            raise ValueError(
                f"Item {item} correlates negatively (r={r:.3f}) with the rest of "
                "its scale; the dataset appears not to be reverse-scored."
            )
