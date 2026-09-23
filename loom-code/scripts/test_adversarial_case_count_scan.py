# concern: the scan that is the whole mechanism against a reintroduced case
# floor reads the bound from a closed list of phrases and the noun from a
# character window, so it misses ordinary English floors and flags sentences
# that state no case count at all.
"""Attack `case_counts` in `loom-code/scripts/test_adversary_protocol.py`.

Two runtime text rules rest on this one function: no runtime file states a
minimum number of cases, and no second file states the ceiling. A phrase the
regex does not list is a floor the repository cannot see; a number the window
attaches to the wrong noun is a legitimate sentence the check refuses.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from test_adversary_protocol import CAP_BOUND  # noqa: E402
from test_adversary_protocol import FLOOR_BOUND  # noqa: E402
from test_adversary_protocol import case_counts  # noqa: E402

# Ordinary English for the bound the intent removed. None of these is exotic;
# each would read naturally in a station, a recipe or an agent contract.
FLOORS_IN_PLAIN_ENGLISH = (
    "write three or more cases",
    "a minimum of three cases",
    "write not fewer than three cases",
    "three probe programs minimum",
    # The wording this change deleted from the READMEs, which a blind run
    # pasted back with the whole suite green: one adjective hides the floor.
    "at least three executable abuse and boundary cases",
)

# Sentences that state no bound on the number of cases at all.
NOT_A_CASE_COUNT = (
    "at least two reviewers read the probe programs",
    "at least one reviewer re-runs every probe program of the change",
)


def test_case_counts_a_floor_in_plain_english_is_read_as_a_floor() -> None:
    """A rule the check cannot read is a rule the repository does not have."""
    missed = [text for text in FLOORS_IN_PLAIN_ENGLISH
              if not any(bound == FLOOR_BOUND for bound, _ in case_counts(text))]
    assert missed == []


def test_case_counts_a_count_of_readers_is_not_a_count_of_cases() -> None:
    """The noun window reaches sixty characters forward, so a number counting
    something else lands on the first case noun that follows it."""
    misread = {text: sorted(case_counts(text)) for text in NOT_A_CASE_COUNT
               if case_counts(text)}
    assert misread == {}


def test_case_counts_the_known_wordings_still_read_correctly() -> None:
    """The control: what the check already reads must keep reading the same,
    so a fix is not a loosening."""
    assert case_counts("write at least three cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("a change commits at most five probe programs") == {(CAP_BOUND, 5)}
    assert case_counts("至少三個可執行的邊界案例") == {(FLOOR_BOUND, 3)}
    assert case_counts("実行可能な境界ケース 3 つ以上を書く") == {(FLOOR_BOUND, 3)}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
