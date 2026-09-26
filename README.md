# Statistical Analysis of Gadget Use as a Learning Medium

Statistical analysis for the research:

> **From Gadgets to Insights: A Statistical Analysis of Gadget Use as a Learning Medium and Its Relationship with Students' Learning Motivation and Social Interaction**

Data: 69 respondents, 29 questionnaire items (X: 15 items on gadget use;
Y: 14 items on learning motivation and social interaction). The item
values in `data/respondents.csv` are already reverse-scored; totals are
plain sums. See `docs/dataset.txt` for the dataset access notice.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Run the analysis

```bash
uv run gadget-analysis
```

Outputs:

- console summary of every statistic;
- `results/results.json` (machine-readable);
- `results/summary.md` (human-readable tables);
- `figures/` (five PDFs; the paper consumes them from `paper/figures/`);
- `paper/generated/stats.tex` (LaTeX macros the paper uses for its numbers).

Paths are configurable:

```bash
uv run gadget-analysis --data data/respondents.csv --results-dir results --figures-dir paper/figures
```

## Paper

The LaTeX document in `paper/` consumes the generated macros and figures.
After the data or the pipeline change, regenerate and rebuild:

```bash
uv run gadget-analysis --figures-dir paper/figures
cd paper && latexmk
```

## Tests and lint

```bash
uv run pytest
uv run ruff check
uv run ruff format --check
```

## Repository structure

```text
data/respondents.csv        anonymized item-level responses
src/gadget_analysis/        analysis package (pipeline modules)
tests/                      pytest suite with locked expected values
docs/dataset.txt            dataset access notice
paper/                      LaTeX write-up of the research
```
