"""loom-workflow runtime prose must not route to a loom-code skill that no
longer exists.

The loom 1.0 cutover removed `brainstorming`, `writing-plans`,
`finishing-a-development-branch` and `dispatching-parallel-agents`. The files
below named them (rule-text consolidation audit, C19). A `loom-code:<name>`
is live only when `loom-code/skills/<name>/` exists; the retired names are
also rejected bare, because a bare backticked name reads as a skill too.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOOM_CODE_SKILLS = REPO_ROOT / "loom-code" / "skills"

SCANNED = (
    "loom-workflow/skills/git-memory/protocols/recall.md",
    "loom-workflow/skills/git-memory/protocols/compose-commit.md",
    "loom-workflow/skills/distill-sessions/agents/prompt-failure-analysis.md",
    "loom-workflow/skills/distill-sessions/agents/prompt-success-analysis.md",
)

# Host maps and READMEs name skills in plain prose and sample output, so a
# retired name is rejected there even without backticks. Scoped to these
# files: elsewhere "brainstorming" is an ordinary English word.
SCANNED_UNQUOTED = (
    "loom-workflow/skills/distill-sessions/references/claude-code-tools.md",
    "loom-workflow/skills/distill-sessions/references/codex-tools.md",
    "loom-workflow/skills/distill-sessions/README.md",
    "loom-workflow/skills/distill-sessions/README.ja.md",
    "loom-workflow/skills/distill-sessions/README.zh-TW.md",
)

RETIRED = (
    "brainstorming",
    "writing-plans",
    "finishing-a-development-branch",
    "dispatching-parallel-agents",
)

_QUALIFIED = re.compile(r"loom-code:([a-z][a-z0-9-]*)")
_BARE = re.compile(r"`(" + "|".join(map(re.escape, RETIRED)) + r")`")
_UNQUOTED = re.compile(
    r"(?<![\w:`-])(" + "|".join(map(re.escape, RETIRED)) + r")(?![\w`-])"
)


def find_retired_names(text: str, live: set[str], unquoted: bool = False) -> list[str]:
    hits = [m.group(0) for m in _QUALIFIED.finditer(text) if m.group(1) not in live]
    hits += [m.group(1) for m in _BARE.finditer(text)]
    if unquoted:
        hits += [m.group(1) for m in _UNQUOTED.finditer(text)]
    return hits


def _live_skills() -> set[str]:
    return {p.name for p in LOOM_CODE_SKILLS.iterdir() if (p / "SKILL.md").is_file()}


def test_no_retired_loom_code_skill_names() -> None:
    live = _live_skills()
    assert "write-plan" in live and "ship" in live, sorted(live)
    hits = {
        rel: found
        for rel in SCANNED
        if (found := find_retired_names((REPO_ROOT / rel).read_text(encoding="utf-8"), live))
    }
    assert not hits, f"retired loom-code skill names still named: {hits}"


def test_distill_sessions_docs_free_of_retired_names() -> None:
    live = _live_skills()
    hits = {
        rel: found
        for rel in SCANNED_UNQUOTED
        if (
            found := find_retired_names(
                (REPO_ROOT / rel).read_text(encoding="utf-8"), live, unquoted=True
            )
        )
    }
    assert not hits, f"retired loom-code skill names still named: {hits}"


def test_retired_name_in_reference_flagged() -> None:
    live = {"write-plan", "build"}
    assert find_retired_names(
        "sessions invoking brainstorming + writing-plans; via "
        "loom-code:dispatching-parallel-agents",
        live,
        unquoted=True,
    ) == ["loom-code:dispatching-parallel-agents", "brainstorming", "writing-plans"]
    assert find_retired_names("e.g. write-plan + build", live, unquoted=True) == []


def test_scanner_rejects_retired_names_and_keeps_live_ones() -> None:
    live = {"write-plan", "ship"}
    assert find_retired_names(
        "If `loom-code:brainstorming` or `writing-plans` is running", live
    ) == ["loom-code:brainstorming", "writing-plans"]
    assert find_retired_names("When `loom-code:ship` delegates this protocol", live) == []
