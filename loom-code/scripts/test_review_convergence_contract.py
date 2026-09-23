import re
from pathlib import Path

from prose_pin import has_negation, split_sentences


ROOT = Path(__file__).resolve().parents[2]
REVIEW = (ROOT / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
# The attack protocol's own text is pinned in test_adversary_protocol.py, so
# that a change to it turns that file red and names it; this module keeps the
# station's text.
REVIEWER = (ROOT / "loom-code/agents/reviewer.md").read_text(encoding="utf-8")
REVIEW_WORDS = " ".join(REVIEW.split())
CONTRACT = " ".join((REVIEW + "\n" + REVIEWER).split())


def test_review_episode_has_three_distinct_content_rounds_and_no_identity_reset() -> None:
    assert "<!-- gate: review.bounded-episode -->" in REVIEW
    assert "<!-- /gate -->" in REVIEW
    assert "three distinct functional-content digests" in REVIEW_WORDS
    assert "does not reset" in REVIEW_WORDS
    for identity in ("reviewer", "vendor", "model", "task", "app", "branch"):
        assert identity in REVIEW_WORDS


def test_round_roles_name_three_rounds_and_relook_term() -> None:
    assert "Round 1" in REVIEW_WORDS
    assert "Round 2" in REVIEW_WORDS
    assert "Round 3" in REVIEW_WORDS
    assert "technical design re-look" in REVIEW_WORDS
    assert "NON_CONVERGENT" in CONTRACT
    assert "Round 4" in CONTRACT


def test_stuck_review_stops_local_patching() -> None:
    assert "same blocker survives two consecutive rounds" in REVIEW_WORDS
    assert "blocker count does not decrease" in REVIEW_WORDS
    assert "stop local patching" in REVIEW_WORDS


def test_agent_owns_technical_choices_until_product_contract_changes() -> None:
    assert "requirements, visible behavior, or guarantees" in REVIEW_WORDS
    assert "Do not ask the user whether to continue" in REVIEW_WORDS


def test_same_content_executor_retry_is_bounded_and_not_a_round() -> None:
    assert "same functional-content digest" in REVIEW_WORDS
    assert "retry once" in REVIEW_WORDS
    assert "EXECUTION_FAILED" in CONTRACT


def test_contract_adds_no_review_round_ledger_or_schema() -> None:
    forbidden = ("review-round.json", "rounds.json", "review_episode.json")
    assert not any(name in CONTRACT for name in forbidden)


def test_round_four_is_forbidden_in_context() -> None:
    assert "never dispatch Round 4" in REVIEW_WORDS
    assert "must not dispatch Round 4" in CONTRACT


def _sentences(text: str) -> list[str]:
    return split_sentences(text, ends=".:;")  # colon is a boundary here


def test_station_commits_report_before_finalize() -> None:
    instruction = "commit that report on the change branch before"
    assert instruction in REVIEW_WORDS
    assert "before running `finalize-review`" in REVIEW_WORDS
    assert "docs/loom/<change-id>/blind-run-report.md" in REVIEW_WORDS
    command = "loom_checker.py finalize-review <change-id>"
    assert REVIEW_WORDS.index(instruction) < REVIEW_WORDS.index(command)


def test_report_committed_before_reviewers_read_final_digest() -> None:
    order = next(s for s in _sentences(REVIEW_WORDS) if "commit that report" in s)
    assert "Finish the blind run" in order
    assert "before the reviewers read the final functional-content digest" in order
    reason = next(s for s in _sentences(REVIEW_WORDS) if "committed after their verdicts" in s)
    assert "next round" in reason


_COMMIT_AFTER_VERDICTS = re.compile(
    r"\bcommit (?:that|the|its) (?:blind-run )?report\b[^.]*\bafter\b"
    r"|\bafter\b[^.]*\b(?:verdicts?|reviewers? (?:read|return))\b[^.]*\bcommit (?:that|the|its) (?:blind-run )?report\b",
    re.IGNORECASE,
)


def test_report_commit_after_verdicts_not_instructed() -> None:
    assert _COMMIT_AFTER_VERDICTS.search("After the verdicts arrive, commit the blind-run report.")
    assert _COMMIT_AFTER_VERDICTS.search("Commit that report after reviewers return.")
    assert not _COMMIT_AFTER_VERDICTS.search("A report committed after their verdicts needs the next round.")
    offending = [s for s in _sentences(REVIEW_WORDS) if _COMMIT_AFTER_VERDICTS.search(s)]
    assert offending == []


def test_finalize_before_report_commit_not_instructed() -> None:
    finalize_then_commit = re.compile(
        r"finaliz\w*.*\b(then|afterwards?|later)\b.*commit\w*.*blind-run report"
        r"|commit\w*.*blind-run report.*\b(after|once)\b.*finaliz",
        re.IGNORECASE,
    )
    offending = [s for s in _sentences(REVIEW_WORDS) if finalize_then_commit.search(s)]
    assert offending == []


def test_reviewer_yaml_is_converted_to_finalization_json() -> None:
    assert "structured YAML" in REVIEW_WORDS
    assert "convert" in REVIEW_WORDS
    assert "temporary JSON" in REVIEW_WORDS


# ---------------------------------------------------------------------------
# Acceptance A4/A5 — the recording passage at the end of convergence
#
# READ THIS BEFORE YOU EDIT OR DELETE ANYTHING BELOW.
#
# The passage these tests pin says three things: a lesson this branch already
# taught is written down while a round can still absorb it, a recorded lesson
# is ordinary functional content and never justifies a fourth digest, and
# almost nothing qualifies. It is deliberately inert — it names no plugin,
# calls no tool, and sits OUTSIDE the `review.bounded-episode` gate markers so
# it registers no mechanism and needs no budget exception.
#
# It has been lost once. From 2026-07-08 (#515) the timing half was carried by
# the `finishing-a-development-branch` skill and pinned by a test; the loom 1.0
# cutover (#780) deleted that skill, and the instruction and its test went out
# together. Nothing was left to go red, so nobody noticed, and two consecutive
# changes afterwards reached merge before anyone thought about memory at all.
#
# WHAT KIND OF TEST THIS IS, stated accurately because the previous wording
# here overclaimed it: this is a LITERAL-PHRASE pin. Whitespace is flattened
# first, so prose may rewrap freely — but the phrases below are matched
# literally, and a faithful rewrite that says "goes in the commit message"
# instead of "belongs in its commit message" WILL go red. That is not a defect
# and it is not a reason to delete the pin. The correct response to a red is:
#
#   1. check the clause is still in the passage and still says the same thing;
#   2. if it is, update the phrase list below in the same commit as the
#      rewrite, and say in that commit that the meaning was preserved;
#   3. if it is not, you are removing a station contract — that needs an
#      intent, not an edit here.
#
# Step 2 is the one that looks like the anti-pattern every reviewer is trained
# to stop. It is not, provided the commit shows the clause survived. Deleting
# the assertion is what the 2026-07 cutover did.
# ---------------------------------------------------------------------------

_WHY = (
    "This element belongs to the recording passage at the end of convergence. "
    "It was lost once already when loom 1.0 deleted the skill carrying it "
    "along with its test. If the passage was reworded and still says this, "
    "update the phrase here in the same commit; if the clause is gone, that is "
    "a station contract change and needs an intent. See this section's header."
)


def _recording_passage() -> str:
    """The whole passage between the convergence gate's close and Finalize.

    Selecting one `\n\n` block was a real gap: the scarcity paragraph sat
    outside it, so a plugin name or a gate marker could be added there with
    every test staying green. Acceptance 5 is a property of the passage.
    """
    finalize = REVIEW.index("\n## 5. Finalize")
    closes_episode = REVIEW.rindex("<!-- /gate -->", 0, finalize)
    return REVIEW[closes_episode + len("<!-- /gate -->") : finalize]


def _flat_passage() -> str:
    """The passage with whitespace flattened — every clause assertion in this
    section runs against THIS, never against the whole station file.

    Every defect this episode found was one assertion reading a wider text
    than the clause it defends: the clause survived somewhere else in the
    file and the test stayed green while its subject was deleted. Widening
    the scope of an assertion here does not make it stricter, it makes it
    about something other than its name.
    """
    return " ".join(_recording_passage().split())


def test_convergence_states_the_recording_moment() -> None:
    """Timing half: record while a round can still read it, not after merge."""
    passage = _flat_passage()
    for element in (
        "after the merge costs a branch",
        "docs/loom/memory/",
        "a digest the reviewers read",
    ):
        assert element in passage, (
            f"the recording passage no longer states {element!r}. {_WHY}"
        )


def test_convergence_forbids_spending_an_extra_digest_on_a_lesson() -> None:
    """Recording is not free: a memory entry is functional content, so the
    passage must say where it lands and that it never buys another round.

    Scoped to the passage. Against the whole file this test passed while the
    sentence it names was deleted, because `functional content` occurs four
    more times in the station text — the same union-scoping defect this
    episode had just fixed elsewhere, reintroduced in the commit that fixed
    it."""
    passage = _flat_passage()
    for element in (
        "functional content",
        "never justifies exceeding this episode's digests",
    ):
        assert element in passage, (
            f"the recording passage no longer states {element!r}. {_WHY}"
        )


def test_convergence_states_the_scarcity_bar() -> None:
    """Scarcity half: almost nothing surfaced by a review is durable."""
    passage = _flat_passage()
    for element in (
        "Almost nothing qualifies",
        "belongs in its commit message",
        "Zero to one durable lesson per change",
    ):
        assert element in passage, (
            f"the recording passage no longer states {element!r}. {_WHY}"
        )


def test_recording_passage_invokes_nothing_and_registers_no_mechanism() -> None:
    """The whole passage must stay inert: no plugin name, no tool call, and no
    gate marker anywhere in it, so the mechanism count is unchanged."""
    passage = _recording_passage()
    assert "cheap to keep" in passage, (
        "the recording passage is gone from the end of convergence. " + _WHY
    )
    assert "<!-- gate:" not in passage, (
        "the passage must not be marked as a gate: the charter forbids a "
        "prose-only gate, and its criterion is a judgement. " + _WHY
    )
    for plugin in ("loom-memory", "loom-workflow", "git-memory"):
        assert plugin not in passage, (
            f"the passage must not name {plugin!r}; it points at a store path "
            "that can be checked for existence, not at an install. " + _WHY
        )
    for invocation in ("Invoke", "invoke the", "Use `"):
        assert invocation not in passage, (
            f"the passage must not instruct an invocation ({invocation!r}); "
            "#821 REQ-4 forbids a station calling memory by virtue of being "
            "reached. " + _WHY
        )


def test_blind_run_before_first_reviewer_dispatch() -> None:
    section = REVIEW.split("## 2. Compute review depth", 1)[1].split("## 3.", 1)[0]
    words = " ".join(section.split())
    sentence = (
        "When a blind run is needed, finish it and commit its report (§3) "
        "before dispatching the first reviewers."
    )
    assert sentence in words
    assert words.index(sentence) < words.index("loom_checker.py reviewer-count")


# ---------------------------------------------------------------------------
# 2026-09-15-mechanical-checks-before-review — acceptance 3, 6, 7
# ---------------------------------------------------------------------------

def _flat_section(heading: str) -> str:
    return " ".join(REVIEW.split(heading, 1)[1].split("\n## ", 1)[0].split())


_EARLY_DISPATCH = re.compile(
    r"\b(?:while|during|in parallel|still run\w*|under time pressure)\b", re.IGNORECASE
)
_OPTIONAL_ROUND = re.compile(
    r"\b(?:may|might|can|optional(?:ly)?|skip\w*|waive\w*)\b", re.IGNORECASE
)


def _early_dispatch_sentences(text: str) -> list[str]:
    """Sentences that permit dispatching reviewers before Build's checks finish."""
    return [
        s for s in _sentences(text)
        if re.search(r"\bdispatch\w*\b", s, re.IGNORECASE)
        and re.search(r"\breviewers?\b", s)
        and _EARLY_DISPATCH.search(s)
    ]


# The §2 precondition has two antecedents, not one. Until 2026-09-19 a single
# `Otherwise` clause carried both, which is the defect W0-02 repaired: a check
# that reported a failure and an item that was simply absent collapsed into the
# same branch, and a re-entered run cycled build -> closing-review -> ship. The
# obligation these helpers and assertions defend is unchanged — no reviewer is
# dispatched until Build's checks are confirmed — but it is now pinned per
# branch, so losing either one goes red on its own.
_BRANCH_ANTECEDENT = re.compile(
    r"reports a check failing|an item is absent|it is another station",
    re.IGNORECASE,
)
_AFFIRMATIVE_DISPATCH = re.compile(r"\bdispatch\w*\b(?!\s+no\b)", re.IGNORECASE)


def test_gate_helpers_synthetic() -> None:
    assert _early_dispatch_sentences(
        "Under time pressure, dispatch reviewers while Build's checks still run."
    )
    assert not _early_dispatch_sentences("Otherwise return the change to Build and dispatch no reviewer.")
    assert not _early_dispatch_sentences(
        "When that hand-off reports a check failing, return the change to Build "
        "and dispatch no reviewer."
    )
    assert _OPTIONAL_ROUND.search("the fixed content may skip the next review round")
    assert not _OPTIONAL_ROUND.search("the fixed content must pass the next review round")
    assert _AFFIRMATIVE_DISPATCH.search("When an item is absent, dispatch the reviewers anyway.")
    assert not _AFFIRMATIVE_DISPATCH.search(
        "When it is another station, return the change there and dispatch no reviewer."
    )


def test_reviewers_dispatched_after_build_checks() -> None:
    depth = _flat_section("## 2. Compute review depth")
    confirm = next(s for s in _sentences(depth) if s.startswith("Before dispatching reviewers in any round"))
    for element in ("Build's hand-off", "complete package suite", "every adversarial program", "`selection show`"):
        assert element in confirm, confirm
    assert not has_negation(confirm), confirm
    for step in (
        "the complete package suite passing or `package-tests` is skipped (listed by "
        "`selection show` or skipped by the user's plain-words instruction)",
        "every adversarial program passing or `adversarial` is skipped (listed by "
        "`selection show` or skipped by the user's plain-words instruction)",
        "each skip waiving only its own check",
    ):
        assert step in confirm, confirm
    assert "that step" not in confirm, confirm

    # Branch 1 — a check reported a failure: back to Build, no reviewer.
    failing = next(
        s for s in _sentences(depth)
        if s.startswith("When that hand-off reports a check failing")
    )
    assert "return the change to Build" in failing, failing
    assert "dispatch no reviewer" in failing, failing

    # Branch 2 — the item is absent: a distinct antecedent, routed by owner
    # lookup, and still no reviewer. Absence must not read as a failing check.
    assert "Absence is a distinct antecedent from a failing check." in depth
    neither = next(
        s for s in _sentences(depth)
        if s.startswith("Neither state is a check reporting a failure")
    )
    assert "neither routes like one" in neither, neither
    produced_here = next(
        s for s in _sentences(depth) if s.startswith("When that owner is this station")
    )
    assert "produce the item here" in produced_here, produced_here
    assert "route it nowhere" in produced_here, produced_here
    elsewhere = next(
        s for s in _sentences(depth) if s.startswith("When it is another station")
    )
    assert "return the change there" in elsewhere, elsewhere
    assert "dispatch no reviewer" in elsewhere, elsewhere
    assert "Recovery adds a path and waives nothing" in depth
    assert "every check above runs on the recovered content" in depth

    # Neither branch may dispatch a reviewer.
    for sentence in _sentences(depth):
        if _BRANCH_ANTECEDENT.search(sentence):
            assert not _AFFIRMATIVE_DISPATCH.search(sentence), sentence

    assert _early_dispatch_sentences(REVIEW_WORDS) == []
    assert depth.index(confirm) < depth.index("loom_checker.py reviewer-count")
    round_two = next(s for s in REVIEW_WORDS.split("- **") if s.startswith("Round 2"))
    assert "repeats its end-of-Build mechanical checks" in round_two


def test_no_adversary_dispatch_in_closing_review() -> None:
    assert "loom-code:adversary" not in REVIEW
    assert "adversary dispatch" not in REVIEW_WORDS
    assert "create committed adversarial programs" not in REVIEW_WORDS
    assert "Run blind and adversarial checks" not in REVIEW
    for sentence in _sentences(REVIEW_WORDS):
        if re.search(r"\badversary\b", sentence):
            assert has_negation(sentence), sentence


def test_probe_graduation_gate_states_both_halves() -> None:
    """The station rule behind `review.probe-graduation`.

    Acceptance 6 of
    `docs/loom/intent/2026-09-23-adversarial-probes-earn-their-place.md`: a
    probe that caught a defect graduates into the suite that runs on every
    later change, and one that caught none is reported and deleted. It is a
    station rule with no checker rule behind it, so this test is the whole
    mechanism: both halves, and the source the station reads each program's
    result from.
    """
    assert "<!-- gate: review.probe-graduation -->" in REVIEW
    gate = " ".join(
        REVIEW.split("<!-- gate: review.probe-graduation -->", 1)[1]
        .split("<!-- /gate -->", 1)[0]
        .split()
    )
    graduated = next(s for s in _sentences(gate) if s.startswith("A probe program that caught"))
    assert "carried into the suite that runs on every later change" in graduated, graduated
    assert "through a plan task" in graduated, graduated
    assert not has_negation(graduated), graduated
    deleted = next(s for s in _sentences(gate) if s.startswith("A program of this change"))
    for element in ("caught none", "named as such in the review report", "deleted from the repository"):
        assert element in deleted, (element, deleted)
    assert "Build's hand-off" in gate and "observed result" in gate, gate


def test_finalize_failure_fix_needs_next_round() -> None:
    finalize = _flat_section("## 5. Finalize")
    sentence = next(s for s in _sentences(finalize) if s.startswith("When `finalize-review` fails"))
    for element in (
        "return the fix to Build, which repeats its end-of-Build mechanical checks",
        "must pass the next review round (§4) before `finalize-review` runs again",
    ):
        assert element in sentence, sentence
    assert not has_negation(sentence), sentence
    for other in _sentences(finalize):
        if re.search(r"\bround\b|end-of-Build|mechanical checks", other):
            assert not _OPTIONAL_ROUND.search(other), other
    assert "The checker runs the declared package suite and each adversarial program once." in finalize


def test_finalize_failure_without_round_is_non_convergent() -> None:
    finalize = _flat_section("## 5. Finalize")
    sentence = next(s for s in _sentences(finalize) if s.startswith("When no round remains"))
    assert "fourth distinct digest" in sentence, sentence
    assert "ends the episode as `NON_CONVERGENT`" in sentence, sentence


def test_earlier_verdicts_not_reused() -> None:
    finalize = _flat_section("## 5. Finalize")
    assert "Earlier verdicts are never reused for the fixed content." in finalize
    for sentence in _sentences(REVIEW_WORDS):
        if re.search(r"\breus(?:e|ed|es|ing)\b", sentence, re.IGNORECASE):
            assert has_negation(sentence), sentence
    rerun_with_old = re.compile(
        r"\b(?:re-?run|run)\b[^.]*`finalize-review`[^.]*\b(?:same|earlier|previous|existing|prior) verdicts",
        re.IGNORECASE,
    )
    assert not [s for s in _sentences(REVIEW_WORDS) if rerun_with_old.search(s)]


def test_unresolved_adversarial_findings_reach_finalize_input() -> None:
    finalize = _flat_section("## 5. Finalize")
    sentence = next(s for s in _sentences(finalize) if "unresolved adversarial finding" in s)
    assert "`findings` input" in sentence, sentence
    assert "Build's hand-off" in sentence, sentence
    assert not has_negation(sentence), sentence
    assert not _OPTIONAL_ROUND.search(sentence), sentence


# ---------------------------------------------------------------------------
# 2026-09-15-station-gaps-after-dogfood — acceptance 2
# ---------------------------------------------------------------------------

def _round_three_bullet() -> str:
    start = REVIEW.index("- **Round 3")
    return " ".join(REVIEW[start:].split("\n\n", 1)[0].split())


def test_round2_blockers_still_require_relook_before_round3() -> None:
    stuck = next(
        s for s in split_sentences(REVIEW_WORDS, ends=".")
        if s.startswith("Treat the episode as stuck")
    )
    trigger, _, action = stuck.partition(";")
    condition = next(c for c in trigger.split(", ") if "Round 2 still has blockers" in c)
    assert not has_negation(condition), condition
    assert "stop local patching" in action, stuck
    assert "technical design re-look" in action, stuck
    assert not has_negation(action), action


def _round_three_relook_sentences(text: str) -> list[str]:
    """Sentences that name Round 3 and also the technical design re-look."""
    return [s for s in _sentences(text) if "Round 3" in s and "technical design re-look" in s]


def test_round_three_relook_helper_synthetic() -> None:
    assert _round_three_relook_sentences(
        "Round 1 reviews. Before Round 3, always perform a technical design re-look."
    ) == ["Before Round 3, always perform a technical design re-look."]
    assert _round_three_relook_sentences(
        "Treat the episode as stuck when Round 2 still has blockers; use the next "
        "available round only after the technical design re-look."
    ) == []


def test_finalize_failure_round_requires_no_relook() -> None:
    bullet = _round_three_bullet()
    assert "technical design re-look" not in bullet, bullet
    assert "stop local patching" not in bullet, bullet
    converge = _flat_section("## 4. Converge within one bounded episode")
    assert _round_three_relook_sentences(converge) == []
    finalize = _flat_section("## 5. Finalize")
    for sentence in _sentences(finalize):
        if "technical design re-look" in sentence:
            assert has_negation(sentence), sentence
            assert "unless the episode is stuck" in sentence, sentence


_NO_RELOOK = "No technical design re-look precedes that round unless the episode is stuck."


def test_finalize_failure_round_states_no_relook_unless_stuck() -> None:
    finalize = _flat_section("## 5. Finalize")
    assert _NO_RELOOK in finalize
    assert "fix verification, as in Round 2" not in finalize
    assert not _OPTIONAL_ROUND.search(_NO_RELOOK)


def test_reviewer_contract_does_not_tie_relook_to_round3() -> None:
    reviewer = " ".join(REVIEWER.split())
    tied = [
        s for s in _sentences(reviewer)
        if "Round 3" in s and "technical design re-look" in s
    ]
    assert tied == [], tied


def test_dispatch_profile_does_not_tie_relook_to_round3() -> None:
    profile = (ROOT / "loom-code/references/dispatch-profile.md").read_text(
        encoding="utf-8"
    )
    prose = " ".join(re.sub(r"`[^`]*`", "", profile).split())
    tied = [
        s for s in _sentences(prose)
        if re.search(r"round[- ]3", s, re.IGNORECASE)
        and re.search(r"re-look|redesign", s, re.IGNORECASE)
    ]
    assert tied == [], tied
