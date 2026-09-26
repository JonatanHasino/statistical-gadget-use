from pathlib import Path

import polars as pl
import pytest

from gadget_analysis.data import X_ITEMS, Y_ITEMS, load_responses
from gadget_analysis.reliability import (
    cronbach_alpha,
    item_total_correlations,
    validate_reversed,
)

DATA_PATH = Path("data/respondents.csv")


def test_cronbach_alpha():
    df = load_responses(DATA_PATH)
    assert cronbach_alpha(df, X_ITEMS) == pytest.approx(0.8850, abs=5e-4)
    assert cronbach_alpha(df, Y_ITEMS) == pytest.approx(0.8794, abs=5e-4)


@pytest.mark.parametrize("items, low, high", [(X_ITEMS, 0.36, 0.70), (Y_ITEMS, 0.35, 0.67)])
def test_item_total_correlations_all_positive(items, low, high):
    df = load_responses(DATA_PATH)
    correlations = item_total_correlations(df, items)
    assert len(correlations) == len(items)
    for r in correlations.values():
        assert 0.0 < r <= 1.0
        assert low <= r <= high


def test_validate_reversed_accepts_real_data():
    df = load_responses(DATA_PATH)
    validate_reversed(df, X_ITEMS)
    validate_reversed(df, Y_ITEMS)


def test_validate_reversed_rejects_raw_items():
    base = [1, 2, 3, 4, 5, 3, 2, 1, 2, 3, 4, 5]
    data = {f"X{i}": base for i in range(1, 15)}
    data["X15"] = [6 - value for value in base]
    df = pl.DataFrame(data)
    with pytest.raises(ValueError, match="reverse-scored"):
        validate_reversed(df, [f"X{i}" for i in range(1, 16)])
