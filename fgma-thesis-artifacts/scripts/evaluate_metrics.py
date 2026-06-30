import argparse
from pathlib import Path

import pandas as pd


def summarize(input_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    required = {
        "condition",
        "correction_success",
        "repeated_error",
        "memory_recall",
        "latency_ms",
        "token_count",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    grouped = (
        df.groupby("condition", as_index=False)
        .agg(
            n=("condition", "size"),
            correction_success_rate=("correction_success", "mean"),
            repeated_error_rate=("repeated_error", "mean"),
            memory_recall_rate=("memory_recall", "mean"),
            mean_latency_ms=("latency_ms", "mean"),
            mean_token_count=("token_count", "mean"),
        )
        .sort_values("condition")
    )
    return grouped


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute FGMA condition-level summary metrics.")
    parser.add_argument("--input", required=True, type=Path, help="Input dialogue CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Output summary CSV.")
    args = parser.parse_args()

    summary = summarize(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
