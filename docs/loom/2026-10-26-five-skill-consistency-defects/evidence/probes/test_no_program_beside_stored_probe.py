# concern: a no-program record lets finalize-review attest a change whose store still holds an unexecuted (even RED) adversarial program.
"""Adversarial probe for change 2026-10-26-five-skill-consistency-defects.

The no-program record means "the adversary committed no program". When the
change's probe store holds a committed program, that record contradicts the
tree, and accepting it silently drops the program from execution.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))
sys.path.insert(0, str(ROOT / "loom-code" / "tests"))

from test_selection_finalize import (  # noqa: E402
    ADVERSARIAL, CHANGE, PASSING, commit_all, finalize, make_repo, review_input,
    no_host_session, validate, write_probes, written,
)

__all__ = ["no_host_session"]  # the autouse fixture applies to this module too

NO_PROGRAM = {"no_program": "no attack succeeded and no repository test covers it"}


def test_finalizeReview_noProgramBesideStoredRedProbe_refused(tmp_path: Path) -> None:
    """finalize-review refuses a no-program record while the store holds a RED program."""
    repo = make_repo(tmp_path)
    probes = repo / f"docs/loom/{CHANGE}/evidence/probes"
    probes.mkdir(parents=True)
    (probes / "test_pinned_defect.py").write_text(
        "# concern: a pinned defect Build never fixed\n"
        "def test_product_defect_red():\n    assert False\n", encoding="utf-8")
    commit_all(repo, "red probe")

    result = finalize(repo, review_input(tmp_path, PASSING, [NO_PROGRAM]))

    assert result.returncode == 1, "finalize-review attested a no-program record beside a stored RED probe"
    assert "BLOCK finalize.adversarial" in result.stderr


def test_validateAttestation_noProgramBesideStoredProbe_refused(tmp_path: Path) -> None:
    """The attestation validator refuses a no-program row when the store holds a program."""
    repo = make_repo(tmp_path)
    write_probes(repo, 1)
    accepted = finalize(repo, review_input(tmp_path, PASSING, ADVERSARIAL))
    assert accepted.returncode == 0, accepted.stderr
    attestation = written(repo)
    attestation["executions"] = [
        row for row in attestation["executions"] if row["kind"] != "adversarial"
    ] + [{"kind": "adversarial", **NO_PROGRAM}]

    assert validate(repo, attestation) != [], "validator accepted a no-program row beside a stored probe"
