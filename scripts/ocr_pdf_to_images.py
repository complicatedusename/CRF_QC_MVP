"""Convert PDF CRF scans into per-page PNG images for Label Studio."""
from __future__ import annotations

import argparse
from pathlib import Path

import pdfplumber


def export_pages(pdf_path: Path, destination: Path, dpi: int = 200) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    with pdfplumber.open(pdf_path) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            im = page.to_image(resolution=dpi)
            out_path = destination / f"{pdf_path.stem}_page_{index:02d}.png"
            im.save(out_path, format="PNG")
            output_paths.append(out_path)
    return output_paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("--output", type=Path, default=Path("data/scans"), help="Folder to write page images")
    parser.add_argument("--dpi", type=int, default=200, help="Resolution used for rendering each page")
    args = parser.parse_args()

    images = export_pages(args.pdf, args.output, dpi=args.dpi)
    for path in images:
        print(path)


if __name__ == "__main__":
    main()
