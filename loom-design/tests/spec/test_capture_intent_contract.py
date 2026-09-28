"""capture-intent station contract (plan W2-01).

The station is loom-design's entry point. These tests check its structure:
frontmatter, word caps, gate markers and their registration, the shared
locate-loom-code link, resolving paths, absent deleted vocabulary, and the
two cross-plugin invariants: the `## Station summary` section is
byte-identical to loom-code's copy of it (a reader who lands on either
station sees the same whole-flow table), and the plugin declares the
contract version it needs. The station's rule wording is review-only.

Reading loom-code's file from a loom-design TEST is deliberate: the ban on
cross-plugin references is a RUNTIME portability rule for prose contracts
(a dispatched agent only has the repo it stands in). A test runs in this
repository, where both plugins are checked out side by side.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

SKILL = REPO / "loom-design/skills/capture-intent/SKILL.md"
WRITE_PLAN = REPO / "loom-code/skills/write-plan/SKILL.md"
WRITE_SPEC = REPO / "loom-design/skills/write-spec/SKILL.md"
TOOL_SKILLS = (
    REPO / "loom-design/skills/design-system/SKILL.md",
    REPO / "loom-design/skills/product-principles/SKILL.md",
    REPO / "loom-design/skills/architecture-design/SKILL.md",
)
STATION_TABLE_HEADER = "| station | artifact | who decides | checker | checkpoint |"
LOCATE_REFERENCE = REPO / "loom-design/skills/capture-intent/references/locate-loom-code.md"
LOCATE_LINKS = {
    SKILL: "references/locate-loom-code.md",
    WRITE_SPEC: "../capture-intent/references/locate-loom-code.md",
    TOOL_SKILLS[0]: "../capture-intent/references/locate-loom-code.md",
    TOOL_SKILLS[1]: "../capture-intent/references/locate-loom-code.md",
    TOOL_SKILLS[2]: "../capture-intent/references/locate-loom-code.md",
}
HOST_TABLE_HEADER = "| Where `loom-code` lives |"
CONTRACT_COMMAND = "python3 <loom-code>/scripts/loom_checker.py contract --require 2.1"
PLUGIN_JSON = REPO / "loom-design/.claude-plugin/plugin.json"
MECHANISMS = REPO / "docs/loom/evidence/mechanisms.yaml"

WORD_CAP = 3500
DESCRIPTION_CAP = 400

# Vocabulary the redesign deletes (concept-model §10). A station written
# after the cut must not reintroduce any of it.
DELETED_VOCABULARY = (
    "brief",
    "seed",
    "pipeline",
    "conductor",
    "on-ramp",
    "onramp",
    "reception",
    "critic",
    "batch",
    "waiver",
)

GATE_IDS = (
    "capture-intent.no-confirmed-without-restatement",
    "capture-intent.product-problem-plain-words",
)


def _text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _body(text: str) -> str:
    """The SKILL.md body, frontmatter stripped."""
    parts = text.split("---\n", 2)
    return parts[2] if len(parts) == 3 else text


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert m, f"section {heading!r} missing"
    return m.group(0)


def test_skill_file_exists() -> None:
    assert SKILL.is_file(), f"{SKILL} does not exist"


def test_frontmatter_name_and_version() -> None:
    text = _text()
    assert re.search(r"^name: capture-intent$", text, re.M)
    assert re.search(r"^version: 1\.0\.0$", text, re.M)


def test_description_within_cap() -> None:
    m = re.search(r"^description: \|\n((?:  .*\n)+)", _text(), re.M)
    assert m, "description must be a block scalar"
    description = " ".join(line.strip() for line in m.group(1).splitlines())
    assert len(description) <= DESCRIPTION_CAP, len(description)


def test_body_within_word_cap() -> None:
    words = len(_body(_text()).split())
    assert words <= WORD_CAP, words


def test_station_summary_is_byte_identical_to_write_plan() -> None:
    ours = _section(_text(), "## Station summary")
    theirs = _section(WRITE_PLAN.read_text(encoding="utf-8"), "## Station summary")
    assert ours == theirs


def test_station_summary_three_station_copies_byte_identical() -> None:
    ours = _section(_text(), "## Station summary")
    for station in (WRITE_SPEC, WRITE_PLAN):
        theirs = _section(station.read_text(encoding="utf-8"), "## Station summary")
        assert ours == theirs, station


def _carries_station_table(text: str) -> bool:
    return "## Station summary" in text or STATION_TABLE_HEADER in text


def test_tool_skills_carry_no_station_table() -> None:
    """The two tools are not stations; only the three stations carry the table."""
    for tool in TOOL_SKILLS:
        assert not _carries_station_table(tool.read_text(encoding="utf-8")), tool


def test_tool_skill_carries_station_table_is_caught() -> None:
    table = _section(_text(), "## Station summary")
    rows_only = table.split("\n", 1)[1]
    for tool in TOOL_SKILLS:
        text = tool.read_text(encoding="utf-8")
        assert _carries_station_table(text + "\n" + table), tool
        assert _carries_station_table(text + "\n" + rows_only), tool


def test_four_skills_link_one_locate_loom_code_reference() -> None:
    assert LOCATE_REFERENCE.is_file(), LOCATE_REFERENCE
    for skill_md, link in LOCATE_LINKS.items():
        text = skill_md.read_text(encoding="utf-8")
        step0 = _section(text, "## Step 0 — Check the contract version")
        assert f"`{link}`" in step0, skill_md
        assert CONTRACT_COMMAND in step0, skill_md
        assert (skill_md.parent / link).resolve() == LOCATE_REFERENCE.resolve()
        assert HOST_TABLE_HEADER not in text, skill_md
    carriers = sorted(
        path
        for path in (REPO / "loom-design/skills").rglob("*.md")
        if HOST_TABLE_HEADER in path.read_text(encoding="utf-8")
    )
    assert carriers == [LOCATE_REFERENCE]


def test_gate_markers_present() -> None:
    text = _text()
    for gate_id in GATE_IDS:
        assert f"<!-- gate: {gate_id} -->" in text, gate_id


def test_gate_markers_registered_in_mechanisms() -> None:
    registry = MECHANISMS.read_text(encoding="utf-8")
    for gate_id in GATE_IDS:
        assert f'id: "{gate_id}"' in registry, gate_id


def test_no_deleted_vocabulary() -> None:
    body = _body(_text()).lower()
    found = [w for w in DELETED_VOCABULARY if re.search(rf"\b{re.escape(w)}\b", body)]
    assert not found, found


def test_referenced_relative_paths_exist() -> None:
    """Every `references/...` or `assets/...` path is skill-dir-relative."""
    skill_dir = SKILL.parent
    cited = set(re.findall(r"`((?:references|assets|scripts)/[^`]+)`", _text()))
    assert cited, "the station cites no bundled file"
    missing = [p for p in cited if not (skill_dir / p).exists()]
    assert not missing, missing


def test_loom_design_version_2_2_0_consistent() -> None:
    claude_manifest = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    codex_manifest = json.loads(
        (REPO / "loom-design/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    agy_manifest = json.loads(
        (REPO / "loom-design/plugin.json").read_text(encoding="utf-8")
    )
    changelog = (REPO / "loom-design/CHANGELOG.md").read_text(encoding="utf-8")
    assert claude_manifest["version"] == "2.6.0"
    assert codex_manifest["version"] == "2.6.0"
    assert agy_manifest["version"] == "2.6.0"
    assert "## [2.6.0]" in changelog
    assert "## [2.2.1]" not in changelog
    readme_pins = {
        "README.md": "| [`loom-design`](loom-design/) | 2.6.0 |",
        "loom-design/README.md": "**Version**: 2.6.0",
        "loom-design/README.ja.md": "**Version**: 2.6.0",
        "loom-design/README.zh-TW.md": "**Version**: 2.6.0",
    }
    for name, pin in readme_pins.items():
        assert pin in (REPO / name).read_text(encoding="utf-8"), name


def test_capture_intent_bare_branch_absent() -> None:
    bare = "creates " + "`<change-id>`"  # split so the repo sweep grep skips this pin
    assert bare not in _text()


def test_plugin_declares_requires_contract() -> None:
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    assert data["requires-contract"] == ">=2.1"


def test_interview_reference_within_word_cap() -> None:
    ref = SKILL.parent / "references/interview.md"
    assert ref.is_file()
    assert len(ref.read_text(encoding="utf-8").split()) <= 1200
