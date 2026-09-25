"""Put `loom-code/scripts/` on the import path.

loom-code's tests live here, apart from the scripts they test, and many import
those scripts by bare module name (`import repo_files`, `from loom_checker ...`).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
