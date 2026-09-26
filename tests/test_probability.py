from pathlib import Path

import pytest

from gadget_analysis.data import add_totals, load_responses
from gadget_analysis.probability import threshold_analysis

DATA_PATH = Path("data/respondents.csv")


def test_threshold_analysis():
    df = add_totals(load_responses(DATA_PATH))
    result = threshold_analysis(df)
    assert result["counts"] == {"n": 69, "high_x": 30, "high_y": 9, "both": 7}
    assert result["probabilities"]["p_a"] == pytest.approx(43.48 / 100, abs=5e-4)
    assert result["probabilities"]["p_b"] == pytest.approx(13.04 / 100, abs=5e-4)
    assert result["probabilities"]["p_both"] == pytest.approx(10.14 / 100, abs=5e-4)
    assert result["probabilities"]["p_b_given_a"] == pytest.approx(23.33 / 100, abs=5e-4)
