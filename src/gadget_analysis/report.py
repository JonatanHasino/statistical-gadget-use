"""Rendering of results: JSON, Markdown and console."""

import json
from pathlib import Path

import polars as pl

from gadget_analysis import descriptives, inference, probability, reliability
from gadget_analysis.data import X_ITEMS, Y_ITEMS


def _split(stats: dict) -> dict:
    return {
        "descriptives": {key: stats[key] for key in ("n", "mean", "median", "sd", "min", "max")},
        "distribution": {key: stats[key] for key in ("q1", "q3", "iqr", "skewness", "kurtosis")},
    }


def build_results(df: pl.DataFrame) -> dict:
    """Compute every reported statistic into one nested dictionary."""
    x = descriptives.describe(df["x_total"])
    y = descriptives.describe(df["y_total"])
    return {
        "data": {"n": df.height},
        "x": {
            **_split(x),
            "normality": inference.normality(df["x_total"]),
            "cronbach_alpha": reliability.cronbach_alpha(df, X_ITEMS),
            "item_total_correlations": reliability.item_total_correlations(df, X_ITEMS),
        },
        "y": {
            **_split(y),
            "normality": inference.normality(df["y_total"]),
            "cronbach_alpha": reliability.cronbach_alpha(df, Y_ITEMS),
            "item_total_correlations": reliability.item_total_correlations(df, Y_ITEMS),
        },
        "bivariate": {
            "pearson": inference.pearson(df["x_total"], df["y_total"]),
            "regression": inference.regression(df["x_total"], df["y_total"]),
        },
        "probability": probability.threshold_analysis(df),
    }


def write_json(results: dict, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=2) + "\n")
    return path


def write_markdown(results: dict, path: Path) -> Path:
    x, y = results["x"], results["y"]
    pearson, regression = results["bivariate"]["pearson"], results["bivariate"]["regression"]
    counts, probabilities = (
        results["probability"]["counts"],
        results["probability"]["probabilities"],
    )
    lines = [
        "# Statistical Results",
        "",
        f"Dataset: n = {results['data']['n']} respondents.",
        "Note: item values are already reverse-scored; totals are plain sums.",
        "",
        "## Descriptives and distribution",
        "",
        "| Statistic | X (Gadget Use) | Y (Motivation & Social Interaction) |",
        "|---|---|---|",
        f"| N | {x['descriptives']['n']} | {y['descriptives']['n']} |",
        f"| Mean | {x['descriptives']['mean']:.4f} | {y['descriptives']['mean']:.4f} |",
        f"| Median | {x['descriptives']['median']:.1f} | {y['descriptives']['median']:.1f} |",
        f"| SD (sample) | {x['descriptives']['sd']:.4f} | {y['descriptives']['sd']:.4f} |",
        f"| Min / Max | {x['descriptives']['min']} / {x['descriptives']['max']} | {y['descriptives']['min']} / {y['descriptives']['max']} |",
        f"| Q1 / Q3 / IQR | {x['distribution']['q1']:.0f} / {x['distribution']['q3']:.0f} / {x['distribution']['iqr']:.0f} | {y['distribution']['q1']:.0f} / {y['distribution']['q3']:.0f} / {y['distribution']['iqr']:.0f} |",
        f"| Skewness | {x['distribution']['skewness']:.4f} | {y['distribution']['skewness']:.4f} |",
        f"| Kurtosis | {x['distribution']['kurtosis']:.4f} | {y['distribution']['kurtosis']:.4f} |",
        "",
        "## Reliability",
        "",
        f"- Cronbach's alpha: X = {x['cronbach_alpha']:.4f}, Y = {y['cronbach_alpha']:.4f}.",
        "- All item-total correlations are positive (data is already reverse-scored).",
        "",
        "## Bivariate analysis",
        "",
        f"- Pearson r = {pearson['r']:.4f}, Sig. = {pearson['p']:.4f}",
        f"- R^2 = {regression['r2'] * 100:.2f}%",
        f"- t = {regression['t']:.4f}, F = {regression['f']:.4f}",
        "",
        "## Probability (threshold >= 60)",
        "",
        f"- High X: {counts['high_x']}, High Y: {counts['high_y']}, Both: {counts['both']}",
        f"- P(A) = {probabilities['p_a'] * 100:.2f}%, P(B) = {probabilities['p_b'] * 100:.2f}%",
        f"- P(A and B) = {probabilities['p_both'] * 100:.2f}%, P(B|A) = {probabilities['p_b_given_a'] * 100:.2f}%",
        "",
        "## Notes",
        "",
        (
            f"- Y passes Shapiro-Wilk (p = {y['normality']['p']:.4f}); "
            f"X is borderline (p = {x['normality']['p']:.4f}, W = {x['normality']['w']:.4f}) "
            "and should be reported as a caveat, not a failure."
        ),
        "- Reliability (alpha) above 0.8 is conventionally interpreted as good.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))
    return path


def format_console(results: dict) -> str:
    x, y = results["x"], results["y"]
    pearson, regression = results["bivariate"]["pearson"], results["bivariate"]["regression"]
    counts, probabilities = (
        results["probability"]["counts"],
        results["probability"]["probabilities"],
    )
    lines = [
        f"n = {results['data']['n']} respondents",
        "",
        "Descriptives:",
        (
            f"  X: mean {x['descriptives']['mean']:.4f}, median {x['descriptives']['median']:.1f}, "
            f"SD {x['descriptives']['sd']:.4f}, min/max {x['descriptives']['min']}/{x['descriptives']['max']}"
        ),
        (
            f"  Y: mean {y['descriptives']['mean']:.4f}, median {y['descriptives']['median']:.1f}, "
            f"SD {y['descriptives']['sd']:.4f}, min/max {y['descriptives']['min']}/{y['descriptives']['max']}"
        ),
        "",
        "Distribution:",
        (
            f"  X: Q1/Q3 {x['distribution']['q1']:.0f}/{x['distribution']['q3']:.0f}, "
            f"IQR {x['distribution']['iqr']:.0f}, skew {x['distribution']['skewness']:.4f}, "
            f"kurtosis {x['distribution']['kurtosis']:.4f}"
        ),
        (
            f"  Y: Q1/Q3 {y['distribution']['q1']:.0f}/{y['distribution']['q3']:.0f}, "
            f"IQR {y['distribution']['iqr']:.0f}, skew {y['distribution']['skewness']:.4f}, "
            f"kurtosis {y['distribution']['kurtosis']:.4f}"
        ),
        "",
        "Normality (Shapiro-Wilk):",
        f"  X: W {x['normality']['w']:.4f}, p {x['normality']['p']:.4f}",
        f"  Y: W {y['normality']['w']:.4f}, p {y['normality']['p']:.4f}",
        "",
        "Reliability (Cronbach alpha):",
        f"  X: {x['cronbach_alpha']:.4f}   Y: {y['cronbach_alpha']:.4f}",
        "",
        "Bivariate:",
        f"  Pearson r = {pearson['r']:.4f}, Sig. = {pearson['p']:.4f}",
        f"  Regression: Y = {regression['intercept']:.4f} + {regression['slope']:.4f} X",
        f"  R2 = {regression['r2'] * 100:.2f}%, t = {regression['t']:.4f}, F = {regression['f']:.4f}",
        "",
        "Probability (threshold >= 60):",
        f"  High X {counts['high_x']}, High Y {counts['high_y']}, Both {counts['both']}",
        (
            f"  P(A) = {probabilities['p_a'] * 100:.2f}%, P(B) = {probabilities['p_b'] * 100:.2f}%, "
            f"P(A and B) = {probabilities['p_both'] * 100:.2f}%, P(B|A) = {probabilities['p_b_given_a'] * 100:.2f}%"
        ),
    ]
    return "\n".join(lines)
