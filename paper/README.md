# Article sources

LaTeX sources of the research article. The compiled PDF is not distributed
in this repository; the article is available on Medium (see the repository
root README).

## License

The article sources in this directory are licensed under the Creative
Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public
License (CC BY-NC-ND 4.0). The full license text is in the repository root
`LICENSE` file (Part 2).

## Building

The document consumes generated inputs (`generated/stats.tex` and
`figures/*.pdf`) produced by the analysis pipeline in `src/gadget_analysis`.
Regenerate them with:

```bash
uv run gadget-analysis
cd paper && latexmk
```
