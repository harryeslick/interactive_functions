#!/usr/bin/env bash
set -euo pipefail

# Build wheel and place it under docs/assets/wheels for Pyodide micropip
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

mkdir -p docs/assets/wheels

# Build wheel using uv/hatchling
echo "Building wheel..." >&2
uv build --wheel

# Locate the latest built wheel (uv may place it in a parent dist)
echo "Locating built wheel..." >&2
WHEEL_PATH=$(python - <<'PY'
import glob, os, sys
candidates = []
for base in ("dist", "../dist", "../../dist"):
		pattern = os.path.join(base, "interactive_functions-*.whl")
		matches = glob.glob(pattern)
		matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
		candidates.extend(matches)
print(candidates[0] if candidates else "")
PY
)

if [ -z "${WHEEL_PATH}" ] || [ ! -f "${WHEEL_PATH}" ]; then
	echo "ERROR: Could not find built wheel. Looked in dist/, ../dist, ../../dist" >&2
	exit 1
fi

echo "Using wheel: ${WHEEL_PATH}" >&2
cp "${WHEEL_PATH}" docs/assets/wheels/interactive_functions-latest-py3-none-any.whl

# Export marimo notebooks to html-wasm
python -m marimo export html-wasm dispersal_kernels_marimo.py -o dispersal_kernels_marimo.html
# python -m marimo export html-wasm docs/notebooks/diminishing_returns.py -o docs/notebooks/diminishing_returns.html

echo "Exported notebooks and prepared wheel at docs/assets/wheels/interactive_functions-latest-py3-none-any.whl"
