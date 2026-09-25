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
AGENTS = ("implementer", "reviewer", "adversary", "acceptance-tester")
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


def test_role_dispatch_checks_accept_self_and_reject_plugin_typename() -> None:
    good = "| `reviewer` | `self` | `<loom-code>/agents/reviewer.md` |"
    assert _role_dispatch_ok(good, "reviewer")
    assert not _role_dispatch_ok("| `reviewer` | `self` |", "reviewer")
    assert _plugin_agent_typenames('Use `TypeName: "reviewer"`.') == ["reviewer"]
    assert _plugin_agent_typenames("`TypeName` `acceptance-tester`") == ["acceptance-tester"]
    assert _plugin_agent_typenames("`TypeName` (required), for example `reviewer`.") == ["reviewer"]
    assert _plugin_agent_typenames(f"Use `{SELF_TYPENAME}`. The `reviewer` reads.") == []


WRITE_PLAN_VENDOR = PLUGIN / "skills" / "write-plan" / "references" / "second-vendor-ask-and-docs-lint.md"
FIXED_CLI_BLOCKER = (
    "A fixed CLI or an accepted `ask` answer cannot run on Antigravity CLI, "
    "so Closing Review follows the existing review failure behavior: it "
    "reports the blocker and never silently drops the second vendor."
)


def _h2(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"section {heading!r} missing"
    return _flat(match.group(0))


def test_agy_fixed_cli_reports_blocker_not_silent_drop() -> None:
    agy = _h2(REFERENCE.read_text(encoding="utf-8"), "Second vendor")
    fixed = _h2(WRITE_PLAN_VENDOR.read_text(encoding="utf-8"), "Fixed CLI")
    assert FIXED_CLI_BLOCKER in agy
    assert FIXED_CLI_BLOCKER in fixed
    assert "`suggest` and a declined `ask` continue without a second vendor" in agy
    assert "continue the review without one" not in agy


def test_agy_model_fallback_records_host_default_unverified() -> None:
    section = _h2(REFERENCE.read_text(encoding="utf-8"), "Model and effort overrides")
    assert "`host-default/unverified`" in section
    assert "effort inheritance is unverified on agy 1.2.2" in section
    assert "profile as `inherited`" not in section
