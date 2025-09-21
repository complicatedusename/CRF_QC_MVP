"""Utility for generating Label Studio JSON tasks for CRF QC."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def build_task(scan_path: Path, draft_path: Path, checklist: Iterable[str]) -> dict:
    """Build a task dictionary linking a scan image to a rendered draft."""
    draft_html = draft_path.read_text(encoding="utf-8")
    return {
        "data": {
            "image_url": scan_path.as_posix(),
            "draft_html": draft_html,
            "checks": list(checklist),
            "field_deltas": [["Field", "Scan Value", "Draft Value"]],
        }
    }


def discover_files(scan_dir: Path, draft_dir: Path) -> Iterable[tuple[Path, Path]]:
    scans = sorted(scan_dir.glob("*.png")) + sorted(scan_dir.glob("*.jpg"))
    if not scans:
        raise FileNotFoundError(f"No scan images found in {scan_dir}")

    for scan in scans:
        draft_name = scan.stem + ".html"
        draft = draft_dir / draft_name
        if not draft.exists():
            raise FileNotFoundError(f"Expected draft HTML for {scan.name} at {draft}")
        yield scan, draft


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Destination JSONL file")
    parser.add_argument("--scans", type=Path, default=Path("data/scans"), help="Directory containing scan images")
    parser.add_argument("--drafts", type=Path, default=Path("data/drafts"), help="Directory containing rendered HTML drafts")
    parser.add_argument("--checklist", type=Path, help="Optional file with newline separated checklist items")
    args = parser.parse_args()

    checklist_items: Iterable[str]
    if args.checklist:
        checklist_items = [line.strip() for line in args.checklist.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        checklist_items = [
            "Confirm participant identifiers match between scan and draft",
            "Verify visit date and investigator signature",
            "Ensure critical safety data (vitals, labs, AEs) is present",
        ]

    tasks = []
    for scan, draft in discover_files(args.scans, args.drafts):
        tasks.append(build_task(scan, draft, checklist_items))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fp:
        for task in tasks:
            fp.write(json.dumps(task, ensure_ascii=False) + "\n")

    print(f"Wrote {len(tasks)} tasks to {args.output}")


if __name__ == "__main__":
    main()
