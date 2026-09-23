"""Adversarial probe: a suite-settled row cannot read "works" on a check nobody has run.

Step 6 of the tester's contract makes a suite-settled row cite the suite
command and say `finalize-review` executes it. Two readings slip through:
the contract names no verdict for that row, so "works -- finalize-review runs
the suite" is compliant although nobody tried it; and when `package-tests` is
skipped the contract only says to run that criterion's own tests, leaving the
row still citing a finalize-review suite run that will not happen (and under
a plain-words skip, finalize-review itself does not run).

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-23-lighter-acceptance-testing/evidence/probes/test_suite_settled_row_verdict_and_skip.py -q

concern: overclaimed verdict -- a suite-settled row can say works, or cite a finalize-review run that a skip removes, with no result behind it
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code" / "scripts"))
from prose_pin import flat_prose, has_negation, split_sentences  # noqa: E402

TESTER = REPO / "loom-code" / "agents" / "acceptance-tester.md"
VERDICTS = ("not verified", "works", "partly", "fails")
AFFIRM = r"\b(?:is|gets|marks|reports|records|carries|gives|says|writes)\b"


def _affirms_verdict(sentence: str) -> bool:
    """A sentence about the suite that affirmatively assigns a verdict to the row."""
    if "suite" not in sentence:
        return False
    for verdict in VERDICTS:
        # The verdict must be quoted as a verdict (backticks or double quotes),
        # so the verb "fails" in "refuses ... when it fails" is not a verdict.
        pattern = AFFIRM + r"[^.;]*[`\"]" + re.escape(verdict) + r"[`\"]"
        if re.search(pattern, sentence):
            rest = sentence.replace(f"`{verdict}`", "").replace(verdict, "")
            return not has_negation(rest)
    return False


def _affirms_skip_row(sentence: str) -> bool:
    """A sentence about a skipped package-tests step that affirmatively says what the row carries."""
    if "`package-tests` is skipped" not in sentence:
        return False
    if not re.search(AFFIRM + r"[^.;]*\brow\b|\brow\b[^.;]*" + AFFIRM, sentence):
        return False
    return not has_negation(sentence)


def test_selftest_verdict_affirmative_accepted():
    """Synthetic: an affirmative verdict sentence about a suite row is accepted."""
    assert _affirms_verdict("A row the suite settles is `not verified` until its result exists")


def test_selftest_verdict_negated_rejected():
    """Synthetic: a negated verdict sentence about a suite row is rejected."""
    assert not _affirms_verdict("A row the suite settles never says `works`")


def test_selftest_verdict_unquotedverb_rejected():
    """Synthetic: the verb "fails" in a suite sentence is not a verdict assignment."""
    assert not _affirms_verdict("The row says finalize-review refuses the attestation when the suite fails")


def test_selftest_skiprow_affirmative_accepted():
    """Synthetic: an affirmative skipped-suite row sentence is accepted."""
    assert _affirms_skip_row("When `package-tests` is skipped, the row reports that criterion's own test result")


def test_selftest_skiprow_negated_rejected():
    """Synthetic: a negated skipped-suite row sentence is rejected."""
    assert not _affirms_skip_row("When `package-tests` is skipped, the row does not cite anything")


def _sentences() -> list[str]:
    return split_sentences(flat_prose(TESTER))


def test_suiterow_verdict_isnamed():
    """The contract names the verdict a suite-settled row carries, so works is not the unforced reading."""
    assert [s for s in _sentences() if _affirms_verdict(s)], (
        "tester contract names no verdict for a row that cites the suite instead of a result"
    )


def test_suiterow_packagetestsskipped_saysrowcontent():
    """With package-tests skipped, the contract says what the row carries instead of the finalize-review citation."""
    assert [s for s in _sentences() if _affirms_skip_row(s)], (
        "with `package-tests` skipped the row still cites a finalize-review suite run that will not happen"
    )
