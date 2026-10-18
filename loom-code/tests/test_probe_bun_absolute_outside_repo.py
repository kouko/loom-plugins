# concern: a bun probe command must run the committed artifact by its repo-relative `./` path, never an absolute path that names one checkout.
"""Refuse any absolute `bun test` target; accept only `bun test ./<A>`."""

from __future__ import annotations

import tempfile
from pathlib import Path

from loom_checker.attestation import adversarial_route

REPO = Path(__file__).resolve().parents[2]

ARTIFACT = "docs/loom/2026-10-16-accept-non-python-probes/evidence/probes/x.test.ts"


def test_bun_route_absolute_path_outside_repo_refused() -> None:
    """An absolute bun target in another directory runs a file the attestation never bound."""
    elsewhere = Path(tempfile.gettempdir()) / "other-checkout" / ARTIFACT
    route, row = adversarial_route(f"bun test {elsewhere}", ARTIFACT, REPO)
    assert (route, row and row.name) == ("not-accepted", "bun")


def test_bun_route_absolute_path_inside_repo_refused() -> None:
    """Even this checkout's own absolute path cannot re-run from another checkout."""
    route, row = adversarial_route(f"bun test {REPO / ARTIFACT}", ARTIFACT, REPO)
    assert (route, row and row.name) == ("not-accepted", "bun")


def test_bun_route_dot_slash_relative_path_parsed() -> None:
    """The one accepted form, `bun test ./<A>`, still attests by parsed result."""
    route, row = adversarial_route(f"bun test ./{ARTIFACT}", ARTIFACT, REPO)
    assert (route, row and row.name) == ("parsed", "bun")
