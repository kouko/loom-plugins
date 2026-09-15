"""write-spec station contract (plan W2-02).

write-spec turns a confirmed intent into `docs/loom/<change-id>/spec.md`
(concept-model §2c), runs decision point ② for product changes, and hands
the spec to loom-code's review station under the spec lens before a plan
exists. These tests pin the cross-plugin invariants a cold reader depends
on and the shapes the contract package owns.

The REQ identifier grammar is READ from `loom-code/contract/manifest.yaml`
rather than restated here: the manifest is the single declaration of the
spec schema (concept-model §11), and a second copy of the grammar in a
loom-design test would be a second drift surface.

Reading loom-code's files from a loom-design TEST is deliberate, exactly
as in `test_capture_intent_contract.py`: the ban on cross-plugin
references is a RUNTIME portability rule for prose contracts. A test runs
in this repository, where both plugins are checked out side by side.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

SKILL = REPO / "loom-design/skills/write-spec/SKILL.md"
CAPTURE_INTENT = REPO / "loom-design/skills/capture-intent/SKILL.md"
WRITE_PLAN = REPO / "loom-code/skills/write-plan/SKILL.md"
MANIFEST = REPO / "loom-code/contract/manifest.yaml"
CHECKER = REPO / "loom-code/scripts/loom_checker.py"
MECHANISMS = REPO / "docs/loom/evidence/mechanisms.yaml"

WORD_CAP = 3500
DESCRIPTION_CAP = 400
SPEC_FORMS_CAP = 900
UI_FLOWS_CAP = 700

# Vocabulary the redesign deletes (concept-model §10) plus the two terms
# this station's own predecessors carried (`expansion`, and the critic
# provenance tags). A station written after the cut reintroduces none.
DELETED_VOCABULARY = (
    "brief",
    "seed",
    "pipeline",
    "conductor",
    "batch",
    "waiver",
    "critic",
    "critic-found",
    "provenance-tagged",
    "expansion",
)

GATE_IDS = (
    "write-spec.product-visible-behaviour-confirmed-before-review",
    "write-spec.no-design-decision-shown-to-user",
)

# UI flow 2 (spec.md): the fixed sentence decision point ② is asked with.
UI_FLOW_2_SENTENCE = "你下 ___ 會看到 ___；___ 的情況會 ___。對嗎？"


def _text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _body(text: str) -> str:
    """The SKILL.md body, frontmatter stripped."""
    parts = text.split("---\n", 2)
    return parts[2] if len(parts) == 3 else text


def _gate(text: str, gate_id: str) -> str:
    m = re.search(
        rf"<!-- gate: {re.escape(gate_id)} -->(.*?)<!-- /gate -->",
        text,
        re.S,
    )
    assert m, f"gate {gate_id!r} missing or unclosed"
    return " ".join(m.group(1).split())


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert m, f"section {heading!r} missing"
    return m.group(0)


@lru_cache(maxsize=1)
def _checker_usage() -> str:
    """The checker's own usage block — its list of sub-commands."""
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--help"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    return proc.stdout + proc.stderr


@lru_cache(maxsize=1)
def _checker_rule_ids() -> frozenset[str]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--list-rules"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert proc.returncode == 0, proc.stderr
    return frozenset(
        line.split("\t", 1)[0].strip()
        for line in proc.stdout.splitlines()
        if line.strip()
    )


def _requirements_grammar() -> str:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    fields = manifest["artifacts"]["spec"]["fields"]
    for field in fields:
        if field["name"] == "Requirements":
            return field["grammar"]
    raise AssertionError("manifest declares no Requirements grammar for spec")


def _grammar_to_regex(grammar: str) -> re.Pattern[str]:
    """Turn the manifest's grammar string into a matcher.

    `<n>` is a number, `<name>` and `…` are free text; everything else —
    the literal `REQ-`, the em dash, the arrow, `Acceptance #` — is
    matched character for character, so a station that writes `REQ1` or
    drops the back-reference fails here.
    """
    pattern = ""
    for token in re.split(r"(<n>|<name>|…)", grammar):
        if token == "<n>":
            pattern += r"\d+"
        elif token == "<name>":
            pattern += r"[^\n]+?"
        elif token == "…":
            pattern += r"[\s\S]+?"
        else:
            pattern += re.escape(token)
    return re.compile(pattern)


def test_skill_file_exists() -> None:
    assert SKILL.is_file(), f"{SKILL} does not exist"


def test_frontmatter_name_and_version() -> None:
    text = _text()
    assert re.search(r"^name: write-spec$", text, re.M)
    assert re.search(r"^version: 1\.0\.0$", text, re.M)


def test_description_within_cap() -> None:
    m = re.search(r"^description: \|\n((?:  .*\n)+)", _text(), re.M)
    assert m, "description must be a block scalar"
    description = " ".join(line.strip() for line in m.group(1).splitlines())
    assert len(description) <= DESCRIPTION_CAP, len(description)


def test_body_within_word_cap() -> None:
    words = len(_body(_text()).split())
    assert words <= WORD_CAP, words


def test_requirements_preserve_acceptance_ownership_without_invented_state() -> None:
    low = _gate(_text(), "write-spec.product-visible-behaviour-confirmed-before-review").lower()

    assert "exact count" in low
    assert "`→ acceptance #<n>` mapping" in low
    assert "continuing observable result" in low
    assert "original action as the `when` trigger" in low
    assert re.search(
        r"do not invent .*named state.*lifecycle.*storage.*persistence mechanism",
        low,
    )


def test_out_of_scope_is_not_promoted_to_product_prohibition() -> None:
    low = _gate(_text(), "write-spec.product-visible-behaviour-confirmed-before-review").lower()

    assert re.search(
        r"do not promote .*out of scope.*capability does not exist.*prohibited.*irreversible.*one-way",
        low,
    )
    assert re.search(r"out of scope.*not designed.*not implemented.*not verified", low)


def test_ui_flows_do_not_invent_visible_reactions() -> None:
    writing = _gate(
        _text(), "write-spec.product-visible-behaviour-confirmed-before-review"
    ).lower()

    assert re.search(r"do not invent an interface, control, or status presentation", writing)
    assert "four variants `references/ui-flows.md` requires" in writing
    assert re.search(r"variant's content is unsupplied.*open question", writing)


def test_semantic_inversions_are_rejected() -> None:
    """Adversarial replay: opposite rules may reuse every important noun."""
    text = _text()
    gate = _gate(text, "write-spec.product-visible-behaviour-confirmed-before-review").lower()
    invent_sentences = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+", gate)
        if re.search(r"\binvent(?:s|ing)?\b", sentence)
    ]
    assert invent_sentences and all(
        re.search(r"\b(?:do not|instead of)\b.*\binvent", sentence)
        for sentence in invent_sentences
    )

    promoted = text.replace("Do not promote Out of scope", "Promote Out of scope")
    promoted_gate = _gate(
        promoted, "write-spec.product-visible-behaviour-confirmed-before-review"
    ).lower()
    assert not re.search(
        r"do not promote .*out of scope.*capability does not exist.*prohibited.*irreversible.*one-way",
        promoted_gate,
    )

    invented = text.replace("Do not invent an interface", "Invent an interface")
    invented_gate = _gate(
        invented, "write-spec.product-visible-behaviour-confirmed-before-review"
    ).lower()
    assert not re.search(
        r"do not invent an interface, control, or status presentation", invented_gate
    )

    contradicted = re.sub(
        r"instead of\s+inventing it\.",
        "instead of inventing it. Invent the control that completes the flow.",
        text,
    )
    contradicted_gate = _gate(
        contradicted, "write-spec.product-visible-behaviour-confirmed-before-review"
    ).lower()
    invent_sentences = [
        sentence
        for sentence in re.split(r"(?<=[.!?])\s+", contradicted_gate)
        if re.search(r"\binvent(?:s|ing)?\b", sentence)
    ]
    assert any(
        not re.search(r"\b(?:do not|instead of)\b.*\binvent", sentence)
        for sentence in invent_sentences
    )


def test_station_summary_is_byte_identical_to_write_plan() -> None:
    ours = _section(_text(), "## Station summary")
    theirs = _section(WRITE_PLAN.read_text(encoding="utf-8"), "## Station summary")
    assert ours == theirs


def test_station_summary_is_byte_identical_to_capture_intent() -> None:
    ours = _section(_text(), "## Station summary")
    theirs = _section(CAPTURE_INTENT.read_text(encoding="utf-8"), "## Station summary")
    assert ours == theirs


def test_what_you_will_be_asked_list_present() -> None:
    section = _section(_text(), "## What you will be asked, in plain words")
    assert "decision point ②" in section or "②" in section


def test_requirement_grammar_follows_the_manifest() -> None:
    """The station shows a REQ line that matches the manifest's grammar."""
    matcher = _grammar_to_regex(_requirements_grammar())
    assert matcher.search(_text()), matcher.pattern


def test_requirement_near_misses_are_not_shown_as_the_form() -> None:
    body = _body(_text())
    for near_miss in (r"\bREQ\d", r"\breq-\d", r"\bR-\d"):
        assert not re.search(near_miss, body), near_miss


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
    """Every bundled path the station cites is skill-dir-relative."""
    skill_dir = SKILL.parent
    cited = set(re.findall(r"`((?:references|assets|scripts)/[^`]+)`", _text()))
    assert cited, "the station cites no bundled file"
    missing = [p for p in cited if not (skill_dir / p).exists()]
    assert not missing, missing


def test_ui_flow_two_sentence_present() -> None:
    assert UI_FLOW_2_SENTENCE in _text()


def test_checker_subcommands_named_exist() -> None:
    usage = _checker_usage()
    named = set(re.findall(r"loom_checker\.py (\w[\w-]*)", _text()))
    assert {"intake", "contract"} <= named, named
    for sub in named:
        assert re.search(rf"loom_checker\.py {re.escape(sub)}\b", usage), sub


def test_checker_rules_named_exist() -> None:
    rules = _checker_rule_ids()
    named = set(re.findall(r"`((?:intake|intent|push|standing|contract)\.[a-z-]+)`", _text()))
    assert {"intake.confirmed", "standing.product-principles-reject"} <= named, named
    unknown = sorted(named - rules)
    assert not unknown, unknown


def test_intake_station_argument_is_this_station() -> None:
    assert "intake write-spec <change-id>" in _text()


def test_risk_triggered_spec_review_contract() -> None:
    text = _text()
    assert "loom-code:closing-review" in text
    assert "loom-code:write-plan" in text
    assert "pre-build-review: required|not-required — <reason>" in text
    assert "spec+adversarial" in text
    assert "do not dispatch\n   a blind runner or a separate adversary" in text
    assert "If `pre-build-review: not-required`" in text


def test_spec_risk_classes_are_explicit() -> None:
    text = _text()
    for risk in (
        "security or privacy",
        "irreversible data",
        "public contract",
        "cross-system architecture",
        "materially ambiguous",
    ):
        assert risk in text


def test_reference_files_exist_within_caps() -> None:
    forms = SKILL.parent / "references/spec-forms.md"
    flows = SKILL.parent / "references/ui-flows.md"
    assert forms.is_file() and flows.is_file()
    assert len(forms.read_text(encoding="utf-8").split()) <= SPEC_FORMS_CAP
    assert len(flows.read_text(encoding="utf-8").split()) <= UI_FLOWS_CAP


_STEP2 = "## Step 2 — Write the spec"
_STEP3 = "## Step 3 — Decision point ②, product changes only"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _flows() -> str:
    return (SKILL.parent / "references/ui-flows.md").read_text(encoding="utf-8")


def _forms() -> str:
    return (SKILL.parent / "references/spec-forms.md").read_text(encoding="utf-8")


def _affirmed(text: str, *literals: str) -> list[str]:
    """Sentences holding every literal and no negation token outside code spans.

    Engineering baseline prose-pin rule: "do not record each item in the
    spec" must not pass a pin on "record each item in the spec".
    """
    return [
        s
        for s in split_sentences(_flat(text), ".;")
        if all(lit in s for lit in literals)
        and not has_negation(re.sub(r"`[^`]*`", "", s))
    ]


def test_affirmedPin_syntheticAffirmativeSentence_accepted() -> None:
    """Self-test: an affirmative sentence satisfies the pin."""
    assert _affirmed("Read the list and record each item in the spec.", "record each item in the spec")


def test_affirmedPin_syntheticNegatedSentence_rejected() -> None:
    """Self-test (negated-pin-mutant-killed): a negated sentence fails the pin."""
    assert not _affirmed("Read the list and do not record each item in the spec.", "record each item in the spec")
    assert not _affirmed("When a flow branches, never lead with a table.", "lead with a table")


def test_spec_records_each_carried_detail() -> None:
    """A1 positive: each carried detail lands in the spec and in ② read-back."""
    step2 = _flat(_section(_text(), _STEP2))
    assert _affirmed(
        step2,
        "Read the carried-details list from `capture-intent`'s hand-off",
        "record each item in the spec",
        "a visible flow or reaction as a UI flows line",
    )
    assert _affirmed(step2, "decision point ② shows each of them as part of the read-back")
    for gate_id in GATE_IDS:
        assert "carried-details" not in _gate(_text(), gate_id)


def test_product_carried_detail_recorded_where_decision_point_two_shows() -> None:
    """A1 positive (product routing): a product change's non-visible detail goes
    on a Requirement line; only an engineering change may use Design decision,
    which ② never shows."""
    carried = _flat(_section(_text(), _STEP2)).split("**Carried details.**", 1)[1].split("Forms:", 1)[0]
    assert _affirmed(carried, "anything else on the matching Requirement line")
    design = [s for s in split_sentences(carried, ".;") if "Design decision line" in s]
    assert design and all("engineering" in s for s in design)
    assert _affirmed(carried, "engineering change", "Design decision line")


def test_agent_proposal_not_agreed_not_recorded() -> None:
    """A1 negative: nothing beyond what the user agreed is recorded."""
    step2 = _flat(_section(_text(), _STEP2))
    assert "an agent proposal the user did not agree to is not recorded" in step2
    recording = [
        s for s in re.split(r"(?<=[.])\s+", step2) if "proposal" in s.lower()
    ]
    assert recording and all("not recorded" in s for s in recording)


def test_parallel_cases_table_branching_diagram() -> None:
    """A2 positive: parallel cases are a table, branching paths a diagram."""
    flows = _flat(_flows())
    assert "several parallel cases on one surface: a table" in flows.lower()
    assert "`case | what the user does | what they see`" in flows
    assert re.search(r"branch or go back and forth.*`stateDiagram-v2` or `flowchart`", flows)
    assert "ASCII still for layout" in flows
    assert "`spec-forms.md`" in flows
    for kept in ("every variant", "naming the way out", "irreversible-step sentence", "paths walk"):
        assert kept in flows.lower(), kept
    forms = _flat(_section(_forms(), "## Table"))
    assert "**UI flow cases**" in forms
    diagram = _flat(_section(_forms(), "## Diagram"))
    assert "**UI flows** that branch or go back and forth" in diagram


def test_short_flow_stays_lines() -> None:
    """A2 boundary: the one-line form stays the default for a short flow."""
    flows = _flat(_flows())
    assert "One line per operation is the default, for a short flow" in flows
    assert "A short flow gets the sentences only" in _flat(_section(_text(), _STEP3))


def test_readback_leads_with_table_or_text_diagram() -> None:
    """A3 positive: ② leads with a table or text diagram, then the sentences."""
    step3 = _flat(_section(_text(), _STEP3))
    back = _flat(_section(_flows(), "## Reading it back"))
    for text in (step3, back):
        leading = [
            s
            for s in _affirmed(text, "parallel cases or branches, ", "then the per-case sentences")
            if re.search(r"lead\w* with a table or a text \(ASCII\) diagram", s)
        ]
        assert leading, text[:200]


def test_chat_readback_has_no_mermaid() -> None:
    """A3 negative: Mermaid never appears in the chat read-back."""
    step3 = _section(_text(), _STEP3)
    back = _section(_flows(), "## Reading it back")
    for text in (step3, back):
        flat = _flat(text)
        assert "Never put Mermaid in" in flat
        assert "a terminal shows it as raw code" in flat
        assert "```mermaid" not in text
    assert "Nothing from `## Design decision` down is ever shown to the user." in _flat(step3)


def test_plugin_declares_requires_contract() -> None:
    data = json.loads(
        (REPO / "loom-design/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    assert data["requires-contract"] == ">=2.1"
