# Feedback-Guided Memory Adaptation Thesis Artifacts

This repository contains the artifact package for the thesis:

**Feedback-Guided Memory Adaptation for Correcting Persistent Persona Errors in AI Companions**

## Repository Contents

| Path | Contents |
| --- | --- |
| `paper/` | Final thesis PDF. |
| `configs/` | Feedback-condition and metric definitions. |
| `data/` | Small public sample data and copy-ready validation cases. |
| `scripts/` | Lightweight metric and figure reproduction scripts. |
| `results/` | Thesis-facing normalized tables. |
| `figures/` | Final figure assets used in the thesis. |
| `live_tui/` | Optional live API terminal demo source, with `.env.example` only. |
| `docs/` | Repository structure, manifest, and reproducibility checklist. |

## Quick Start

Create a local Python environment:

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

Run the offline sample metric computation:

```bash
python scripts/evaluate_metrics.py --input data/samples/raw_dialogue_sample.csv --output results/tables/example_metrics.csv
```

Generate the example figure:

```bash
python scripts/make_figures.py --input results/tables/example_metrics.csv --output figures/example_condition_comparison.png
```

The included thesis tables and figures are fixed artifacts used for inspection. The sample commands above are a small reproducibility smoke test rather than a full rerun of every reported experiment.

## Live TUI Demo

The `live_tui/` folder contains an optional terminal interface for live wrong-prior recovery validation. It requires external API keys and therefore ships only with `.env.example`, not with a real `.env` file.

To run it locally:

```bash
cd live_tui
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
python scripts/fgma_live_tui.py --quick-demo --model deepseek_chat --case-id fs001 --condition C2
```

Replace the model binding with one configured in your local `.env`.

## Notes

The live API demo can create runtime logs under `live_tui/outputs/`; those are ignored by Git. API credentials should be supplied locally through `live_tui/.env`, using `live_tui/.env.example` as the template.
