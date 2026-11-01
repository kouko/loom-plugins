"""A publication-only Closing Review re-entry must continue to Ship."""

# concern: a matching attestation on re-entry can trigger a progress-only stop before Ship

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[5]
REVIEW = ROOT / "loom-code/skills/closing-review/SKILL.md"


def test_matching_attestation_reentry_calls_ship_in_same_turn() -> None:
    content = REVIEW.read_text(encoding="utf-8")
    entry = content.split("## 1. Establish the content", 1)[1].split(
        "## 2. Compute review depth", 1
    )[0]
    branch = re.search(
        r"If only publication metadata changed and a matching\s+"
        r"attestation already exists,.*?(?=\n\n|$)",
        entry,
        re.DOTALL,
    )
    assert branch, "matching-attestation re-entry route is missing"
    route = " ".join(branch.group(0).split())
    assert re.search(r"call `loom-code:ship` in (?:the|this) same turn", route), route
