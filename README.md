# Statistical Analysis of Gadget Use as a Learning Medium

This repository contains the statistical analysis for the research:

> **From Gadgets to Insights: A Statistical Analysis of Gadget Use as a Learning Medium and Its Relationship with Students’ Learning Motivation and Social Interaction**

The analysis uses data from **69 students** and examines the relationship between:

* **X:** Use of Gadgets as a Learning Medium
* **Y:** Students' Learning Motivation and Social Interaction

The statistical analysis includes:

1. Pearson Correlation
2. Scatter Plot Visualization
3. Descriptive Statistics
4. Simple Linear Regression
5. R-Square
6. t-Test
7. F-Test

## Repository Structure

```text
statistical-analysis-gadget-use/
│
├── README.md
├── data/
├── src/
│   ├── code_01_scatter_plot.py
│   ├── code_02_pearson_correlation.py
│   └── code_03_regression_analysis.py
├── results/
├── docs/
│   └── statistical_analysis.md
├── requirements.txt
└── .gitignore
```

## Requirements

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## How to Run

Run each analysis separately:

```bash
python src/code_01_scatter_plot.py
```

```bash
python src/code_02_pearson_correlation.py
```

```bash
python src/code_03_regression_analysis.py
```

## Analysis Overview

### Code 1 — Scatter Plot

Calculates the Pearson correlation using Pandas and visualizes the relationship between X and Y using a scatter plot.

### Code 2 — Pearson Correlation

Calculates:

* Number of observations
* Mean X
* Mean Y
* Standard deviation X
* Standard deviation Y
* Pearson correlation coefficient
* p-value

### Code 3 — Regression Analysis

Performs:

* Data validation
* Pearson correlation
* Simple linear regression
* R² calculation
* t-test
* F-test
* Statistical significance interpretation

## Research Context

The study uses questionnaire data from 69 students. Variable X represents gadget use as a learning medium, while variable Y represents students' learning motivation and social interaction.

The questionnaire consisted of 29 statements, with 15 statements measuring X and 14 statements measuring Y.
