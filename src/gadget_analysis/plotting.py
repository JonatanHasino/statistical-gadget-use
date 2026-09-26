"""Figure generation (PDF) for the paper and reports."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import polars as pl
from scipy import stats

X_LABEL = "Gadget Use (X)"
Y_LABEL = "Learning Motivation & Social Interaction (Y)"


def scatter_with_fit(df: pl.DataFrame, outdir: Path) -> Path:
    """Scatter plot of X vs Y with the simple regression line."""
    x = df["x_total"].to_list()
    y = df["y_total"].to_list()
    fitted = stats.linregress(x, y)
    slope, intercept, r = fitted.slope, fitted.intercept, fitted.rvalue
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.scatter(x, y, s=30, edgecolor="white", linewidth=0.4, zorder=3)
    line_x = [min(x), max(x)]
    ax.plot(line_x, [slope * value + intercept for value in line_x], color="crimson", linewidth=1.2)
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    ax.set_title(f"Gadget Use vs Motivation and Social Interaction (r = {r:.2f})")
    fig.tight_layout()
    path = outdir / "scatter_plot.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def histogram(series: pl.Series, outdir: Path, filename: str, label: str) -> Path:
    """Histogram of a score series with a mean marker."""
    values = series.to_list()
    mean = float(series.mean())
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.hist(values, bins=8, edgecolor="white")
    ax.axvline(mean, color="crimson", linestyle="--", linewidth=1.2, label=f"mean = {mean:.2f}")
    ax.set_xlabel(label)
    ax.set_ylabel("Frequency")
    ax.legend()
    fig.tight_layout()
    path = outdir / filename
    fig.savefig(path)
    plt.close(fig)
    return path


def box_plots(df: pl.DataFrame, outdir: Path) -> Path:
    """Side-by-side box plots for X and Y totals."""
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.boxplot(
        [df["x_total"].to_list(), df["y_total"].to_list()],
        tick_labels=["X (Gadget Use)", "Y (Motivation & Social Interaction)"],
    )
    ax.set_ylabel("Total score")
    fig.tight_layout()
    path = outdir / "box_plots.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def correlation_heatmap(df: pl.DataFrame, outdir: Path) -> Path:
    """Annotated 2x2 correlation heatmap for X and Y totals."""
    r = float(stats.pearsonr(df["x_total"].to_list(), df["y_total"].to_list()).statistic)
    matrix = [[1.0, r], [r, 1.0]]
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    image = ax.imshow(matrix, vmin=-1, vmax=1, cmap="coolwarm")
    for row in range(2):
        for column in range(2):
            ax.text(column, row, f"{matrix[row][column]:.2f}", ha="center", va="center")
    ax.set_xticks([0, 1], labels=["X", "Y"])
    ax.set_yticks([0, 1], labels=["X", "Y"])
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    path = outdir / "correlation_heatmap.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def generate_all(df: pl.DataFrame, outdir: Path) -> dict[str, Path]:
    """Generate every figure; returns name -> path."""
    outdir.mkdir(parents=True, exist_ok=True)
    return {
        "scatter_plot": scatter_with_fit(df, outdir),
        "histogram_x": histogram(df["x_total"], outdir, "histogram_x.pdf", X_LABEL),
        "histogram_y": histogram(df["y_total"], outdir, "histogram_y.pdf", Y_LABEL),
        "box_plots": box_plots(df, outdir),
        "correlation_heatmap": correlation_heatmap(df, outdir),
    }
