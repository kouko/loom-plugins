import re
from pathlib import Path

from prose_pin import has_negation, split_sentences


ROOT = Path(__file__).resolve().parents[2]
REVIEW = (ROOT / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
# The attack protocol's own structure is checked in test_adversary_protocol.py
# (a one-home scan and the return-block keys; its wording is not pinned); this
# module keeps the station's text.
REVIEWER = (ROOT / "loom-code/agents/reviewer.md").read_text(encoding="utf-8")
REVIEW_WORDS = " ".join(REVIEW.split())
CONTRACT = " ".join((REVIEW + "\n" + REVIEWER).split())


def test_review_episode_has_three_distinct_content_rounds_and_no_identity_reset() -> None:
    assert "<!-- gate: review.bounded-episode -->" in REVIEW
    assert "<!-- /gate -->" in REVIEW


def test_contract_adds_no_review_round_ledger_or_schema() -> None:
    forbidden = ("review-round.json", "rounds.json", "review_episode.json")
    assert not any(name in CONTRACT for name in forbidden)


def _sentences(text: str) -> list[str]:
    return split_sentences(text, ends=".:;")  # colon is a boundary here


_COMMIT_AFTER_VERDICTS = re.compile(
    r"\bcommit (?:that|the|its) (?:acceptance[- ]test )?report\b[^.]*\bafter\b"
    r"|\bafter\b[^.]*\b(?:verdicts?|reviewers? (?:read|return))\b[^.]*\bcommit (?:that|the|its) (?:acceptance[- ]test )?report\b",
    re.IGNORECASE,
)


def test_report_commit_after_verdicts_not_instructed() -> None:
    assert _COMMIT_AFTER_VERDICTS.search("After the verdicts arrive, commit the acceptance test report.")
    assert _COMMIT_AFTER_VERDICTS.search("Commit that report after reviewers return.")
    assert not _COMMIT_AFTER_VERDICTS.search("A report committed after their verdicts needs the next round.")
    offending = [s for s in _sentences(REVIEW_WORDS) if _COMMIT_AFTER_VERDICTS.search(s)]
    assert offending == []


def test_finalize_before_report_commit_not_instructed() -> None:
    finalize_then_commit = re.compile(
        r"finaliz\w*.*\b(then|afterwards?|later)\b.*commit\w*.*acceptance test report"
        r"|commit\w*.*acceptance test report.*\b(after|once)\b.*finaliz",
        re.IGNORECASE,
    )
    offending = [s for s in _sentences(REVIEW_WORDS) if finalize_then_commit.search(s)]
    assert offending == []


# ---------------------------------------------------------------------------
# Acceptance A5 — the recording passage at the end of convergence stays inert.
# Its wording (timing, digest limit, scarcity bar) is read by closing review.
# ---------------------------------------------------------------------------


def _recording_passage() -> str:
    """The whole passage between the convergence gate's close and Finalize.

    Selecting one `\n\n` block was a real gap: the scarcity paragraph sat
    outside it, so a plugin name or a gate marker could be added there with
    every test staying green. Acceptance 5 is a property of the passage.
    """
    finalize = REVIEW.index("\n## 5. Finalize")
    closes_episode = REVIEW.rindex("<!-- /gate -->", 0, finalize)
    return REVIEW[closes_episode + len("<!-- /gate -->") : finalize]


def test_recording_passage_invokes_nothing_and_registers_no_mechanism() -> None:
    """The whole passage must stay inert: no plugin name, no tool call, and no
    gate marker anywhere in it, so the mechanism count is unchanged."""
    passage = _recording_passage()
    assert "<!-- gate:" not in passage, (
        "the passage must not be marked as a gate: the charter forbids a "
        "prose-only gate, and its criterion is a judgement."
    )
    for plugin in ("loom-memory", "loom-workflow", "git-memory"):
        assert plugin not in passage, (
            f"the passage must not name {plugin!r}; it points at a store path "
            "that can be checked for existence, not at an install."
        )
    for invocation in ("Invoke", "invoke the", "Use `"):
        assert invocation not in passage, (
            f"the passage must not instruct an invocation ({invocation!r}); "
            "#821 REQ-4 forbids a station calling memory by virtue of being "
            "reached."
        )


# ---------------------------------------------------------------------------
# 2026-09-15-mechanical-checks-before-review — acceptance 3, 6, 7
# ---------------------------------------------------------------------------

def _flat_section(heading: str) -> str:
    return " ".join(REVIEW.split(heading, 1)[1].split("\n## ", 1)[0].split())


_EARLY_DISPATCH = re.compile(
    r"\b(?:while|during|in parallel|still run\w*|under time pressure)\b", re.IGNORECASE
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
# dispatched until Build's checks are confirmed — and the scan below checks
# that no sentence naming either antecedent dispatches a reviewer.
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
    assert _AFFIRMATIVE_DISPATCH.search("When an item is absent, dispatch the reviewers anyway.")
    assert not _AFFIRMATIVE_DISPATCH.search(
        "When it is another station, return the change there and dispatch no reviewer."
    )


def test_reviewers_dispatched_after_build_checks() -> None:
    depth = _flat_section("## 2. Compute review depth")
    # Neither branch may dispatch a reviewer.
    for sentence in _sentences(depth):
        if _BRANCH_ANTECEDENT.search(sentence):
            assert not _AFFIRMATIVE_DISPATCH.search(sentence), sentence

    assert _early_dispatch_sentences(REVIEW_WORDS) == []


def test_no_adversary_dispatch_in_closing_review() -> None:
    assert "loom-code:adversary" not in REVIEW
    assert "adversary dispatch" not in REVIEW_WORDS
    assert "create committed adversarial programs" not in REVIEW_WORDS
    assert "Run blind and adversarial checks" not in REVIEW
    for sentence in _sentences(REVIEW_WORDS):
        if re.search(r"\badversary\b", sentence):
            assert has_negation(sentence), sentence


def test_earlier_verdicts_not_reused() -> None:
    for sentence in _sentences(REVIEW_WORDS):
        if re.search(r"\breus(?:e|ed|es|ing)\b", sentence, re.IGNORECASE):
            assert has_negation(sentence), sentence
    rerun_with_old = re.compile(
        r"\b(?:re-?run|run)\b[^.]*`finalize-review`[^.]*\b(?:same|earlier|previous|existing|prior) verdicts",
        re.IGNORECASE,
    )
    assert not [s for s in _sentences(REVIEW_WORDS) if rerun_with_old.search(s)]


# ---------------------------------------------------------------------------
# 2026-09-15-station-gaps-after-dogfood — acceptance 2
# ---------------------------------------------------------------------------

def _round_three_bullet() -> str:
    start = REVIEW.index("- **Round 3")
    return " ".join(REVIEW[start:].split("\n\n", 1)[0].split())


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
