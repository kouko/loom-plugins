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
