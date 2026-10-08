# concern: capture-intent's complexity check drifts out of Step 4, loses a pinned sentence (one stop, trigger, exemption, absent-plugin skip), swaps critique's mode or reaches into loom-workflow's files
"""capture-intent station contract (plan W2-01).

The station is loom-design's entry point. These tests check its structure:
frontmatter, word caps, gate markers and their registration, resolving
paths, absent deleted vocabulary, and the
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
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from prose_pin import affirms  # noqa: E402

SKILL = REPO / "loom-design/skills/capture-intent/SKILL.md"
SECOND_VENDOR = REPO / "loom-design/skills/capture-intent/references/second-vendor.md"
WRITE_PLAN = REPO / "loom-code/skills/write-plan/SKILL.md"
WRITE_SPEC = REPO / "loom-design/skills/write-spec/SKILL.md"
TOOL_SKILLS = (
    REPO / "loom-design/skills/design-system/SKILL.md",
    REPO / "loom-design/skills/product-principles/SKILL.md",
    REPO / "loom-design/skills/architecture-design/SKILL.md",
)
STATION_TABLE_HEADER = "| station | artifact | who decides | checker | checkpoint |"
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


STEP_4 = "## Step 4 — Decision point ①: restate and confirm"

# Whole sentences, not keyword subsets: a keyword pin lets reversed meaning pass.
NO_SECOND_STOP = (
    "Compose **one message**. Everything below goes into it; you do not stop "
    "twice, and this is the only stop this station makes."
)
COMPLEXITY_CHECK = (
    "When the user's request or an option under discussion would add a "
    "mechanism, field, rule or step, run `loom-workflow:critique` in complexity "
    "mode before you compose this message.",
    "Carry only its verdict and its smaller alternative into this message, in "
    "the user's plain words; this adds no stop, and the user still chooses.",
    "Never paste critique's full response, its mindset or its "
    "question-by-question shape.",
    "A request that adds no such cost, such as a bug fix or a wording change, "
    "does not run it.",
    "When loom-workflow is not installed, skip this item; the rest of this "
    "message is unchanged.",
)


def _flat(text: str) -> str:
    return " ".join(text.split())


def test_step_4_runs_complexity_check_in_the_one_message() -> None:
    """A1-A4 positive, A2 boundary: the pinned sentences and the one-stop rule."""
    step_4 = _flat(_section(_text(), STEP_4))
    for sentence in (NO_SECOND_STOP, *COMPLEXITY_CHECK):
        assert sentence in step_4, sentence


def test_critique_named_only_in_step_4() -> None:
    """A1 negative: no other step runs it, and no path reaches into loom-workflow."""
    text = _text()
    outside = text.replace(_section(text, STEP_4), "")
    assert "critique" not in outside.lower()
    assert "loom-workflow/" not in text


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


def test_second_vendor_direct_request_and_antigravity_route() -> None:
    routing = SECOND_VENDOR.read_text(encoding="utf-8")
    station = _text()
    assert "direct user request" in routing
    assert "unambiguous active review target" in routing
    assert affirms(routing, "Skip", "per-change question", "direct user request")
    assert "suggestion alone" in routing
    assert "continue without asking" in routing
    assert "agy" in routing
    assert "selected model's provider family" in _flat(routing)
    assert "On Antigravity CLI, probe nothing" not in routing
    assert "cannot run on Antigravity CLI" not in routing
    assert "direct user request" in station


def test_second_vendor_direct_request_negation_is_rejected() -> None:
    routing = SECOND_VENDOR.read_text(encoding="utf-8")
    sentence = (
        "Skip the per-change question when a direct user request names an "
        "outside coding agent and an unambiguous active review target."
    )
    assert sentence in _flat(routing)
    reversed_routing = routing.replace(sentence, "Do not " + sentence, 1)
    assert not affirms(
        reversed_routing, "Skip", "per-change question", "direct user request"
    )


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
    package_manifest = json.loads(
        (REPO / "loom-design/package.json").read_text(encoding="utf-8")
    )
    changelog = (REPO / "loom-design/CHANGELOG.md").read_text(encoding="utf-8")
    assert claude_manifest["version"] == "2.14.0"
    assert codex_manifest["version"] == "2.14.0"
    assert agy_manifest["version"] == "2.14.0"
    assert package_manifest["version"] == "2.14.0"
    assert "## [2.14.0]" in changelog
    assert "## [2.2.1]" not in changelog
    readme_pins = {
        "README.md": "| [`loom-design`](loom-design/) | 2.14.0 |",
        "loom-design/README.md": "**Version**: 2.14.0",
        "loom-design/README.ja.md": "**Version**: 2.14.0",
        "loom-design/README.zh-TW.md": "**Version**: 2.14.0",
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
