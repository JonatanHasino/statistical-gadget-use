# Statistical Analysis of Gadget Use as a Learning Medium

Statistical analysis for the research:

> **From Gadgets to Insights: A Statistical Analysis of Gadget Use as a Learning Medium and Its Relationship with Students' Learning Motivation and Social Interaction**

Data: 69 respondents, 29 questionnaire items (X: 15 items on gadget use;
Y: 14 items on learning motivation and social interaction). The anonymized
item-level dataset is published at `data/respondents.csv`; its use terms are
in `docs/dataset.txt`. The item values are already reverse-scored, so totals
are plain sums.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Run the analysis

```bash
uv run gadget-analysis
```

Outputs (all generated, all ignored by git):

- console summary of every statistic;
- `results/results.json` (machine-readable);
- `results/summary.md` (human-readable tables);
- `paper/figures/` (five PDFs the LaTeX sources consume);
- `paper/generated/stats.tex` (LaTeX macros the paper uses for its numbers).

Paths are configurable; the defaults are shown:

```bash
uv run gadget-analysis --data data/respondents.csv --results-dir results --figures-dir paper/figures
```

## Paper

The LaTeX sources in `paper/` consume the generated macros and figures.
After the data or the pipeline change, regenerate and rebuild:

```bash
uv run gadget-analysis
cd paper && latexmk
```

The compiled PDF is not distributed in this repository; see the article
link below.

## Tests and lint

```bash
uv run pytest
uv run ruff check
uv run ruff format --check
```

## Repository structure

```text
data/respondents.csv        anonymized item-level responses (see docs/dataset.txt)
src/gadget_analysis/        analysis package (pipeline modules)
tests/                      pytest suite with locked expected values
docs/dataset.txt            dataset availability and access notice
paper/                      LaTeX sources of the article (see paper/README.md)
LICENSE                     dual license: MIT (code) + CC BY-NC-ND 4.0 (content)
```

## Article

The full research article, including the methodology, statistical analysis,
and interpretation of the results, is available on Medium:

[**From Gadgets to Insights: A Statistical Analysis of Gadget Use as a Learning Medium and Its Relationship with Students' Learning Motivation and Social Interaction**](https://medium.com/@jonatanlimsaklim749/from-gadgets-to-insights-a-statistical-analysis-of-gadget-use-as-a-learning-medium-and-its-bba39bf7e9fb)

## License

This repository is dual-licensed by content type (full texts in `LICENSE`):

- **Software** (`src/`, `tests/`, configuration): MIT License.
- **Content** (article sources in `paper/`, documentation in `docs/`, and
  this README): CC BY-NC-ND 4.0 — share verbatim with attribution; no
  commercial use and no derivative works without permission.
- **Dataset** (`data/respondents.csv`): governed by `docs/dataset.txt`, not
  by the CC content license.
