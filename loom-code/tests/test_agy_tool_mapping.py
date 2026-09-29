"""W2-04 -- one Antigravity CLI (agy) tool-and-dispatch mapping reference.

Positive (stations-reference-agy-tool-mapping): the relative link from
build, closing-review and write-plan to
``loom-code/references/antigravity-tools.md`` resolves, and the reference
dispatches every loom-code role as the ``self`` subagent reading its
contract.

Negative (mapping-names-no-claude-only-tool): outside an explicit Claude Code
label, the reference never presents a Claude-only tool name as something to
call; in the mapping table the Antigravity CLI column carries none of them.
"""
from __future__ import annotations

import re
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
REFERENCE = PLUGIN / "references" / "antigravity-tools.md"
LINK = "../../references/antigravity-tools.md"
STATIONS = ("build", "closing-review", "write-plan")
AGENTS = ("implementer", "reviewer", "adversary", "acceptance-tester")
CLAUDE_ONLY = ("Agent", "Task", "AskUserQuestion", "Bash", "Read", "Edit", "Write", "Skill")
AGY_HEADER = "Antigravity CLI"
CLAUDE_LABEL = "Claude Code"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", _flat(text))


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
        assert (skill.parent / LINK).resolve() == REFERENCE.resolve()
        assert REFERENCE.is_file()


def test_reference_names_no_claude_only_tool_for_agy() -> None:
    assert _claude_only_violations(REFERENCE.read_text(encoding="utf-8")) == []


SELF_TYPENAME = 'TypeName: "self"'


def _role_dispatch_ok(text: str, role: str) -> bool:
    """A line routes ``role`` to the ``self`` subagent reading its contract."""
    contract = f"<loom-code>/agents/{role}.md"
    return any(
        f"`{role}`" in line and "`self`" in line and contract in line
        for line in text.splitlines()
    )


def _plugin_agent_typenames(text: str) -> list[str]:
    """Places that hand a loom plugin agent name to agy as a TypeName.

    A unit is a table row or a prose sentence; one that names ``TypeName``
    and a loom agent (quoted or in backticks) is a violation.
    """
    units: list[str] = []
    prose: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            units.append(line)
        else:
            prose.append(line)
    units += _sentences("\n".join(prose))
    found: list[str] = []
    for unit in units:
        if "TypeName" not in unit:
            continue
        for agent in AGENTS:
            if re.search(rf"[`\"']{re.escape(agent)}[`\"']", unit):
                found.append(agent)
    return found


def test_reference_dispatches_every_role_as_self_reading_its_contract() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    assert SELF_TYPENAME in text
    for role in AGENTS:
        assert _role_dispatch_ok(text, role), role


def test_reference_never_invokes_a_plugin_agent_as_typename() -> None:
    assert _plugin_agent_typenames(REFERENCE.read_text(encoding="utf-8")) == []


# Synthetic self-tests: the checks accept a good example and reject a bad one.


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


def test_role_dispatch_checks_accept_self_and_reject_plugin_typename() -> None:
    good = "| `reviewer` | `self` | `<loom-code>/agents/reviewer.md` |"
    assert _role_dispatch_ok(good, "reviewer")
    assert not _role_dispatch_ok("| `reviewer` | `self` |", "reviewer")
    assert _plugin_agent_typenames('Use `TypeName: "reviewer"`.') == ["reviewer"]
    assert _plugin_agent_typenames("`TypeName` `acceptance-tester`") == ["acceptance-tester"]
    assert _plugin_agent_typenames("`TypeName` (required), for example `reviewer`.") == ["reviewer"]
    assert _plugin_agent_typenames(f"Use `{SELF_TYPENAME}`. The `reviewer` reads.") == []


# OpenCode v2 mapping reference (W1-02).

OPENCODE = PLUGIN / "references" / "opencode-tools.md"
OPENCODE_LINK = "../../references/opencode-tools.md"


def test_stations_link_opencode_reference() -> None:
    for station in STATIONS:
        skill = PLUGIN / "skills" / station / "SKILL.md"
        assert OPENCODE_LINK in skill.read_text(encoding="utf-8"), station
        assert (skill.parent / OPENCODE_LINK).resolve() == OPENCODE.resolve()


def test_opencode_reference_maps_subagent_agent_ids() -> None:
    text = OPENCODE.read_text(encoding="utf-8")
    assert "`subagent`" in text and "`agent`" in text
    for role in AGENTS:
        assert f"`loom-code:{role}`" in text, role


def test_opencode_reference_never_tells_agent_to_pass_subagent_type() -> None:
    assert "subagent_type" not in OPENCODE.read_text(encoding="utf-8")
