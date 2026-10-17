# concern: a bun probe command must run the committed artifact, not a same-named file outside the repository.
"""Refuse a `bun test` absolute path that only ends with the artifact's path."""

from __future__ import annotations

import tempfile
from pathlib import Path

from loom_checker.attestation import adversarial_route

REPO = Path(__file__).resolve().parents[2]

ARTIFACT = "docs/loom/2026-10-16-accept-non-python-probes/evidence/probes/x.test.ts"


def test_bun_route_absolute_path_outside_repo_not_parsed() -> None:
    """An absolute bun target in another directory runs a file the attestation never bound."""
    elsewhere = Path(tempfile.gettempdir()) / "other-checkout" / ARTIFACT
    route, _row = adversarial_route(f"bun test {elsewhere}", ARTIFACT, REPO)
    assert route != "parsed"


def test_bun_route_absolute_path_inside_repo_parsed() -> None:
    """The artifact's own absolute path in this repository stays accepted."""
    route, _row = adversarial_route(f"bun test {REPO / ARTIFACT}", ARTIFACT, REPO)
    assert route == "parsed"
