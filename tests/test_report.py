import json
from pathlib import Path

import pytest

from gadget_analysis.data import add_totals, load_responses
from gadget_analysis.report import build_results, write_json, write_markdown

DATA_PATH = Path("data/respondents.csv")


@pytest.fixture(scope="module")
def results():
    return build_results(add_totals(load_responses(DATA_PATH)))


def test_build_results_structure(results):
    assert results["data"] == {"n": 69}
    assert set(results["x"]) == {
        "descriptives",
        "distribution",
        "normality",
        "cronbach_alpha",
        "item_total_correlations",
    }
    assert results["bivariate"]["pearson"]["r"] == pytest.approx(0.7325, abs=5e-4)
    assert results["probability"]["counts"]["both"] == 7


def test_write_json(results, tmp_path):
    path = write_json(results, tmp_path / "results.json")
    loaded = json.loads(path.read_text())
    assert loaded["data"]["n"] == 69
    assert loaded["x"]["normality"]["p"] == pytest.approx(0.0338, abs=5e-4)


def test_write_markdown(results, tmp_path):
    path = write_markdown(results, tmp_path / "summary.md")
    text = path.read_text()
    assert "0.7325" in text
    assert "53.66" in text
    assert "Cronbach" in text
    assert "Shapiro" in text or "normality" in text.lower()
