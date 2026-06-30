import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an example FGMA condition comparison figure.")
    parser.add_argument("--input", required=True, type=Path, help="Input metric summary CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    required = {"condition", "correction_success_rate", "repeated_error_rate"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    x = range(len(df))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar([i - width / 2 for i in x], df["correction_success_rate"], width, label="Correction success")
    ax.bar([i + width / 2 for i in x], df["repeated_error_rate"], width, label="Repeated error")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["condition"])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Rate")
    ax.set_title("Example FGMA Condition Comparison")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=200)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
