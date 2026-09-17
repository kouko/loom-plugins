"""Adversarial probe: manifest.yaml exists and declares artifact_types.

Run from the repository root: python3 <this file>. Exit 1 on failure.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
MANIFEST = ROOT / "loom-code/contract/manifest.yaml"


def test_manifest_artifactTypes_declared() -> None:
    """manifest.yaml exists and declares the artifact_types mapping."""
    assert MANIFEST.is_file(), "manifest.yaml does not exist"
    text = MANIFEST.read_text(encoding="utf-8")
    assert "artifact_types:" in text, "manifest.yaml does not declare artifact_types"


if __name__ == "__main__":
    try:
        test_manifest_artifactTypes_declared()
    except AssertionError as exc:
        print("RED:", exc)
        sys.exit(1)
    print("GREEN")
    sys.exit(0)
