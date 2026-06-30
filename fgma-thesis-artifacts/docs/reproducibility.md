# Reproducibility Checklist


## Safety

- No API keys or credentials.
- No account-specific values in scripts or configuration files.
- No local machine paths that are required for reproduction.
- No unapproved real-user data.

## Completeness

- README explains the project and the scope of the artifact package.
- Dependencies are listed in `requirements.txt` or `environment.yml`.
- Experiment conditions are documented in `configs/`.
- Sample data can run at least one end-to-end script.
- Result tables match the thesis table labels.
- Figure scripts can regenerate the included figures.

## Thesis Alignment

- Raw dialogue rows and evaluated follow-up turns are distinguished.
- Metric definitions match the thesis.
- Model labels match the thesis-facing labels.
