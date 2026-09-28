from pathlib import Path

import re

from prose_pin import has_negation, split_sentences


ROOT = Path(__file__).resolve().parents[2]
REVIEW = (ROOT / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
SHIP = (ROOT / "loom-code/skills/ship/SKILL.md").read_text(encoding="utf-8")
MAINTAIN = (ROOT / "loom-code/skills/maintain/SKILL.md").read_text(encoding="utf-8")
BUILD = (ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
CAPTURE = (ROOT / "loom-design/skills/capture-intent/SKILL.md").read_text(encoding="utf-8")
PLAN = (ROOT / "loom-code/skills/write-plan/SKILL.md").read_text(encoding="utf-8")
PRINCIPLES = (ROOT / "PRINCIPLES.md").read_text(encoding="utf-8")
MEMORY_PR = (
    ROOT / "loom-workflow/skills/git-memory/protocols/compose-pr.md"
).read_text(encoding="utf-8")
SHIP_PROSE = " ".join(SHIP.split())
# write-plan's own intent confirmation (step 3) lives in this reference.
PLAN_CONFIRM = (
    ROOT / "loom-code/skills/write-plan/references/confirm-intent.md"
).read_text(encoding="utf-8")
CONTRACT_MANIFEST = (ROOT / "loom-code/contract/manifest.yaml").read_text(encoding="utf-8")
SKIPPED_BY = "(listed by `selection show` or skipped by the user's plain-words instruction)"


def test_review_uses_one_computed_reviewer_floor_without_prose_allowlist() -> None:
    review_prose = " ".join(REVIEW.split())
    assert "Every change: two fresh-context reviewers" not in REVIEW
    assert "tests only" not in review_prose
    assert "docs only" not in review_prose


def _design_skill(name: str) -> str:
    return (ROOT / "loom-design/skills" / name / "SKILL.md").read_text(encoding="utf-8")


# The station summary table lives in the three stations only; the three
# loom-design tools (product-principles, design-system, architecture) carry none.
TOOL_SKILLS = ("product-principles", "design-system", "architecture-design")


def test_station_summaries_do_not_duplicate_reviewer_counts() -> None:
    stations = [CAPTURE, PLAN, _design_skill("write-spec")]
    for station in stations:
        flat = " ".join(station.split())
        assert "one in the small lane, two or more in the full lane" not in flat
    for tool in TOOL_SKILLS:
        flat = " ".join(_design_skill(tool).split())
        assert "## Station summary" not in flat, tool
        assert "one in the small lane, two or more in the full lane" not in flat


def test_principles_require_the_mechanically_computed_reviewer_floor() -> None:
    principles = " ".join(PRINCIPLES.split())
    assert "zero reviewers" not in principles


def test_review_generates_attestation_without_ledger_ceremony() -> None:
    assert "review.json" not in REVIEW


def test_ci_failure_continues_without_new_recovery_machinery() -> None:
    assert "Use for CI failures" not in MAINTAIN
    for forbidden in ("recovery script", "failure classifier", "recovery state"):
        assert forbidden not in SHIP_PROSE


def test_ship_owns_one_self_contained_contextual_pr_body() -> None:
    for heading in (
        "## Context",
        "## Intended outcome",
        "## Scope",
        "## Decisions",
        "## Implementation",
        "## Behaviour change",
        "## Verification",
        "## Risks and rollback",
        "## Follow-ups",
    ):
        assert SHIP.count(heading) == 1


def test_git_memory_contributes_without_competing_top_level_schema() -> None:
    assert "Claude Code's standard" not in MEMORY_PR
    contextual = (
        "## Context", "## Intended outcome", "## Scope", "## Decisions",
        "## Implementation", "## Behaviour change", "## Verification",
        "## Risks and rollback", "## Follow-ups",
    )
    assert not all(any(line == heading for line in MEMORY_PR.splitlines())
                   for heading in contextual)


def test_current_surfaces_do_not_restore_legacy_publication_ledgers() -> None:
    for surface in (SHIP, MEMORY_PR):
        assert "review.json" not in surface
        assert "probe ledger" not in surface


def test_git_memory_defers_loom_consent_and_schema_to_ship() -> None:
    assert "loom-code:finishing-a-development-branch" not in MEMORY_PR


def test_host_specific_skill_guidance_uses_each_native_contract() -> None:
    assert "injected loom-code plugin root" not in PLAN


def test_build_has_no_evidence_accounting() -> None:
    assert "review.json" not in BUILD


def test_build_and_plan_require_implementer_dispatch_without_requiring_parallelism() -> None:
    for station in (BUILD, PLAN):
        assert "Parallel work is optional" not in station
    assert "Implementer dispatch is mandatory for every implementation task" not in PLAN
    build_prose = " ".join(BUILD.split())
    assert "The main agent must not substitute itself as implementer" not in build_prose


def test_shared_intent_contract_names_altitude_without_new_schema() -> None:
    assert "source-id" not in CONTRACT_MANIFEST
    assert "question-id" not in CONTRACT_MANIFEST


def test_stations_read_the_bound_selection_at_entry() -> None:
    prose_read = (
        "run `loom_checker.py selection show <change-id>` and omit the prose steps "
        "`selection show` lists as skipped (spec, plan, implementer, tdd, acceptance-test), plus "
        "any step the user told you to skip in plain words"
    )
    assert prose_read not in " ".join(REVIEW.split())
    assert prose_read not in " ".join(BUILD.split())


def test_build_obligations_yield_to_a_bound_selection() -> None:
    assert "For every behavior change:" not in BUILD


def test_review_dispatches_nothing_for_skipped_steps() -> None:
    assert "## 3. Run blind and adversarial checks" not in REVIEW


# One shared sentence for the step-list lines Ship builds itself; its example
# is the checker's own mapping, so prose and code cannot drift apart.
STEP_NAMES_SENTENCE = (
    "In the `<steps>` of the `Skipped by instruction:` and `Skipped steps:` lines, write "
    "`acceptance-test` as `acceptance-test (independent acceptance testing)`; every other "
    "step reads as recorded."
)


def test_ship_step_names_example_matches_the_checker_mapping() -> None:
    from loom_checker.rule_checks.publish import STEP_PLAIN_NAMES

    examples = re.findall(r"write `([^`]+)` as `([^`]+)`", STEP_NAMES_SENTENCE)
    assert dict(examples) == STEP_PLAIN_NAMES


def test_ship_renders_selection_disclosure_and_skipped_intent_decision() -> None:
    assert "render_selection_disclosure" not in SHIP
    assert "In `<steps>`, write" not in SHIP_PROSE
    assert "lists the intent as skipped" not in SHIP_PROSE


def _station_summary_rows(station: str) -> tuple[list[str], list[str]]:
    rows = [line for line in station.splitlines() if line.startswith("| ")]
    build = [row for row in rows if row.startswith("| build |")]
    review = [row for row in rows if row.startswith("| closing-review |")]
    return build, review


def test_station_summary_rows_name_builds_mechanical_checks() -> None:
    for tool in TOOL_SKILLS:
        assert _station_summary_rows(_design_skill(tool)) == ([], []), tool
    stations = [CAPTURE, PLAN, _design_skill("write-spec")]
    for station in stations:
        build, review = _station_summary_rows(station)
        assert len(build) == 1 and len(review) == 1
        assert "execute once during" not in review[0]
        for row in (*build, *review):
            assert "closing review dispatches" not in row.lower()
            assert "closing-review dispatches" not in row.lower()


WRITE_SPEC = (ROOT / "loom-design/skills/write-spec/SKILL.md").read_text(encoding="utf-8")
ACCEPTANCE_TESTER = (ROOT / "loom-code/agents/acceptance-tester.md").read_text(encoding="utf-8")


def test_spec_review_names_the_spec_commits_parent_as_reviewed_sha() -> None:
    """A1 follow-up: cold reader found "the commit before the spec" ambiguous."""
    for station in (PLAN, WRITE_SPEC):
        prose = " ".join(station.split())
        assert "the commit before the spec" not in prose


def test_closing_review_scope_spec_rejected() -> None:
    """A1 negative: no station hands a pre-build spec to closing-review."""
    for station in (PLAN, WRITE_SPEC):
        flat = " ".join(station.split())
        assert "scope `spec`" not in flat
        assert "hand the spec to the **closing-review** station" not in flat
        assert "hand it to **`loom-code:closing-review`**" not in flat


def test_plan_questions_asked_claims_no_reader_or_design_record() -> None:
    for text in (PLAN, PLAN_CONFIRM):
        flat = " ".join(text.split())
        assert "questions[]" not in text
        assert "§11" not in text
        assert "review record" not in flat


def test_acceptance_tester_names_current_artifacts_and_package_suite_owners() -> None:
    flat = " ".join(ACCEPTANCE_TESTER.split())
    assert "review record" not in flat
    assert "package-tests probe" not in flat


ROUTER = (ROOT / "loom-code/skills/using-loom-code/SKILL.md").read_text(encoding="utf-8")
SKIP_STATIONS = {"build": BUILD, "closing-review": REVIEW, "ship": SHIP, "using-loom-code": ROUTER,
                 "write-plan": PLAN}
CODE_REQUEST = re.compile(
    r"expert-mode <code>|generated code|typed code|confirm\w* by typing|skip is still confirmed"
)


# no-generated-code-requested (A10 negative)
def test_no_generated_code_requested() -> None:
    for name, text in SKIP_STATIONS.items():
        prose = " ".join(text.split())
        for sentence in split_sentences(prose):
            if CODE_REQUEST.search(sentence):
                assert has_negation(sentence), (name, sentence)


# Every skip condition in a station honours both skip sources: the bound
# selection and the user's plain-words instruction. A sentence that names a
# skip read only from `selection show` contradicts the plain-words rule.
SKIP_CONDITION_STATIONS = {"build": BUILD, "closing-review": REVIEW, "ship": SHIP,
                           "write-plan": PLAN}
SELECTION_ONLY = re.compile(r"`selection show` lists `|\bit lists `|omit only the")


def _selection_only_skip_conditions(prose: str) -> list[str]:
    return [s for s in split_sentences(prose)
            if SELECTION_ONLY.search(s)
            or (re.search(r"\blists\b.*\bas skipped\b", s) and "plain words" not in s)]


def test_no_skip_condition_reads_selection_show_alone() -> None:
    for name, text in SKIP_CONDITION_STATIONS.items():
        assert _selection_only_skip_conditions(" ".join(text.split())) == [], name


def test_selection_only_detector_rejects_the_old_forms() -> None:
    for old in (
        "Unless `selection show` lists `tdd` as skipped, for every behavior change:",
        "until every adversarial program has passed or it lists `adversarial` as skipped.",
        "At entry, run it and omit only the steps it lists as skipped (spec, plan).",
    ):
        assert _selection_only_skip_conditions(old), old
    assert not _selection_only_skip_conditions(
        "Unless `tdd` is skipped " + SKIPPED_BY + ", for every behavior change:")


def test_review_floor_mismatch_surfaces_as_stale() -> None:
    review_prose = " ".join(REVIEW.split())
    assert "publication validation recompute" not in review_prose


def test_attestation_readers_name_the_pr_floor_check() -> None:
    assert 'readers: ["ship", "land", "the PR-floor check"]' in CONTRACT_MANIFEST
    assert '"the publication gate"' not in CONTRACT_MANIFEST


def test_readmes_name_the_hook_a_publication_reminder() -> None:
    root = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in ("loom-code/README.md", "loom-code/README.ja.md", "loom-code/README.zh-TW.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "publication gate" not in text, name
    assert "push gate" not in root and "fast publication gate" not in root
