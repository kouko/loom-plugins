# concern: duplicate YAML verdict keys can conceal a review that says NEEDS_REVISION.
"""Reject an outside review whose raw YAML gives two conflicting verdicts."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code/scripts"))
from loom_checker.reviewers import attach_outside_receipt  # noqa: E402


def test_receipt_duplicate_rejected() -> None:
    """A later PASS must not erase an earlier NEEDS_REVISION in raw output."""
    target = "b" * 40
    raw = (
        "verdict: NEEDS_REVISION\n"
        "verdict: PASS\n"
        "lens: plan\n"
        f"reviewed_sha: {'a' * 40}\n"
        f"review_target_sha: {target}\n"
        "dimension_scores:\n"
        "  deletion-first: PASS\n"
        "findings: []\n"
        "notes: []\n"
    )
    fields = yaml.safe_load(raw)
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
            "review_output": raw,
        },
    }
    incumbent = {"reviewer": "native", "vendor": "openai", "lens": "plan"}

    _, failure = attach_outside_receipt([incumbent, outside], "anthropic", target)

    assert failure is not None, "conflicting raw verdicts were accepted as PASS"
