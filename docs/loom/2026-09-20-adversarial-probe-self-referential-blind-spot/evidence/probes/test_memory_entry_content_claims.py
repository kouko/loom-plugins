"""Adversarial probes for `2026-09-20-adversarial-probe-self-referential-blind-spot`.

The change adds exactly one memory entry (plus a regenerated `index.md`) to
`docs/loom/memory/`. That artifact type has no adversary recipe today
(`loom-code/skills/closing-review/references/adversarial.md`'s routing table
rows `memory` to `none`), so this file attacks it with the shared protocol
alone: nothing here follows a recipe, because no recipe exists.

`loom_memory.py validate` only checks the store's MECHANICAL shape --
frontmatter presence, `name`/filename identity, index drift. It asserts
nothing about whether an entry's prose actually says what its own Acceptance
criteria require (the plan's own Current State Evidence says so: "no test
asserts the truth of an entry's content"). That gap is this file's target,
because it is exactly the class of gap the entry itself is warning about --
a check that goes green without ever exercising the claim it stands for.

Cases:

* the real store (not a synthetic fixture) validates clean -- the generic
  mechanism is already proven correct against synthetic fixtures by
  `loom-workflow/skills/loom-memory/scripts/test_loom_memory.py` (reused,
  not re-proven here); what that suite cannot catch is a violation specific
  to THIS store's actual content, such as this entry colliding with an
  existing name or leaving `index.md` stale;
* the new entry's frontmatter satisfies Acceptance 1 (filename/name
  identity) and Acceptance 4 (sources cites the originating change) in
  isolation, so an unrelated future entry's violation cannot mask this one
  going stale;
* the description states the durable rule and never names a specific tool,
  file, or function (Acceptance 2) -- checked as an absence probe, since a
  later edit naming e.g. a script path would violate the store's own rule
  silently (nothing else checks this);
* the body actually names both concrete manifestations, and states they
  were caught by real execution rather than by reading (Acceptance 3) --
  pinned with an affirmative-verb-before-literal / same-clause-negation
  check in both directions, because a same-sentence negation ("never
  surfaced when...") would otherwise satisfy a naive substring match while
  asserting the opposite of what Acceptance 3 requires; each direction
  carries a synthetic self-test proving the check accepts the true polarity
  and rejects the flipped one;
* the entry's two `[[wikilink]]` cross-references resolve to files that
  exist in the store -- `loom_memory.py` never checks this link shape (only
  `index.md`'s own `[name](file)` lines), so nothing else would catch a
  dangling one;
* the `sources` citation actually corroborates: the probe file it names
  (`test_modular_recipes_abuse.py`, itself only readable after flattening
  its own line-wrapped docstrings -- the exact same whitespace trap this
  repo's memory store already records) really does describe both original
  defects, not just share a filename with the change being cited.

Every literal pinned against real prose is matched against a
whitespace-flattened copy of the text
(`docs/loom/memory/a-prose-literal-assertion-is-false-green-until-it-flattens-whitespace.md`):
this file's own two source documents wrap their prose across lines, so an
un-flattened substring search would silently miss a real, present phrase
and report the wrong kind of failure (or, for an absence check, silently
pass for the wrong reason).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "loom-code").is_dir() and (candidate / "loom-design").is_dir():
            return candidate
    raise RuntimeError(f"could not locate repo root above {start}")


REPO = _find_repo_root(Path(__file__).parent)
MEMORY_STORE = REPO / "docs/loom/memory"
ENTRY_PATH = MEMORY_STORE / "an-adversarial-probe-can-go-green-by-excluding-what-would-refute-it.md"
CORROBORATING_PROBE_PATH = (
    REPO
    / "docs/loom/2026-09-18-modular-adversary-recipes/evidence/probes/test_modular_recipes_abuse.py"
)

sys.path.insert(0, str(REPO / "loom-workflow/skills/loom-memory/scripts"))
import loom_memory as lm  # noqa: E402


# ---------------------------------------------------------------------------
# Flattening + clause-scoped negation helpers
# ---------------------------------------------------------------------------


def _flatten(text: str) -> str:
    """Collapse all whitespace runs to a single space so a multi-word phrase
    that happens to wrap across a markdown or docstring line becomes a
    contiguous substring again."""
    return re.sub(r"\s+", " ", text)


NEGATION_PATTERNS = [
    r"\bnot\b",
    r"n't\b",
    r"\bnever\b",
    r"\bcannot\b",
    r"\bno\b",
    r"\bneither\b",
    r"\bnor\b",
    r"\bwithout\b",
    r"\bfails? to\b",
    r"\bfailed to\b",
]


def _has_negation(clause: str) -> bool:
    return any(re.search(pattern, clause) for pattern in NEGATION_PATTERNS)


def _clauses(flattened_text: str) -> list[str]:
    """Split flattened prose at sentence-enders and em/double-hyphen dashes.

    A dash-joined compound sentence can carry two claims of OPPOSITE
    polarity in one grammatical sentence -- this very entry's own body does
    it ("neither was found by reading ... -- they surfaced only when a
    blind-run reader performed ..."). Splitting only on periods would put a
    negated clause and the affirmative clause that follows it in one span,
    which defeats a same-clause negation check in both directions. A colon
    introducing a markdown list item is the same trap in the other
    direction: this entry's lead-in clause ("... because the probe itself
    chose what its own run would exclude or cover:") carries a negation
    ("could not have seen") that has nothing to do with the affirmative
    bullet that follows it, so a colon splits too.
    """
    return [c.strip() for c in re.split(r"[.;:]|--|—", flattened_text) if c.strip()]


def _clause_containing(clauses: list[str], literal: str) -> str | None:
    for clause in clauses:
        if literal in clause:
            return clause
    return None


def _assert_affirmative_claim(text: str, literal: str) -> None:
    """Require some clause to contain `literal` (an affirmative verb sitting
    immediately before the pinned wording) with no negation token sharing
    that clause -- otherwise a sentence that DENIES the exact same wording
    would satisfy a bare substring check and the probe would report a claim
    true that the prose actually contradicts."""
    clause = _clause_containing(_clauses(_flatten(text)), literal)
    assert clause is not None, f"no clause contains the affirmative literal {literal!r}"
    assert not _has_negation(clause), (
        f"clause containing {literal!r} also carries a negation token, so it does not "
        f"affirm the claim: {clause!r}"
    )


def _assert_negated_claim(text: str, literal: str) -> None:
    """The mirror check, for a claim the prose is supposed to DENY: require
    some clause containing `literal` to also carry a negation token."""
    clause = _clause_containing(_clauses(_flatten(text)), literal)
    assert clause is not None, f"no clause contains the literal {literal!r}"
    assert _has_negation(clause), (
        f"clause containing {literal!r} carries no negation token, so the prose affirms "
        f"rather than denies it: {clause!r}"
    )


# ---------------------------------------------------------------------------
# Synthetic self-tests for the two helpers -- required before trusting them
# against real prose, per this same change's own "How to apply" clause.
# ---------------------------------------------------------------------------


def test_assert_affirmative_claim_accepts_a_true_affirmative_example():
    _assert_affirmative_claim(
        "It surfaced only when a blind-run reader performed the check for real.",
        "surfaced only when a blind-run reader performed",
    )


def test_assert_affirmative_claim_rejects_a_negated_example():
    with pytest.raises(AssertionError):
        _assert_affirmative_claim(
            "It never surfaced when a blind-run reader performed the check for real.",
            "surfaced when a blind-run reader performed",
        )


def test_assert_negated_claim_accepts_a_true_negated_example():
    _assert_negated_claim(
        "The defect was not found by reading the probe's code.",
        "found by reading the probe's code",
    )


def test_assert_negated_claim_rejects_an_affirmed_example():
    with pytest.raises(AssertionError):
        _assert_negated_claim(
            "The defect was found by reading the probe's code.",
            "found by reading the probe's code",
        )


# ---------------------------------------------------------------------------
# Acceptance 5 -- the real store (not a synthetic fixture) validates clean
# ---------------------------------------------------------------------------


def test_real_memory_store_validates_with_no_violations():
    violations = lm.validate_bundle(MEMORY_STORE)
    assert violations == [], [v.render() for v in violations]


def test_entry_frontmatter_alone_is_violation_free():
    """Acceptance 1, isolated to this one file so a future entry's own
    violation elsewhere in the store cannot mask this one going stale."""
    violations = lm._validate_concept_file(ENTRY_PATH)
    assert violations == [], [v.render() for v in violations]


# ---------------------------------------------------------------------------
# Acceptance 4 -- sources cites the originating change
# ---------------------------------------------------------------------------


def test_entry_sources_cites_the_originating_commit_pr_and_change():
    frontmatter = lm.parse_frontmatter(ENTRY_PATH.read_text(encoding="utf-8"))
    sources = frontmatter["sources"]
    assert isinstance(sources, list) and sources
    resource = sources[0]["resource"]
    for literal in ("9bf87029", "PR #33", "2026-09-18-modular-adversary-recipes"):
        assert literal in resource, f"sources[0].resource is missing {literal!r}: {resource!r}"


# ---------------------------------------------------------------------------
# Acceptance 2 -- description is tool-agnostic
# ---------------------------------------------------------------------------


def test_entry_description_names_the_durable_rule():
    frontmatter = lm.parse_frontmatter(ENTRY_PATH.read_text(encoding="utf-8"))
    description = frontmatter["description"]
    assert "population" in description
    assert "deselects" in description


def test_entry_description_never_names_a_specific_tool_file_or_function():
    frontmatter = lm.parse_frontmatter(ENTRY_PATH.read_text(encoding="utf-8"))
    description = frontmatter["description"]
    assert "`" not in description, "description quotes a code span: " + description
    assert not re.search(r"\.(py|sh|yaml|yml)\b", description), description
    assert "test_modular_recipes_abuse" not in description
    assert "_manifest_types" not in description
    assert "9bf87029" not in description


# ---------------------------------------------------------------------------
# Acceptance 3 -- both concrete manifestations, named as evidence
# ---------------------------------------------------------------------------


def test_entry_body_names_the_deselect_in_nested_run_manifestation():
    body = ENTRY_PATH.read_text(encoding="utf-8")
    _assert_affirmative_claim(body, "deselects the cases that copy the repository")


def test_entry_body_states_the_flawed_probe_could_not_see_the_routing_row_defect():
    """The manifestation's actual consequence, phrased as a denial on
    purpose (a probe that WAS able to see the defect would not be the
    defect being recorded) -- flipping this to an affirmed claim would
    silently reverse the entry's meaning."""
    body = ENTRY_PATH.read_text(encoding="utf-8")
    _assert_negated_claim(body, "see the defect a missing routing row would cause")


def test_entry_body_names_the_alphabetically_first_population_manifestation():
    body = ENTRY_PATH.read_text(encoding="utf-8")
    _assert_affirmative_claim(body, "computed as the alphabetically-first unrouted artifact type")


def test_entry_body_states_that_candidate_could_not_trigger_the_name_collision_defect():
    body = ENTRY_PATH.read_text(encoding="utf-8")
    _assert_negated_claim(
        body, "trigger the name-collision defect that was actually present for other kinds"
    )


def test_entry_body_states_execution_caught_the_defects_affirmatively():
    body = ENTRY_PATH.read_text(encoding="utf-8")
    _assert_affirmative_claim(body, "surfaced only when a blind-run reader performed")


def test_entry_body_states_reading_code_or_the_diff_did_not_catch_them():
    body = ENTRY_PATH.read_text(encoding="utf-8")
    _assert_negated_claim(body, "found by reading the probe's code or the diff")


# ---------------------------------------------------------------------------
# `[[wikilink]]` cross-references -- loom_memory.py never checks this shape
# ---------------------------------------------------------------------------


def test_entry_wikilinks_resolve_to_files_that_exist_in_the_store():
    body = ENTRY_PATH.read_text(encoding="utf-8")
    targets = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", body)
    assert targets, "entry has no [[wikilink]] cross-references to check"
    for target in targets:
        candidate = MEMORY_STORE / f"{target}.md"
        assert candidate.is_file(), f"[[{target}]] does not resolve to {candidate}"


def test_loom_memory_validate_does_not_check_wikilink_targets():
    """Documents why the probe above exists rather than being redundant with
    `validate`: a dangling `[[wikilink]]` is invisible to the mechanical
    gate, so this store-wide sweep must never regress a linked concept's
    filename without this probe catching it. `INDEX_LINK_LINE_RE` matches
    only `index.md`'s generated `[name](file)` line shape, never a
    double-bracket `[[wikilink]]` written in a concept body."""
    import inspect

    source = inspect.getsource(lm)
    assert "wikilink" not in source.lower()
    assert r"\[\[" not in source, "loom_memory.py would need a [[wikilink]] pattern to check this"


# ---------------------------------------------------------------------------
# The `sources` citation actually corroborates (not just names a real file)
# ---------------------------------------------------------------------------


def test_corroborating_probe_file_actually_describes_the_deselect_manifestation():
    text = _flatten(CORROBORATING_PROBE_PATH.read_text(encoding="utf-8"))
    assert "deselects the cases that copy the repository" in text


def test_corroborating_probe_file_actually_describes_the_population_manifestation():
    text = _flatten(CORROBORATING_PROBE_PATH.read_text(encoding="utf-8"))
    assert "alphabetically first unrouted kind proves the claim for that kind and no other" in text
