"""W1-03 — adversary.md and engineering-baseline.md state the prose-pin
rule: a test that pins a sentence of prose requires an affirmative verb
before the pinned literal, rejects any negation token in that same
sentence, and carries synthetic self-tests.

Mirrors test_language_station_text.py's negation-aware matcher shape:
resolve REPO via `git rev-parse`, read each file, split into sentences,
and assert one sentence carries the required affirmative-verb-then-
keyword shape with no negation token anywhere in the sentence.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

_REPO_RESULT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True,
    text=True,
    check=True,
)
REPO = Path(_REPO_RESULT.stdout.strip())

ADVERSARY_MD = REPO / "loom-code" / "agents" / "adversary.md"
BASELINE_MD = REPO / "loom-code" / "references" / "engineering-baseline.md"

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
from prose_pin import NEGATION_RE as _NEGATION_RE  # shared matcher, one place to widen
_AFFIRM_VERB_RE = re.compile(r"\b(require|requires|must|is|are|asserts)\b")
_AFFIRM_KW_RE = re.compile(r"\baffirmative(ly)?\b")
_NEGATION_KW_RE = re.compile(r"\bnegat(?:ion|ed)\b")
_SELFTEST_KW_RE = re.compile(r"\b(self-test|synthetic)\b")


def _sentences(text: str) -> list[str]:
    """Split text into sentences after collapsing newlines to spaces —
    same normalization test_language_station_text.py uses, so a sentence
    that line-wraps in the source still reads as one unit here."""
    flat = " ".join(text.split())
    return [p for p in _SENTENCE_SPLIT.split(flat) if p.strip()]


def _has_negation(sentence: str) -> bool:
    """True iff `sentence` contains a word-boundary negation token — 'not',
    'never' or 'no' as whole words, or an "n't" contraction."""
    return bool(_NEGATION_RE.search(sentence))


def _sentence_pins_prose_rule(sentence: str) -> bool:
    """True iff `sentence` (lowercased for keyword matching) names
    "affirmative"/"affirmatively", "negation"/"negated", and "self-test"/
    "synthetic", has one of the affirmative verb forms
    (require/requires/must/is/are/asserts) BEFORE the earliest of those
    three keyword hits, and carries no negation token anywhere in the
    sentence."""
    low = sentence.lower()
    m_affirm = _AFFIRM_KW_RE.search(low)
    m_negation = _NEGATION_KW_RE.search(low)
    m_selftest = _SELFTEST_KW_RE.search(low)
    if not (m_affirm and m_negation and m_selftest):
        return False
    first_kw_idx = min(m_affirm.start(), m_negation.start(), m_selftest.start())
    if not _AFFIRM_VERB_RE.search(low[:first_kw_idx]):
        return False
    return not _has_negation(sentence)


def test_adversarymd_prosepinsentence_present() -> None:
    """adversary.md must carry one sentence pinning the prose-pin rule
    (affirmative verb before affirmative/negation/self-test vocabulary,
    no negation token anywhere in that sentence)."""
    text = ADVERSARY_MD.read_text(encoding="utf-8")
    hits = [s for s in _sentences(text) if _sentence_pins_prose_rule(s)]
    assert hits, (
        "loom-code/agents/adversary.md has no sentence pinning the "
        "prose-pin rule"
    )


def test_engineeringbaselinemd_prosepinsentence_present() -> None:
    """engineering-baseline.md must carry one sentence pinning the
    prose-pin rule (affirmative verb before affirmative/negation/
    self-test vocabulary, no negation token anywhere in that sentence)."""
    text = BASELINE_MD.read_text(encoding="utf-8")
    hits = [s for s in _sentences(text) if _sentence_pins_prose_rule(s)]
    assert hits, (
        "loom-code/references/engineering-baseline.md has no sentence "
        "pinning the prose-pin rule"
    )


def test_sentencepinsproserule_negatedsynthetic_rejected() -> None:
    """Self-test on `_sentence_pins_prose_rule`: a negated synthetic
    sentence carrying all three keyword groups must be rejected, and an
    affirmative synthetic sentence carrying the same three keyword groups
    must be accepted — otherwise the two tests above could be satisfied
    by a sentence that FORBIDS the rule rather than requiring it."""
    affirmative = (
        "A prose-pin rule requires an affirmative sentence verified "
        "through a self-test against a synthetic negated example."
    )
    assert _sentence_pins_prose_rule(affirmative), (
        "a genuinely affirmative synthetic sentence must pass"
    )

    negated = (
        "A prose-pin rule does not require an affirmative sentence, and "
        "skips both the self-test and the synthetic negated example."
    )
    assert not _sentence_pins_prose_rule(negated), (
        "a negated synthetic sentence must be rejected even though it "
        "names all three keyword groups"
    )


# --- W1-03: amend an unseen probe fix into its original commit -------------

_AMEND_KW_RE = re.compile(r"\bamend(?:ed|s)?\b")
_UNSEEN_KW_RE = re.compile(r"\bunseen\b")
_PROBE_KW_RE = re.compile(r"\bprobes?\b")
_COMMIT_KW_RE = re.compile(r"\bcommit\b")


def _sentence_pins_unseen_probe_amend_rule(sentence: str) -> bool:
    """True iff `sentence` names "amend"/"amended", "unseen", "probe"/
    "probes" and "commit", with the amend verb appearing BEFORE the probe
    literal it amends, and carries no negation token anywhere in the
    sentence."""
    low = sentence.lower()
    m_amend = _AMEND_KW_RE.search(low)
    m_unseen = _UNSEEN_KW_RE.search(low)
    m_probe = _PROBE_KW_RE.search(low)
    m_commit = _COMMIT_KW_RE.search(low)
    if not (m_amend and m_unseen and m_probe and m_commit):
        return False
    if m_amend.start() >= m_probe.start():
        return False
    return not _has_negation(sentence)


def test_adversarymd_unseenprobefixsentence_present() -> None:
    """adversary.md must carry one sentence stating that a fix to its own
    probe, not yet seen by any reader, is amended into that probe's
    original commit rather than becoming a new one."""
    text = ADVERSARY_MD.read_text(encoding="utf-8")
    hits = [s for s in _sentences(text) if _sentence_pins_unseen_probe_amend_rule(s)]
    assert hits, (
        "loom-code/agents/adversary.md has no sentence pinning the "
        "unseen-probe-fix-amend rule"
    )


def test_sentencepinsunseenprobeamendrule_negatedsynthetic_rejected() -> None:
    """Self-test on `_sentence_pins_unseen_probe_amend_rule`: an
    affirmative synthetic sentence carrying all four keywords in the
    required order must be accepted, and a negated synthetic sentence
    carrying the same four keywords must be rejected."""
    affirmative = (
        "Amend a fix to an unseen probe into its original commit."
    )
    assert _sentence_pins_unseen_probe_amend_rule(affirmative), (
        "a genuinely affirmative synthetic sentence must pass"
    )

    negated = (
        "Never amend a fix to an unseen probe into its original commit."
    )
    assert not _sentence_pins_unseen_probe_amend_rule(negated), (
        "a negated synthetic sentence must be rejected even though it "
        "names all four keywords in the required order"
    )


def test_engineeringbaselinemd_codefirstbackfill_present() -> None:
    """A user-instructed `tdd` skip for code written before the flow is
    characterised first and its scope recorded (A1); an uninstructed skip
    stays a violation, later code follows the iron law, and a compile
    failure proves only a missing interface (A2). The legacy paragraph it
    extends stays. Each sentence is pinned exactly: a keyword-subset pin
    admits a clause that reverses the rule without a negation word."""
    from prose_pin import affirms, flat_prose, pins_exact_sentence, rule_prose

    text = rule_prose(BASELINE_MD)
    for sentence in (
        "**Code-first backfill.** When the user instructs a `tdd` skip in "
        "plain words for code written before the flow began "
        "(`skipped-by-instruction: tdd <date>`), the backfill characterises "
        "that code first — pin its current behaviour, bugs included — before "
        "changing it, and the plan records which code predates the flow in "
        "its `## Risks`, beside the skip line, or the intent's "
        "`## Constraints` does when plan is absent or skipped.",
        "If it did and was skipped, it is a violation whatever the code's "
        "age, unless the user instructed the skip (Code-first backfill, below).",
        "An uninstructed skip remains a violation.",
        "Code written after the flow began follows the iron law.",
        "A compile or import failure proves only that an interface is missing;",
        "break the covered behaviour and watch the test fail (false-green "
        "diagnostic) to show it catches a defect.",
    ):
        assert pins_exact_sentence(text, sentence), sentence
    assert affirms(text, "is", "violation whatever the code's age")
    build = flat_prose(REPO / "loom-code" / "skills" / "build" / "SKILL.md")
    assert (
        "Unless `tdd` is skipped by the user's plain-words instruction — a skip "
        "that covers only code written before the flow began "
        "([engineering-baseline.md](../../references/engineering-baseline.md), "
        "Code-first backfill) — for every behavior change:"
    ) in build


if __name__ == "__main__":  # pragma: no cover
    import sys
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
