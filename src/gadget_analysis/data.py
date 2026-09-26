"""Load and validate the respondent dataset.

Invariant: the item values in data/respondents.csv are already
reverse-scored for negatively worded items. This module and the whole
pipeline sum item values as-is and must never apply (6 - score).
"""

from pathlib import Path

import polars as pl

X_ITEMS = [f"X{i}" for i in range(1, 16)]
Y_ITEMS = [f"Y{i}" for i in range(1, 15)]
ITEM_COLUMNS = [*X_ITEMS, *Y_ITEMS]
ID_COLUMN = "respondent"
REQUIRED_COLUMNS = [ID_COLUMN, *ITEM_COLUMNS]


def load_responses(path: str | Path) -> pl.DataFrame:
    """Load the CSV and validate it against the data contract."""
    df = pl.read_csv(path)
    validate(df)
    return df


def validate(df: pl.DataFrame) -> None:
    """Raise ValueError when the data contract is violated."""
    if df.columns != REQUIRED_COLUMNS:
        raise ValueError(f"Unexpected columns: expected {REQUIRED_COLUMNS}, got {df.columns}")
    if df[ID_COLUMN].null_count() or df[ID_COLUMN].n_unique() != df.height:
        raise ValueError("respondent values must be unique and non-null")
    for column in ITEM_COLUMNS:
        series = df[column]
        if series.null_count():
            raise ValueError(f"Column {column} contains missing values")
        if not series.dtype.is_integer():
            raise ValueError(f"Column {column} must contain integers, got {series.dtype}")
        if series.min() < 1 or series.max() > 5:
            raise ValueError(f"Column {column} has values outside 1-5")


def add_totals(df: pl.DataFrame) -> pl.DataFrame:
    """Add x_total / y_total as plain item sums (values are pre-reversed)."""
    return df.with_columns(
        pl.sum_horizontal(X_ITEMS).alias("x_total"),
        pl.sum_horizontal(Y_ITEMS).alias("y_total"),
    )
