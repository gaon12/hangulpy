"""Run Mintlify validate with an isolated temporary home directory."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MINT_PACKAGE = "mint@4.2.787"


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    docs_root = project_root / "docs"
    npx = shutil.which("npx") or shutil.which("npx.cmd")

    if not npx:
        raise RuntimeError("npx executable not found")

    isolated_home = tempfile.mkdtemp(prefix="hangulpy-mintlify-")
    env = os.environ.copy()
    env["HOME"] = isolated_home
    env["USERPROFILE"] = isolated_home

    command = [npx, "--yes", MINT_PACKAGE, "validate", *sys.argv[1:]]
    try:
        return subprocess.run(command, cwd=docs_root, env=env).returncode
    finally:
        shutil.rmtree(isolated_home, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
