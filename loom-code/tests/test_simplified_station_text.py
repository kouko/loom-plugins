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
CODEX_FIRST_CONTACT = (
    ROOT / "loom-code/skills/write-plan/references/codex-first-contact.md"
).read_text(encoding="utf-8")
PRINCIPLES = (ROOT / "PRINCIPLES.md").read_text(encoding="utf-8")
MEMORY_PR = (
    ROOT / "loom-workflow/skills/git-memory/protocols/compose-pr.md"
).read_text(encoding="utf-8")
SHIP_PROSE = " ".join(SHIP.split())
CAPTURE_PROSE = " ".join(CAPTURE.split())
PLAN_PROSE = " ".join(PLAN.split())
# write-plan's own intent confirmation (step 3) lives in this reference.
PLAN_CONFIRM = (
    ROOT / "loom-code/skills/write-plan/references/confirm-intent.md"
).read_text(encoding="utf-8")
PLAN_CONFIRM_PROSE = " ".join(PLAN_CONFIRM.split())
INTENT_TEMPLATE = (ROOT / "loom-code/contract/templates/intent.md").read_text(encoding="utf-8")
CONTRACT_MANIFEST = (ROOT / "loom-code/contract/manifest.yaml").read_text(encoding="utf-8")
SKIPPED_BY = "(listed by `selection show` or skipped by the user's plain-words instruction)"


def test_review_uses_one_computed_reviewer_floor_without_prose_allowlist() -> None:
    review_prose = " ".join(REVIEW.split())
    assert "loom_checker.py reviewer-count <change-id>" in review_prose
    assert "computed reviewer floor" in review_prose
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
        assert "reviewer count comes from the installed Review policy" in flat
        assert "one in the small lane, two or more in the full lane" not in flat
    for tool in TOOL_SKILLS:
        flat = " ".join(_design_skill(tool).split())
        assert "## Station summary" not in flat, tool
        assert "one in the small lane, two or more in the full lane" not in flat


def test_principles_require_the_mechanically_computed_reviewer_floor() -> None:
    principles = " ".join(PRINCIPLES.split())
    assert "mechanically computed reviewer floor" in principles
    assert "one reviewer only when the checker proves the whole change is narrow and low-risk" in principles
    assert "two reviewers for every other or undecidable change" in principles
    assert "zero reviewers" not in principles


def test_review_generates_attestation_without_ledger_ceremony() -> None:
    assert "finalize-review" in REVIEW
    assert "attestation.json" in REVIEW
    assert "agents never edit that file by hand" in REVIEW
    assert "validates that single\nattestation directly" in REVIEW
    assert "review.json" not in REVIEW


def test_ship_validates_without_replaying_functional_work() -> None:
    assert "does not repeat functional verification" in SHIP
    assert "does not execute package tests or adversarial probes" in SHIP
    assert "Publication-only edits" in SHIP
    assert "repository-local checker scaffold" in SHIP


def test_ship_keeps_publication_safety() -> None:
    assert "destination/refspec safety" in SHIP
    assert "deterministic secrets scan" in SHIP
    assert "cannot be bypassed" in SHIP


def test_ci_failure_continues_without_new_recovery_machinery() -> None:
    for phrase in (
        "same active task",
        "failed required checks and each available failure log",
        "existing test already exposes the root cause",
        "same bounded Review episode",
        "Every committed-file change",
        "must not be rerun automatically",
        "publication command's failure does not end the task",
        "PR title, body, or other publication data not committed to the "
        "repository may be fixed in place and reuse the matching attestation",
        "required change to requirements, visible behaviour, or guarantees",
        "required diagnostics or permission",
        "persistent external failure established from available evidence",
        "Run it to observe RED",
        "rerun it to observe GREEN",
    ):
        assert phrase in SHIP_PROSE
    assert "active unmerged change" in MAINTAIN
    assert "Use for CI failures" not in MAINTAIN
    for forbidden in ("recovery script", "failure classifier", "recovery state"):
        assert forbidden not in SHIP_PROSE


def test_review_uses_one_observable_claude_attempt_and_existing_retry() -> None:
    review_prose = " ".join(REVIEW.split())
    for phrase in (
        "scripts/claude_reviewer.py",
        "one Claude attempt",
        "empty-output",
        "timeout",
        "same functional-content digest",
        "does not retry",
        "outside the Codex sandbox",
        "reusable host approval",
        "Do not fall back to a sandboxed Claude invocation",
        "separate authentication preflight",
        "broader Python or shell access",
        "Do not read, copy, or move Claude credentials",
        "Only an unauthenticated result from this outside-sandbox invocation",
        "stop without treating it as transient",
    ):
        assert phrase in review_prose
    assert "Do not run a model-backed preflight." in review_prose


def test_review_consumes_every_second_vendor_selection_source() -> None:
    review_prose = " ".join(REVIEW.split())
    for source in ("fixed CLI", "per-change `ask` answer", "`selection-confirmed`"):
        assert source in review_prose


def test_ship_uses_one_publish_command_after_acceptance() -> None:
    assert "publish --confirm-authorized" in SHIP
    assert "one publication command" in SHIP
    assert "push --head HEAD --require-live-head" not in SHIP
    assert "canonical `git push` and PR commands" not in SHIP


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
    for source in ("intent", "plan", "Git change", "attestation", "available CI evidence"):
        assert source in SHIP
    assert "one top-level PR body schema" in SHIP
    assert "review.json" not in SHIP
    assert "probe ledger" not in SHIP


def test_ship_requires_auditable_decisions_without_hidden_reasoning() -> None:
    for field in ("chosen option", "material alternatives", "trade-offs", "evidence", "outcome"):
        assert field in SHIP
    assert "private or hidden chain-of-thought" in SHIP
    assert "unsupported claims" in SHIP


def test_ship_uses_mermaid_only_when_relationships_carry_information() -> None:
    for relationship in (
        "meaningful decision branches",
        "component interactions",
        "state transitions",
        "before-and-after behaviour flows",
    ):
        assert relationship in SHIP_PROSE
    assert "Mermaid" in SHIP
    assert "Simple changes must omit Mermaid diagrams" in SHIP_PROSE


def test_git_memory_contributes_without_competing_top_level_schema() -> None:
    assert "Ship owns the top-level PR body schema" in MEMORY_PR
    assert "Decision, Learning, and Gotcha" in MEMORY_PR
    assert "does not own" in MEMORY_PR
    assert "Claude Code's standard" not in MEMORY_PR
    contextual = (
        "## Context", "## Intended outcome", "## Scope", "## Decisions",
        "## Implementation", "## Behaviour change", "## Verification",
        "## Risks and rollback", "## Follow-ups",
    )
    assert not all(any(line == heading for line in MEMORY_PR.splitlines())
                   for heading in contextual)
    assert "For a non-Loom caller" in MEMORY_PR


def test_ship_diagram_contract_has_mutually_exclusive_outcomes() -> None:
    assert "Graph-bearing changes require a Mermaid diagram" in SHIP_PROSE
    assert "Simple changes must omit Mermaid diagrams" in SHIP_PROSE
    assert "exactly one of those outcomes applies" in SHIP_PROSE


def test_current_surfaces_do_not_restore_legacy_publication_ledgers() -> None:
    for surface in (SHIP, MEMORY_PR):
        assert "review.json" not in surface
        assert "probe ledger" not in surface


def test_git_memory_defers_loom_consent_and_schema_to_ship() -> None:
    assert "git-memory never re-confirms a Loom publication" in MEMORY_PR
    assert "canonical intent authorization" in MEMORY_PR
    assert "single legacy Ship decision" in MEMORY_PR
    assert "loom-code:finishing-a-development-branch" not in MEMORY_PR
    assert "For a Loom change" in MEMORY_PR
    assert "follow Ship's conditional Mermaid rule" in MEMORY_PR


def test_intent_confirmation_discloses_publication_and_separate_merge() -> None:
    for station, prose in ((CAPTURE, CAPTURE_PROSE), (PLAN_CONFIRM, PLAN_CONFIRM_PROSE)):
        assert "automatic publication is the default" in prose
        assert "non-forced push" in prose
        assert "Ready PR" in prose
        assert "explicitly opt out" in prose
        assert "merge remains a separate decision" in prose
        assert "publication: automatic — authorized <date> by <name>" in station
        assert "only after that informed yes" in prose


def test_host_specific_skill_guidance_uses_each_native_contract() -> None:
    assert "`${CLAUDE_PLUGIN_ROOT}` is substituted by Claude Code" in PLAN
    assert "`PLUGIN_ROOT` is provided to Codex plugin hook commands" in PLAN
    assert "not a general skill-shell variable" in " ".join(PLAN.split())
    assert (
        "on any other host it is the directory two levels above this SKILL.md"
        in " ".join(PLAN.split())
    )
    assert "injected loom-code plugin root" not in PLAN
    assert "hooks/hooks-codex.json" in CODEX_FIRST_CONTACT
    assert "`${PLUGIN_ROOT}`" in CODEX_FIRST_CONTACT
    assert "does not also load `hooks/hooks.json`" in CODEX_FIRST_CONTACT


def test_principles_name_installed_hooks_for_both_hosts() -> None:
    assert "Host-installed plugin hooks (Claude Code, Codex and Antigravity CLI)" in PRINCIPLES
    assert "Codex `.codex/hooks.json`" not in PRINCIPLES


def test_station_summaries_distinguish_current_and_legacy_ship_ownership() -> None:
    expected = (
        "automatic for canonical intent authorization; one user decision for a "
        "legacy intent; merge is separate"
    )
    assert expected in CAPTURE_PROSE
    assert expected in PLAN_PROSE


def test_build_has_no_evidence_accounting() -> None:
    assert "no dispatch ledger is created" in BUILD
    assert "finalize-review" in BUILD
    assert "Build never writes `attestation.json`" in BUILD
    assert "review.json" not in BUILD


def test_build_and_plan_require_implementer_dispatch_without_requiring_parallelism() -> None:
    for station in (BUILD, PLAN):
        prose = " ".join(station.split())
        assert "Scheduling multiple implementers concurrently is optional" in prose
        assert "Parallel work is optional" not in station
    assert (
        "Unless `implementer` is skipped " + SKIPPED_BY + ", implementer dispatch is "
        "mandatory for every implementation task."
    ) in " ".join(PLAN.split())
    assert "Implementer dispatch is mandatory for every implementation task" not in PLAN
    assert "implementer dispatch is mandatory" in " ".join(BUILD.split())

    build_prose = " ".join(BUILD.split())
    assert "If implementer dispatch is unavailable, stop and report the blocker" in build_prose
    assert "The main agent must not substitute itself as implementer" not in build_prose
    assert (
        "Unless `implementer` is skipped " + SKIPPED_BY + ", the main agent must not "
        "substitute itself as implementer."
    ) in build_prose
    assert "An implementation agent never acts as its own closing reviewer." in build_prose

    manifest_prose = " ".join(CONTRACT_MANIFEST.split())
    assert "every implementation task is dispatched to an implementer" in manifest_prose
    assert "scheduling multiple implementers concurrently is optional" in manifest_prose
    assert "disjoint files alone do not establish independence" in manifest_prose
    assert "no dispatch ledger is required" in manifest_prose


def test_capture_intent_boundaries_are_shared_with_code_only_intake() -> None:
    for phrase in (
        "ask only for missing required-field content",
        "observable delivery outcome",
        "complete scenarios",
        "Keep, neutralize, defer, reopen, or delete",
        "must remain `open`",
        "explicit answer",
        "decision points remain unchanged",
        "move it to Open questions",
        "before confirmation",
    ):
        assert phrase in CAPTURE_PROSE
        assert phrase in PLAN_PROSE

    assert "question quota" in CAPTURE_PROSE
    assert "question quota" in PLAN_PROSE


def test_shared_intent_contract_names_altitude_without_new_schema() -> None:
    assert "observable delivery outcomes, not scenarios or implementation" in INTENT_TEMPLATE
    assert "each line provable by independent acceptance testing" in INTENT_TEMPLATE
    assert (
        "Material user-outcome or scope choices remain open; only non-material "
        "unsupported detail is deleted"
    ) in CONTRACT_MANIFEST
    assert "why this change exists, the value when needed" in CONTRACT_MANIFEST
    assert "source-id" not in CONTRACT_MANIFEST
    assert "question-id" not in CONTRACT_MANIFEST


def test_code_only_field_boundaries_keep_problem_and_value_semantics() -> None:
    assert "who it affects, and the consequence" in PLAN_PROSE
    assert "beneficiary, urgency, and GO/NO-GO" in PLAN_PROSE
    assert "engineering intent omits obvious value" in PLAN_PROSE


def test_stations_read_the_bound_selection_at_entry() -> None:
    prose_read = (
        "run `loom_checker.py selection show <change-id>` and omit the prose steps "
        "`selection show` lists as skipped (spec, plan, implementer, tdd, acceptance-test), plus "
        "any step the user told you to skip in plain words"
    )
    review_read = (
        "run `loom_checker.py selection show <change-id>` and omit the steps `selection show` "
        "lists as skipped, plus any step the user told you to skip in plain words; §2 and §3 "
        "say how skipped reviewers, adversarial and acceptance-test are handled"
    )
    build_read = (
        "run `loom_checker.py selection show <change-id>` and omit the steps `selection show` "
        "lists as skipped (spec, plan, implementer, tdd, adversarial, package-tests, "
        "`acceptance-test` (independent acceptance testing)), plus any step the user "
        "told you to skip in plain words"
    )
    assert prose_read not in " ".join(REVIEW.split())
    assert prose_read not in " ".join(BUILD.split())
    assert (
        "- Unless reviewers are skipped, a selected second vendor remains required. Resolve it "
        "from the standing fixed CLI"
    ) in " ".join(REVIEW.split())
    for station, read in ((BUILD, build_read), (REVIEW, review_read),
                          (SHIP, prose_read), (PLAN, prose_read)):
        prose = " ".join(station.split())
        assert prose.count(read) == 1
        sentence = next(s for s in prose.split(". ") if read in s)
        assert not has_negation(sentence), sentence
        assert "intent" not in sentence.replace("(", " ").replace(",", " ").split(), sentence
        pointer = (
            "[expert-mode](../expert-mode/SKILL.md) stays an optional route the user may invoke."
        )
        assert prose.count(pointer) == 1
        assert pointer in sentence + ". "


def test_build_obligations_yield_to_a_bound_selection() -> None:
    build_prose = " ".join(BUILD.split())
    assert "Unless `tdd` is skipped " + SKIPPED_BY + ", for every behavior change:" in build_prose
    assert (
        "Unless `implementer` is skipped " + SKIPPED_BY + ", implementer dispatch is "
        "mandatory for every implementation task; when it is skipped, the main agent "
        "implements the task itself."
    ) in build_prose
    assert "For every behavior change:" not in BUILD


def test_review_dispatches_nothing_for_skipped_steps() -> None:
    depth = REVIEW.split("## 2. Compute review depth", 1)[1].split("## 3.", 1)[0]
    assert "## 3. Run blind and adversarial checks" not in REVIEW
    checks = REVIEW.split("## 3. Run acceptance testing", 1)[1].split("## 4.", 1)[0]
    assert (
        "When `reviewers` is skipped " + SKIPPED_BY + ", dispatch no reviewer and pass "
        "no `verdicts`."
    ) in " ".join(depth.split())
    checks_prose = " ".join(checks.split())
    assert (
        "When `adversarial` is skipped " + SKIPPED_BY + ", Build hands off no adversarial "
        "program and §5 omits the `adversarial` input."
    ) in checks_prose
    assert "When `acceptance-test` is skipped " + SKIPPED_BY + ", run no acceptance testing." in checks_prose


def test_review_hands_reviewer_failures_and_scopes_the_waiver() -> None:
    review_prose = " ".join(REVIEW.split())
    assert (
        "Before any fix round, pass each non-passing reviewer verdict to "
        "`loom_checker.py selection record-failure <change-id> --step reviewers --rule <verdict>`"
    ) in review_prose
    assert (
        "When a bound selection exists, `finalize-review` waives only the reviewers, "
        "adversarial and package-tests steps it lists, including no waivers when its "
        "skip list is empty. Automatic narrow-change skips apply only without a bound "
        "selection; attestation validation follows the same precedence, using the "
        "attestation's selection claim in CI where local records are unavailable."
    ) in review_prose


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
    assert SHIP_PROSE.count(STEP_NAMES_SENTENCE) == 1


def test_ship_renders_selection_disclosure_and_skipped_intent_decision() -> None:
    assert "render_selection_disclosure" not in SHIP
    assert (
        "open the Verification section with exactly these lines, filled from the attestation's "
        "`selection` field: one `Skipped steps: <steps> — authority: <source> (<code>, "
        "<YYYY-MM-DD>)` line per confirmation, then one `Prior failure: <step> <rule> "
        "<YYYY-MM-DD>` line per prior failure"
    ) in SHIP_PROSE
    assert SHIP_PROSE.count(STEP_NAMES_SENTENCE) == 1
    assert "In `<steps>`, write" not in SHIP_PROSE
    assert "On a mismatch, `publish` prints the expected lines." in SHIP_PROSE
    assert "lists the intent as skipped" not in SHIP_PROSE
    assert "## 1. Confirm publication authorization" in SHIP
    assert "loom_checker.py publish --confirm-authorized --title" in SHIP_PROSE


def test_code_only_surface_routing_matches_capture_intent() -> None:
    normalized = " ".join(PLAN_PROSE.split())
    assert "file artifact a user or external system depends on" in normalized
    assert "Visible effects with an unknown surface and no spec require" in normalized
    assert "surface-neutral reason" in normalized
    assert "internal files alone do not" in normalized


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
        assert "independent adversary's committed adversarial programs" in build[0]
        assert "complete package suite" in build[0]
        assert "must pass before hand-off" in build[0]
        assert "only content that passed Build's checks" in review[0]
        assert "again on committed content" in review[0]
        assert "execute once during" not in review[0]
        for row in (*build, *review):
            assert "closing review dispatches" not in row.lower()
            assert "closing-review dispatches" not in row.lower()


WRITE_SPEC = (ROOT / "loom-design/skills/write-spec/SKILL.md").read_text(encoding="utf-8")
ACCEPTANCE_TESTER = (ROOT / "loom-code/agents/acceptance-tester.md").read_text(encoding="utf-8")


def _affirmed_sentences(text: str, *literals: str) -> list[str]:
    return [
        s
        for s in split_sentences(" ".join(text.split()), ".;")
        if all(lit in s for lit in literals)
        and not has_negation(re.sub(r"`[^`]*`", "", s))
    ]


def test_spec_review_dispatches_reviewer_directly() -> None:
    """A1 positive: the spec author dispatches loom-code:reviewer itself."""
    for station in (PLAN, WRITE_SPEC):
        assert _affirmed_sentences(
            station, "`pre-build-review: required`", "`loom-code:reviewer`", "lens `spec+adversarial`"
        )
        assert _affirmed_sentences(station, "commit", "send", "back to that reviewer")


def test_spec_review_names_the_spec_commits_parent_as_reviewed_sha() -> None:
    """A1 follow-up: cold reader found "the commit before the spec" ambiguous;

    name the spec commit's parent explicitly so the reviewer's delta is
    exactly the spec commit."""
    for station in (PLAN, WRITE_SPEC):
        prose = " ".join(station.split())
        assert (
            prose.count(
                "the spec commit's parent (`<spec-commit>^`) as `reviewed_sha`"
            )
            == 1
        )
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
    assert _affirmed_sentences(PLAN_CONFIRM_PROSE, "The list shows how often loom interrupts the user")


def test_acceptance_tester_names_current_artifacts_and_package_suite_owners() -> None:
    flat = " ".join(ACCEPTANCE_TESTER.split())
    assert "review record" not in flat
    assert "package-tests probe" not in flat
    assert _affirmed_sentences(flat, "Build", "`finalize-review`", "package suite")


ROUTER = (ROOT / "loom-code/skills/using-loom-code/SKILL.md").read_text(encoding="utf-8")
SKIP_STATIONS = {"build": BUILD, "closing-review": REVIEW, "ship": SHIP, "using-loom-code": ROUTER,
                 "write-plan": PLAN}
SKIP_RULE = (
    "The default is the full flow: skip a step only when the user tells you to in "
    "plain words, then tell the user in one line which step is skipped and continue."
)
NO_CODE = "Never ask the user for a generated code to skip a step."
CODE_REQUEST = re.compile(
    r"expert-mode <code>|generated code|typed code|confirm\w* by typing|skip is still confirmed"
)


# skip-announced-in-one-line (A10 positive)
def test_skip_announced_in_one_line() -> None:
    assert not has_negation(SKIP_RULE)
    for name, text in SKIP_STATIONS.items():
        assert " ".join(text.split()).count(SKIP_RULE) == 1, name


# no-generated-code-requested (A10 negative)
def test_no_generated_code_requested() -> None:
    for name, text in SKIP_STATIONS.items():
        prose = " ".join(text.split())
        assert prose.count(NO_CODE) == 1, name
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


# Acceptance 11 of
# `docs/loom/intent/2026-09-23-adversarial-probes-earn-their-place.md`: the
# checker's own narrow-delta judgement costs the change its spec, plan,
# acceptance-test and adversarial steps, so every station that honours it says so in
# one line, in the same plain words a user-instructed skip already gets.
NARROW_SKIP_ANNOUNCED = (
    "At station entry, keep the full flow unless the user selected or instructed a skip. "
    "Automatic narrow-change simplification belongs to finalization and attestation validation."
)


def test_each_station_names_the_narrow_auto_skip_to_the_user() -> None:
    assert not has_negation(NARROW_SKIP_ANNOUNCED)
    for name, text in SKIP_CONDITION_STATIONS.items():
        prose = " ".join(text.split())
        assert prose.count(NARROW_SKIP_ANNOUNCED) == 1, name
        assert prose.index(NARROW_SKIP_ANNOUNCED) < prose.index(SKIP_RULE), name


NARROW_SKIP_IN_PR = (
    "Report automatic narrow-change simplification from the generated attestation's "
    "verification evidence, rather than inferring it from station entry."
)


def test_ship_lists_the_narrow_auto_skip_in_the_pr_body() -> None:
    verification = " ".join(
        SHIP.split("Under the Verification heading", 1)[1].split("When the attestation", 1)[0].split()
    )
    assert verification.count(NARROW_SKIP_IN_PR) == 1, verification


SKIP_RECORD = (
    "When you honour such a skip, append one line `skipped-by-instruction: <step> "
    "<YYYY-MM-DD>` to the plan's `## Risks` section, or the intent's `## Constraints` "
    "section when plan is absent or skipped, and commit it before dependent checks."
)


def test_each_station_records_a_plain_words_skip_in_the_plan() -> None:
    assert not has_negation(SKIP_RECORD)
    for name, text in SKIP_CONDITION_STATIONS.items():
        if name == "ship":
            continue
        prose = " ".join(text.split())
        assert prose.count(SKIP_RECORD) == 1, name
        assert prose.index(SKIP_RULE) < prose.index(SKIP_RECORD) < prose.index(NO_CODE), name
        assert "Use the confirmed intent when spec or plan is skipped." in prose
    assert "When plan is skipped, omit the plan command" in " ".join(BUILD.split())


SHIP_SKIP_TO_BODY = (
    "When you honour such a skip, write it straight into the PR body's "
    "`Skipped by instruction:` line (§2); Ship only reads the intent's and plan's "
    "`skipped-by-instruction:` lines and leaves both unchanged, because each is "
    "functional content and an appended line would make the attestation stale."
)
REVIEW_SKIP_BEFORE_DIGEST = (
    "Commit that line before reviewers read the final digest, because it changes the "
    "digest; a later commit is harmless only when the skip sends the change to Ship "
    "unattested (§5)."
)


def test_ship_writes_a_plain_words_skip_into_the_body_not_the_plan() -> None:
    assert SHIP_PROSE.count(SKIP_RECORD) == 0
    assert SHIP_PROSE.count(SHIP_SKIP_TO_BODY) == 1
    assert (SHIP_PROSE.index(SKIP_RULE) < SHIP_PROSE.index(SHIP_SKIP_TO_BODY)
            < SHIP_PROSE.index(NO_CODE))
    assert not has_negation(SHIP_SKIP_TO_BODY)
    assert has_negation(SHIP_SKIP_TO_BODY.replace("leaves", "never leaves"))


def test_review_commits_the_skip_record_before_the_final_digest() -> None:
    review_prose = " ".join(REVIEW.split())
    assert review_prose.count(REVIEW_SKIP_BEFORE_DIGEST) == 1
    assert (review_prose.index(SKIP_RECORD) < review_prose.index(REVIEW_SKIP_BEFORE_DIGEST)
            < review_prose.index(NO_CODE))
    assert not has_negation(REVIEW_SKIP_BEFORE_DIGEST)


REVIEW_NO_FINALIZE = (
    "When a step that `finalize-review` needs (reviewers, adversarial, package-tests) was "
    "skipped by the user's plain-words instruction rather than a bound selection, skip "
    "`finalize-review` and leave the change unattested: tell the user in one line that the "
    "PR will show `verification absent`, and hand the change to Ship."
)
REVIEW_FAIL_EXCLUDES_SKIP = (
    "When `finalize-review` fails for any cause other than the plain-words case above, "
    "return the fix to Build"
)


def test_review_plain_words_skip_reaches_ship_without_finalize() -> None:
    finalize = " ".join(REVIEW.split("## 5. Finalize", 1)[1].split("\n## ", 1)[0].split())
    assert finalize.count(REVIEW_NO_FINALIZE) == 1, finalize
    assert finalize.count(REVIEW_FAIL_EXCLUDES_SKIP) == 1, finalize
    assert finalize.index(REVIEW_NO_FINALIZE) < finalize.index(REVIEW_FAIL_EXCLUDES_SKIP)
    assert "When `finalize-review` fails, return the fix to Build" not in finalize
    for sentence in (REVIEW_NO_FINALIZE, REVIEW_FAIL_EXCLUDES_SKIP):
        assert not has_negation(sentence), sentence
    assert has_negation(REVIEW_NO_FINALIZE.replace("skip `finalize-review`",
                                                   "do not run `finalize-review`"))


def test_ship_builds_skipped_by_instruction_from_recorded_lines() -> None:
    verification = " ".join(
        SHIP.split("Under the Verification heading", 1)[1].split("When the attestation", 1)[0].split()
    )
    assert (
        "Build the line `Skipped by instruction: <steps>` from the intent's and plan's "
        "`skipped-by-instruction:` lines plus any skip decided at Ship (§1), not from "
        "conversation recall; with none recorded or decided, "
        "write no such line, and the recomputed `(missing: …)` clause still discloses the "
        "absent records."
    ) in verification
    assert "When the user skipped steps in plain words" not in SHIP_PROSE


def test_review_floor_mismatch_surfaces_as_stale() -> None:
    review_prose = " ".join(REVIEW.split())
    assert (
        "`finalize-review` recomputes the same policy, and the PR's verification status "
        "reports a mismatch as `stale`; the orchestrator never declares or overrides it."
    ) in review_prose
    assert "publication validation recompute" not in review_prose


def test_attestation_readers_name_the_pr_floor_check() -> None:
    assert 'readers: ["ship", "land", "the PR-floor check"]' in CONTRACT_MANIFEST
    assert '"the publication gate"' not in CONTRACT_MANIFEST


def test_readmes_name_the_hook_a_publication_reminder() -> None:
    root = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "- The plugin hooks (the publication reminder, the session context" in root
    assert ("content-bound verification, one closing review and a GitHub-enforced PR floor."
            in " ".join(root.split()))
    for name, phrase in (
        ("loom-code/README.md", "The hooks (the publication reminder, the session context"),
        ("loom-code/README.ja.md", "hook（公開リマインダー・session context・言語リマインダー）"),
        ("loom-code/README.zh-TW.md", "hook（發布提醒、session context 與語言提醒）"),
    ):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert phrase in " ".join(text.split()).replace("、 ", "、"), name
        assert "publication gate" not in text, name
    assert "push gate" not in root and "fast publication gate" not in root


def test_changelog_3_8_0_names_skip_record_and_setup_consent() -> None:
    changelog = (ROOT / "loom-code/CHANGELOG.md").read_text(encoding="utf-8")
    entry = " ".join(changelog.split("## [3.8.0]", 1)[1].split("\n## [", 1)[0].split())
    assert "`skipped-by-instruction: <step> <YYYY-MM-DD>`" in entry
    assert "`Skipped by instruction:`" in entry
    assert "consequence form" in entry
