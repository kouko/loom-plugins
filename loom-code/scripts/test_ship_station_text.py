"""Ship station text: the PR title rule lives where the title is written.

The `<title>` passed to `publish` becomes the squash-merge commit, so ship
§3 affirms that its Conventional Commits type equals the branch `<type>/`
prefix -- an agent at ship never reads write-plan Step 6.
"""
from __future__ import annotations

import re
from pathlib import Path

from prose_pin import has_negation

SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"section {heading!r} missing"
    return match.group(0)


def test_ship_publish_title_type_equals_branch_type() -> None:
    section = _section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once")
    flat = " ".join(section.split())
    sentences = re.split(r"(?<=[.!?])\s+", flat)
    hits = [
        s for s in sentences
        if "`<title>`" in s and "Conventional Commits subject" in s
        and "type" in s and "`<type>/`" in s and "branch" in s
        and "squash-merge commit" in s and not has_negation(s)
    ]
    assert len(hits) == 1, (
        "ship §3 needs one affirmative sentence: the `<title>` is a Conventional "
        "Commits subject whose type equals the branch `<type>/` prefix, because "
        "it becomes the squash-merge commit"
    )


LAND_COMMAND = (
    "cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py "
    "land --accepted-by <name>"
)


# ship-text-runs-land-after-acceptance (A1 positive)
def test_ship_text_runs_land_after_acceptance() -> None:
    text = SHIP.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert LAND_COMMAND in text
    assert "decision point ③" in flat
    assert "blind-run report" in flat
    assert "`next:`" in flat and "starts with the `cd`" in flat
    assert "`land --cleanup <branch>`" in flat
    assert "`land --sweep`" in flat
    assert "`--sweep --confirm <token>`" in flat
    confirm = [
        s for s in re.split(r"(?<=[.!?])\s+", flat)
        if "`--sweep --confirm <token>`" in s and "answers yes" in s
    ]
    assert len(confirm) == 1, "the sweep token is passed only after the maintainer answers yes"
    handoff = " ".join(_section(text, "## Handoff").split())
    assert "land" in handoff and "output" in handoff


# ship-text-separates-authorization-from-acceptance
def test_ship_text_separates_authorization_from_acceptance() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert not re.search(r"^## 1\. Confirm acceptance$", text, re.M)
    assert re.search(r"^## 1\. Confirm publication authorization$", text, re.M)
    land = " ".join(_section(text, "## 5. Land after acceptance").split())
    assert (
        "Publication authorization, including `publication: automatic`, is not "
        "acceptance; always present the result and ask at decision point ③ "
        "before running land."
    ) in land


# ship-text-has-no-direct-gh-pr-merge (A1 negative)
def test_ship_text_has_no_direct_gh_pr_merge() -> None:
    flat = " ".join(SHIP.read_text(encoding="utf-8").split())
    assert not re.search(r"gh pr merge\s+[<0-9-]", flat), "no gh pr merge command form"
    for sentence in re.split(r"(?<=[.!?])\s+", flat):
        if "gh pr merge" in sentence:
            assert has_negation(sentence), f"affirmative merge instruction: {sentence}"


# ship-text-keeps-no-worktree-instruction (A11 negative)
def test_ship_text_keeps_no_worktree_instruction() -> None:
    text = SHIP.read_text(encoding="utf-8").lower()
    assert "keep the worktree" not in " ".join(text.split())


GATE_OPEN_RE = re.compile(r"<!--\s*gate:\s*[A-Za-z0-9._-]+\s*-->")
GATE_CLOSE = "<!-- /gate -->"
NO_HANDOVER = "hand a refused publication command to the user to run"


def _gate_regions(text: str) -> list[tuple[int, int]]:
    """Offsets of every `<!-- gate: id -->` ... `<!-- /gate -->` span."""
    regions = []
    for match in GATE_OPEN_RE.finditer(text):
        close = text.find(GATE_CLOSE, match.end())
        end = len(text) if close == -1 else close + len(GATE_CLOSE)
        regions.append((match.start(), end))
    return regions


# ship-prose-forbids-handing-the-command-over (A3 positive)
def test_ship_prose_forbids_handing_the_command_over() -> None:
    section = _section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once")
    flat = " ".join(section.split())
    hits = [
        s for s in re.split(r"(?<=[.!?])\s+", flat)
        if NO_HANDOVER in s
        and "closing-review station" in s
        and "step selection" in s
        and "typing the code" in s
    ]
    assert len(hits) == 1, (
        "ship §3 needs one sentence forbidding a refused publication command "
        "from being handed to the user, and naming both legal routes: run the "
        "closing-review station, or propose a step selection the user confirms "
        "by typing the code"
    )


# ship-prose-rule-is-not-marked-as-a-gate (A3 negative)
def test_ship_prose_rule_is_not_marked_as_a_gate() -> None:
    text = SHIP.read_text(encoding="utf-8")
    index = text.find(NO_HANDOVER)
    assert index != -1, "the no-handover rule is missing from the ship station"
    for start, end in _gate_regions(text):
        assert not start <= index < end, (
            "PRINCIPLES.md forbids prose-only gates: the no-handover rule is "
            "advisory prose, and the enforceable carrier is the checker's "
            "missing-attestation refusal string"
        )
