"""W2-04 -- one Antigravity CLI (agy) tool-and-dispatch mapping reference.

Positive (stations-reference-agy-tool-mapping): build, closing-review and
write-plan each carry an affirmative pointer to
``loom-code/references/antigravity-tools.md``, the relative link resolves,
and the reference names the agy tools the stations need plus every
loom-code agent.

Negative (mapping-names-no-claude-only-tool): outside an explicit Claude Code
label, the reference never presents a Claude-only tool name as something to
call; in the mapping table the Antigravity CLI column carries none of them.
"""
from __future__ import annotations

import re
from pathlib import Path

from prose_pin import has_negation

PLUGIN = Path(__file__).resolve().parents[1]
REFERENCE = PLUGIN / "references" / "antigravity-tools.md"
LINK = "../../references/antigravity-tools.md"
STATIONS = ("build", "closing-review", "write-plan")
AGENTS = ("implementer", "reviewer", "adversary", "blind-runner")
AGY_TOOLS = ("invoke_subagent", "ask_question", "run_command")
CLAUDE_ONLY = ("Agent", "Task", "AskUserQuestion", "Bash", "Read", "Edit", "Write", "Skill")
AGY_HEADER = "Antigravity CLI"
CLAUDE_LABEL = "Claude Code"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", _flat(text))


def _pointer_ok(sentence: str) -> bool:
    """Affirmative prose pin: a map verb precedes the link, no negation."""
    if LINK not in sentence or has_negation(sentence):
        return False
    return re.search(r"\bmap\b", sentence[: sentence.index(LINK)], re.I) is not None


def _claude_only_violations(text: str) -> list[str]:
    """Claude-only tool names presented outside a Claude Code label.

    Table rows: the cell under the ``Antigravity CLI`` header must not name
    one. Prose: a sentence naming one in backticks must carry the
    ``Claude Code`` label.
    """
    found: list[str] = []
    agy_col = None
    prose: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if AGY_HEADER in cells:
                agy_col = cells.index(AGY_HEADER)
                continue
            if agy_col is not None and agy_col < len(cells):
                cell = cells[agy_col]
                for name in CLAUDE_ONLY:
                    if re.search(rf"`{name}`|\b{name}\b", cell):
                        found.append(f"agy column: {cell}")
            continue
        agy_col = None if not line.strip() else agy_col
        prose.append(line)
    for sentence in _sentences("\n".join(prose)):
        for name in CLAUDE_ONLY:
            if f"`{name}`" in sentence and CLAUDE_LABEL not in sentence:
                found.append(f"prose: {sentence}")
    return found


def test_each_station_points_to_the_reference_and_link_resolves() -> None:
    for station in STATIONS:
        skill = PLUGIN / "skills" / station / "SKILL.md"
        sentences = [s for s in _sentences(skill.read_text(encoding="utf-8")) if LINK in s]
        assert any(_pointer_ok(s) for s in sentences), f"{station}: no affirmative pointer"
        assert (skill.parent / LINK).resolve() == REFERENCE.resolve()
        assert REFERENCE.is_file()


def test_reference_names_agy_tools_and_every_loom_agent() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    for tool in AGY_TOOLS:
        assert f"`{tool}`" in text, tool
    for agent in AGENTS:
        assert f"`{agent}`" in text, agent
        assert (PLUGIN / "agents" / f"{agent}.md").is_file()


def test_reference_names_no_claude_only_tool_for_agy() -> None:
    assert _claude_only_violations(REFERENCE.read_text(encoding="utf-8")) == []


# Synthetic self-tests: the checks accept a good example and reject a bad one.


def test_pointer_pin_accepts_affirmative_and_rejects_negated() -> None:
    assert _pointer_ok(f"On Antigravity CLI, map tool and agent names with `{LINK}`.")
    assert not _pointer_ok(f"On Antigravity CLI, do not map tool names with `{LINK}`.")


def test_violation_check_rejects_claude_tool_in_agy_column_and_prose() -> None:
    bad = (
        "| Concept | Claude Code | Antigravity CLI |\n"
        "|---|---|---|\n"
        "| Shell | `Bash` | `Bash` |\n"
        "\n"
        "On agy, call `AskUserQuestion` to ask.\n"
    )
    assert len(_claude_only_violations(bad)) == 2
    good = (
        "| Concept | Claude Code | Antigravity CLI |\n"
        "|---|---|---|\n"
        "| Shell | `Bash` | `run_command` |\n"
        "\n"
        "Claude Code: `AskUserQuestion`; agy: `ask_question`.\n"
    )
    assert _claude_only_violations(good) == []
