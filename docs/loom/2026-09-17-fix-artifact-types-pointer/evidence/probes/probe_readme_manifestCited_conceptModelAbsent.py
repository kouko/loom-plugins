"""Adversarial probe: README cites manifest.yaml artifact_types, not the concept model.

Run from the repository root: python3 <this file>. Exit 1 on failure.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
README = ROOT / "docs/loom/README.md"


def test_readme_manifestCited_conceptModelAbsent() -> None:
    """README names manifest.yaml artifact_types as the mapping source, not the concept model."""
    text = README.read_text(encoding="utf-8")
    assert "loom-code/contract/manifest.yaml" in text, (
        "README does not name manifest.yaml as the mapping source"
    )
    assert "artifact_types" in text, (
        "README does not name artifact_types"
    )
    assert "concept model" not in text, (
        "README still cites the concept model for the artifact-type mapping"
    )


if __name__ == "__main__":
    try:
        test_readme_manifestCited_conceptModelAbsent()
    except AssertionError as exc:
        print("RED:", exc)
        sys.exit(1)
    print("GREEN")
    sys.exit(0)
