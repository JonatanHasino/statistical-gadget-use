from pathlib import Path

from gadget_analysis.data import add_totals, load_responses
from gadget_analysis.latex import write_latex_macros
from gadget_analysis.report import build_results

DATA_PATH = Path("data/respondents.csv")

EXPECTED = [
    r"\newcommand{\resN}{69}",
    r"\newcommand{\resNItems}{29}",
    r"\newcommand{\resNXItems}{15}",
    r"\newcommand{\resNYItems}{14}",
    r"\newcommand{\resXRangeMin}{15}",
    r"\newcommand{\resXRangeMax}{75}",
    r"\newcommand{\resYRangeMin}{14}",
    r"\newcommand{\resYRangeMax}{70}",
    r"\newcommand{\resXMean}{56.45}",
    r"\newcommand{\resYMean}{50.39}",
    r"\newcommand{\resXMedian}{58}",
    r"\newcommand{\resYMedian}{50}",
    r"\newcommand{\resXSd}{9.09}",
    r"\newcommand{\resYSd}{8.65}",
    r"\newcommand{\resXMin}{31}",
    r"\newcommand{\resXMax}{74}",
    r"\newcommand{\resYMin}{27}",
    r"\newcommand{\resYMax}{70}",
    r"\newcommand{\resR}{0.733}",
    r"\newcommand{\resSig}{0.000}",
    r"\newcommand{\resRSquared}{0.5366}",
    r"\newcommand{\resRSquaredPct}{53.66}",
    r"\newcommand{\resUnexplainedPct}{46.34}",
    r"\newcommand{\resT}{8.808}",
    r"\newcommand{\resF}{77.576}",
    r"\newcommand{\resXNormW}{0.9619}",
    r"\newcommand{\resXNormP}{0.0338}",
    r"\newcommand{\resYNormW}{0.9800}",
    r"\newcommand{\resYNormP}{0.3344}",
    r"\newcommand{\resAlphaX}{0.8850}",
    r"\newcommand{\resAlphaY}{0.8794}",
    r"\newcommand{\resHighX}{30}",
    r"\newcommand{\resHighY}{9}",
    r"\newcommand{\resBoth}{7}",
    r"\newcommand{\resPA}{43.48}",
    r"\newcommand{\resPB}{13.04}",
    r"\newcommand{\resPAB}{10.14}",
    r"\newcommand{\resPBGivenA}{23.33}",
    r"\newcommand{\resPARatio}{0.4348}",
    r"\newcommand{\resPBRatio}{0.1304}",
    r"\newcommand{\resPABRatio}{0.1014}",
    r"\newcommand{\resPBGivenARatio}{0.2333}",
]


def test_write_latex_macros(tmp_path):
    results = build_results(add_totals(load_responses(DATA_PATH)))
    path = write_latex_macros(results, tmp_path / "stats.tex")
    text = path.read_text()
    for expected in EXPECTED:
        assert expected in text, expected


def test_no_empty_macro_values(tmp_path):
    results = build_results(add_totals(load_responses(DATA_PATH)))
    text = write_latex_macros(results, tmp_path / "stats.tex").read_text()
    for line in text.splitlines():
        if line.startswith(r"\newcommand"):
            assert not line.endswith("{}"), line
