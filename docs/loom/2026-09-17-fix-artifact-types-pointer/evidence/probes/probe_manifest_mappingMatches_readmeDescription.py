"""Adversarial probe: manifest.yaml's artifact_types matches what the README describes.

The README describes four types: intent, evidence, memory, maps.
The manifest should declare all four. The current manifest has no
`memory` mapping, so this probe fails — the README describes a
mapping the manifest does not declare.

Run from the repository root: python3 <this file>. Exit 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path.cwd()
MANIFEST = ROOT / "loom-code/contract/manifest.yaml"

# The README describes these four types:
# `docs/loom/intent/**` is intent, `**/evidence/**` is evidence,
# `docs/loom/memory/**` is memory, `docs/loom/maps/**` is map.
README_TYPES = {
    "intent": "docs/loom/intent/**",
    "evidence": "**/evidence/**",
    "memory": "docs/loom/memory/**",
    "map": "docs/loom/maps/**",
}


def _parse_manifest(text: str) -> dict[str, str]:
    """Parse artifact_types from manifest.yaml text. Returns {glob: type}."""
    result: dict[str, str] = {}
    in_artifact_types = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("artifact_types:"):
            in_artifact_types = True
            continue
        if in_artifact_types:
            m = re.match(r'\s*-\s*\{glob:\s*"([^"]+)",\s*type:\s*(\w+)', line)
            if m:
                result[m.group(1)] = m.group(2)
            elif stripped and not stripped.startswith("#") and not stripped.startswith("- {glob:"):
                # End of artifact_types section (next top-level key)
                if not line.startswith(" ") and not line.startswith("\t"):
                    break
    return result


def test_manifest_mappingMatches_readmeDescription() -> None:
    """manifest.yaml declares the four artifact types the README describes."""
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    manifest_types = _parse_manifest(manifest_text)

    missing = []
    for kind, glob in README_TYPES.items():
        if glob not in manifest_types:
            missing.append(f"{kind}: {glob} (not in manifest)")
        elif manifest_types[glob] != kind:
            missing.append(
                f"{kind}: {glob} maps to {manifest_types[glob]}, not {kind}"
            )

    assert not missing, (
        "manifest.yaml missing README-described mappings: " + "; ".join(missing)
    )


if __name__ == "__main__":
    try:
        test_manifest_mappingMatches_readmeDescription()
    except AssertionError as exc:
        print("RED:", exc)
        sys.exit(1)
    print("GREEN")
    sys.exit(0)
