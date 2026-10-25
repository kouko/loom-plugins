# concern: An explained PASS score must not conceal an explicit NEEDS_REVISION conclusion.
"""Reject a contradictory verdict token in an outside dimension score rationale."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from loom_checker.reviewers import attach_outside_receipt  # noqa: E402


def test_score_hidden_verdict_rejected() -> None:
    """A rationale that starts with a contrary score cannot certify PASS."""
    target = "b" * 40
    fields = {
        "verdict": "PASS",
        "lens": "plan",
        "reviewed_sha": "a" * 40,
        "review_target_sha": target,
        "dimension_scores": {
            "deletion-first": "PASS — NEEDS_REVISION: blocking issue",
        },
        "findings": [],
        "notes": [],
    }
    outside = {
        **fields,
        "reviewer": "outside",
        "vendor": "anthropic",
        "model": "sonnet",
        "external_review": {
            "status": "completed",
            "reason": None,
            "executor": "claude",
            "requested_model": "sonnet",
            "requested_effort": "high",
            "requested_family": "anthropic",
            "evidence_level": "accepted-explicit-settings",
            "observed_model": "claude-sonnet-4-5",
            "observed_effort": None,
            "review_output": yaml.safe_dump(fields),
        },
    }

    _, failure = attach_outside_receipt(
        [{"vendor": "openai", "lens": "plan"}, outside], "anthropic", target
    )

    assert failure is not None, "contradictory dimension score was accepted"
