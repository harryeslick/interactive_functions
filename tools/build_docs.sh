#!/usr/bin/env bash
set -euo pipefail


# Export marimo notebooks to HTML, then build the site
repo_root="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/2] Exporting marimo apps to HTML..."
python "$repo_root/tools/export_marimo.py"

echo "[2/2] Building MkDocs site..."
mkdocs build

echo "Done: site/ updated."

