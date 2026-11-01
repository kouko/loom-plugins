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


def test_decision_point_one_decides_measured_technical_choices() -> None:
    step = " ".join(_section(_text(), "## Step 4 — Decision point ①: restate and confirm").split())
    assert "measure" in step and "agent-decided" in step
    assert "hard to swap later alone does not require a user question" in step.lower()
    assert "three or more trade-offs alone do not require a user question" in step.lower()


def test_decision_point_one_asks_only_unresolved_outcomes_or_authorization() -> None:
    step = " ".join(_section(_text(), "## Step 4 — Decision point ①: restate and confirm").split()).lower()
    assert "materially change the user's outcome" in step and "preference remains unresolved" in step
    assert "already pinned" in step and "do not ask again" in step
    assert "disclose" in step and "consequence" in step
    assert "existing data" in step and "explicit consent" in step


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


def test_loom_design_version_2_17_0_consistent() -> None:
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
    assert claude_manifest["version"] == "2.18.0"
    assert codex_manifest["version"] == "2.18.0"
    assert agy_manifest["version"] == "2.18.0"
    assert package_manifest["version"] == "2.18.0"
    assert "## [2.18.0]" in changelog
    assert "## [2.2.1]" not in changelog
    readme_pins = {
        "README.md": "| [`loom-design`](loom-design/) | 2.18.0 |",
        "loom-design/README.md": "**Version**: 2.18.0",
        "loom-design/README.ja.md": "**Version**: 2.18.0",
        "loom-design/README.zh-TW.md": "**Version**: 2.18.0",
    }
    for name, pin in readme_pins.items():
        assert pin in (REPO / name).read_text(encoding="utf-8"), name
    assert "## loom-design\n\nVersion 2.18.0." in (REPO / "README.md").read_text(encoding="utf-8")


def test_capture_intent_bare_branch_absent() -> None:
    bare = "creates " + "`<change-id>`"  # split so the repo sweep grep skips this pin
    assert bare not in _text()


# --- change-branch-before-intent W1-02 -- the intent commit lands only on
# the change's branch ------------------------------------------------------

_SWITCH = "git switch -c <type>/" + "<change" + "-id>"
_TYPES = {"feat", "fix", "docs", "refactor", "test", "chore", "ci"}


def _on_yes() -> str:
    text = _text()
    start = text.index('**On "yes":**')
    return _flat(text[start:text.index("<!-- /gate -->", start)])


def test_capture_intent_branches_before_confirmation_commit() -> None:
    """A1 positive: HEAD becomes the typed change branch before the
    confirmation commit; the type list appears once in this station."""
    text, on_yes = _text(), _on_yes()
    assert text.count(_SWITCH) == 1 and _SWITCH in on_yes
    assert on_yes.index(_SWITCH) < on_yes.index("`docs(loom): intent")
    assert affirms(on_yes, "Before the confirmation commit", "make HEAD the change's branch")
    listed = [
        s for s in re.split(r"(?<=[.;])\s+", _flat(text))
        if len(set(re.findall(r"`([a-z]+)`", s)) & _TYPES) >= 3
    ]
    assert len(listed) == 1 and _TYPES <= set(re.findall(r"`([a-z]+)`", listed[0])), listed


def test_trunk_commit_allowance_absent() -> None:
    """A1 negative: no sentence lets the intent be committed on the trunk."""
    text = _flat(_text()).lower()
    for phrase in ("committed on the trunk", "does " + "not create branches",
                   "still on the trunk"):
        assert phrase not in text, phrase


def test_own_change_branch_reused_at_capture() -> None:
    """A5 positive: this change's branch is reused, the trunk gets one created,
    and an unrelated branch or detached HEAD gets no commit until resolved."""
    on_yes = _on_yes()
    assert affirms(on_yes, "already on", "this change's branch", "reuse it")
    assert affirms(on_yes, "on the trunk", "create it")
    assert affirms(on_yes, "switch to it", "`git switch <type>/<change-id>`",
                   "already exists")
    force = [s for s in re.split(r"(?<=[.;])\s+", on_yes) if "`-C`" in s]
    assert force and all(re.search(r"\bnever\b.*`-C`", s) for s in force), force
    hits = [s for s in re.split(r"(?<=[.;])\s+", on_yes)
            if "unrelated branch" in s and "detached HEAD" in s]
    assert len(hits) == 1, hits
    words = set(re.findall(r"[a-z]+", hits[0].lower()))
    assert {"resolve", "first", "preserve", "existing", "work"} <= words, hits[0]
    assert all(re.search(rf"\b(?:no|not|never)\s+{w}\b", hits[0])
               for w in ("commit", "reset", "discard")), hits[0]
    assert affirms(on_yes, "Resolve it with",
                   "`git worktree add -b <type>/<change-id> <path> <trunk>`",
                   "new worktree", "move", "intent draft")


_CARRY = "every uncommitted file this change produced"


def test_worktree_moves_carry_every_uncommitted_change_file_at_capture() -> None:
    """A6 positive: a move to another worktree, existing or new, carries every
    uncommitted change file, `PRINCIPLES.md` included, onto the change branch.
    A6 negative: no route moves only the intent draft."""
    on_yes = _on_yes()
    assert affirms(on_yes, "move", _CARRY, "another worktree", "intent draft",
                   "`PRINCIPLES.md`", "commit", "change branch")
    assert not re.search(r"move (?:the|any) uncommitted intent draft", on_yes)


def test_existing_branch_off_trunk_gets_worktree_without_b_at_capture() -> None:
    """A5 positive: off the trunk, an existing change branch checked out
    nowhere gets `git worktree add <path> <type>/<change-id>`; an absent one
    keeps `-b`; a `PRINCIPLES.md` edit moves as its diff, stopping to ask on
    a conflict. A5 negative: `git switch` is offered only on the trunk."""
    on_yes = _on_yes()
    assert affirms(on_yes, "Resolve it with",
                   "`git worktree add <path> <type>/<change-id>`", "exists",
                   "`git worktree add -b <type>/<change-id> <path> <trunk>`")
    offers = [s for s in re.split(r"(?<=[.;])\s+", on_yes)
              if "`git switch <type>/<change-id>`" in s]
    assert offers and all("on the trunk" in s for s in offers), offers
    off_trunk = [s for s in re.split(r"(?<=[.;])\s+", on_yes)
                 if "unrelated branch" in s and "detached HEAD" in s]
    assert all(re.search(r"\bno `git switch`", s) for s in off_trunk), off_trunk
    assert affirms(on_yes, "`PRINCIPLES.md` edit", "diff", "conflicts",
                   "stop and ask the maintainer")


def test_plugin_declares_requires_contract() -> None:
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    assert data["requires-contract"] == ">=2.1"


def test_interview_reference_within_word_cap() -> None:
    ref = SKILL.parent / "references/interview.md"
    assert ref.is_file()
    assert len(ref.read_text(encoding="utf-8").split()) <= 1200
