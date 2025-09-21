"""Run Tesseract OCR on CRF page images and emit structured JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pytesseract
from PIL import Image


DEFAULT_LANG = "eng"


def ocr_image(path: Path, lang: str = DEFAULT_LANG) -> str:
    with Image.open(path) as img:
        return pytesseract.image_to_string(img, lang=lang)


def run_batch(images: Iterable[Path], lang: str = DEFAULT_LANG) -> list[dict[str, str]]:
    output = []
    for image in images:
        text = ocr_image(image, lang=lang)
        output.append({"image": image.as_posix(), "text": text})
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path, help="List of page images to process")
    parser.add_argument("--lang", default=DEFAULT_LANG, help="Language to pass to Tesseract")
    parser.add_argument("--output", type=Path, default=Path("data/qc_output/ocr_text.json"), help="Destination JSON file")
    args = parser.parse_args()

    results = run_batch(args.images, lang=args.lang)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote OCR results for {len(results)} pages to {args.output}")


if __name__ == "__main__":
    main()
