#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT="$PROJECT_ROOT"

CONFIG_FILE="$PROJECT_ROOT/label_studio/template_crf.xml"
PROJECT_DIR="$PROJECT_ROOT/label_studio"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Label Studio config missing at $CONFIG_FILE" >&2
  exit 1
fi

if ! command -v label-studio >/dev/null 2>&1; then
  echo "Label Studio is not installed. Run 'pip install -r requirements.txt' first." >&2
  exit 1
fi

label-studio start --project-name "CRF QC" --label-config "$CONFIG_FILE" --init --input-path "$PROJECT_DIR/sample_import.json"
