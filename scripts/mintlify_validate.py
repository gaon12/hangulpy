"""Run Mintlify validate with an isolated temporary home directory."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    isolated_home = tempfile.mkdtemp(prefix="hangulpy-mintlify-")
    npx = shutil.which("npx") or shutil.which("npx.cmd")

    if not npx:
        raise RuntimeError("npx executable not found")

    env = os.environ.copy()
    env["HOME"] = isolated_home
    env["USERPROFILE"] = isolated_home

    command = [npx, "mint", "validate", *sys.argv[1:]]
    return subprocess.run(command, cwd=project_root, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
