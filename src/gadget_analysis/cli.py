"""Command-line entry point: run the whole analysis pipeline."""

import argparse
import sys
from pathlib import Path

from gadget_analysis import latex, plotting, reliability, report
from gadget_analysis.data import X_ITEMS, Y_ITEMS, add_totals, load_responses


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gadget-analysis",
        description="Statistical analysis pipeline for the gadget-use learning study.",
    )
    parser.add_argument("--data", default="data/respondents.csv", type=Path)
    parser.add_argument("--results-dir", default="results", type=Path)
    parser.add_argument("--figures-dir", default="paper/figures", type=Path)
    parser.add_argument("--latex-tex", default="paper/generated/stats.tex", type=Path)
    args = parser.parse_args(argv)

    df = add_totals(load_responses(args.data))
    reliability.validate_reversed(df, X_ITEMS)
    reliability.validate_reversed(df, Y_ITEMS)

    results = report.build_results(df)
    report.write_json(results, args.results_dir / "results.json")
    report.write_markdown(results, args.results_dir / "summary.md")
    latex.write_latex_macros(results, args.latex_tex)
    figures = plotting.generate_all(df, args.figures_dir)

    print(report.format_console(results))
    print(
        f"\nWrote {len(figures)} figures to {args.figures_dir}/, results to "
        f"{args.results_dir}/, and LaTeX macros to {args.latex_tex}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
