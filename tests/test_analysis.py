from pathlib import Path

import pytest

from gadget_analysis.data import add_totals, load_responses
from gadget_analysis.descriptives import describe
from gadget_analysis.inference import normality, pearson, regression

DATA_PATH = Path("data/respondents.csv")

EXPECTED_X = {
    "n": 69,
    "mean": 56.44927536231884,
    "median": 58.0,
    "sd": 9.088674645960186,
    "min": 31,
    "max": 74,
    "q1": 48.0,
    "q3": 63.0,
    "iqr": 15.0,
    "skewness": -0.3410,
    "kurtosis": -0.5820,
}

EXPECTED_Y = {
    "n": 69,
    "mean": 50.391304347826086,
    "median": 50.0,
    "sd": 8.645327522976775,
    "min": 27,
    "max": 70,
    "q1": 44.0,
    "q3": 56.0,
    "iqr": 12.0,
    "skewness": -0.1544,
    "kurtosis": 0.3038,
}


@pytest.mark.parametrize("column, expected", [("x_total", EXPECTED_X), ("y_total", EXPECTED_Y)])
def test_describe(column, expected):
    df = add_totals(load_responses(DATA_PATH))
    result = describe(df[column])
    assert result["n"] == expected["n"]
    assert result["min"] == expected["min"]
    assert result["max"] == expected["max"]
    for key in ("mean", "median", "sd", "q1", "q3", "iqr"):
        assert result[key] == pytest.approx(expected[key], abs=1e-4)
    assert result["skewness"] == pytest.approx(expected["skewness"], abs=5e-4)
    assert result["kurtosis"] == pytest.approx(expected["kurtosis"], abs=5e-4)


def test_pearson():
    df = add_totals(load_responses(DATA_PATH))
    result = pearson(df["x_total"], df["y_total"])
    assert result["r"] == pytest.approx(0.7325, abs=5e-4)
    assert result["p"] < 1e-10


def test_regression():
    df = add_totals(load_responses(DATA_PATH))
    result = regression(df["x_total"], df["y_total"])
    assert result["slope"] == pytest.approx(0.696781, abs=1e-5)
    assert result["intercept"] == pytest.approx(11.058520, abs=1e-5)
    assert result["stderr"] == pytest.approx(0.0791, abs=5e-4)
    assert result["r2"] == pytest.approx(0.5366, abs=5e-4)
    assert result["t"] == pytest.approx(8.8077, abs=5e-4)
    assert result["f"] == pytest.approx(77.5759, abs=0.01)
    assert result["p"] < 1e-10


@pytest.mark.parametrize(
    "column, w, p",
    [("x_total", 0.9619, 0.0338), ("y_total", 0.9800, 0.3344)],
)
def test_normality(column, w, p):
    df = add_totals(load_responses(DATA_PATH))
    result = normality(df[column])
    assert result["w"] == pytest.approx(w, abs=5e-4)
    assert result["p"] == pytest.approx(p, abs=5e-4)
