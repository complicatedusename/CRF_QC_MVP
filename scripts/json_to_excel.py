"""Convert Label Studio export JSON/JSONL into a structured Excel workbook."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_FIELDS = ["image_url", "draft_html", "checks"]


def load_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        records = json.loads(path.read_text(encoding="utf-8"))
    return records


def parse_annotation(record: dict[str, Any]) -> dict[str, Any]:
    data = record.get("data", {})
    for field in REQUIRED_FIELDS:
        if field not in data:
            raise KeyError(f"Missing '{field}' in record data")

    result = {
        "image_url": data["image_url"],
        "draft_html": data["draft_html"],
        "checks": "\n".join(data.get("checks", [])),
    }

    annotations = record.get("annotations") or record.get("completions") or record.get("predictions") or []
    if annotations:
        first = annotations[0]
        answers = first.get("result", [])
        for item in answers:
            if item.get("from_name") == "qc_result":
                result["qc_result"] = ", ".join(item.get("value", {}).get("choices", []))
            if item.get("from_name") == "qc_notes":
                result["qc_notes"] = "\n".join(item.get("value", {}).get("text", []))
    return result


def export(records: list[dict[str, Any]], destination: Path) -> None:
    rows = [parse_annotation(record) for record in records]
    df = pd.DataFrame(rows)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(destination, index=False)
    print(f"Wrote {len(df)} rows to {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Label Studio JSON or JSONL export file")
    parser.add_argument("output", type=Path, default=Path("output/crf_final.xlsx"), nargs="?", help="Destination Excel file")
    args = parser.parse_args()

    records = load_records(args.input)
    export(records, args.output)


if __name__ == "__main__":
    main()
