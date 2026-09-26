"""Threshold-based event probabilities over the sample space."""

import polars as pl


def threshold_analysis(df: pl.DataFrame, threshold: int = 60) -> dict:
    """Counts and probabilities of high-X, high-Y, both, and P(B|A)."""
    high_x = df.filter(pl.col("x_total") >= threshold).height
    high_y = df.filter(pl.col("y_total") >= threshold).height
    both = df.filter((pl.col("x_total") >= threshold) & (pl.col("y_total") >= threshold)).height
    n = df.height
    return {
        "counts": {"n": n, "high_x": high_x, "high_y": high_y, "both": both},
        "probabilities": {
            "p_a": high_x / n,
            "p_b": high_y / n,
            "p_both": both / n,
            "p_b_given_a": (both / n) / (high_x / n),
        },
    }
