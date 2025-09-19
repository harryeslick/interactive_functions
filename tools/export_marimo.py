"""Export all Marimo apps in docs/notebooks to HTML.

This script searches for Python files under docs/notebooks and runs:

    python -m marimo export <in.py> --to <out.html>

so MkDocs serves the fully rendered pages instead of placeholders.

Run locally before `mkdocs build`, or wire it into CI as a pre-build step.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def export_marimo_apps(root: Path) -> None:
    """Export all Marimo apps under docs/notebooks to HTML.

    Args:
        root: Project root directory (where mkdocs.yml lives).
    """
    notebooks_dir = root / "docs" / "notebooks"
    py_files = sorted(notebooks_dir.glob("*.py"))
    if not py_files:
        print("No .py files found under docs/notebooks; nothing to export.")
        return

    for in_file in py_files:
        out_file = in_file.with_suffix(".html")
        cmd = [
            "python",
            "-m",
            "marimo",
            "export",
            str(in_file),
            "--to",
            str(out_file),
        ]
        print(f"Exporting {in_file} -> {out_file}")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    export_marimo_apps(Path(__file__).resolve().parents[2])
