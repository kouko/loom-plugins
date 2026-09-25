"""Put the repository's `scripts/` on the import path.

The repository-level tests live here, apart from the scripts they test, and
several import those scripts by bare module name (`import sync_codex_manifests`).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
