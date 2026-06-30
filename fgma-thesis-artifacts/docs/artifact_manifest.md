# Artifact Manifest

| Artifact | Location | Status |
| --- | --- | --- |
| Condition config | `configs/experiment_conditions.yaml` | Included |
| Sample dialogue rows | `data/samples/raw_dialogue_sample.csv` | Included |
| Validation case text | `data/validation_cases/` and `live_tui/validation_cases/` | Included |
| Metric script | `scripts/evaluate_metrics.py` | Included |
| Figure script | `scripts/make_figures.py` | Included |
| Thesis result tables | `results/tables/` | Included |
| Final figure assets | `figures/` | Included |
| Optional live TUI | `live_tui/` | Included without secrets |
| Full raw logs | Not included | Generated locally when running experiments |
| API credentials | Not included | Supplied locally through `live_tui/.env` |
