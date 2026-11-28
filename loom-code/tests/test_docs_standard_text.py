"""The docs standard is the one text writer and judge read for prose rules.

`loom-code/references/docs-standard.md` holds the rules docs, SKILL.md,
references and rule text are written to; engineering-baseline.md and the
closing-review docs-lens rows point to it instead of restating it. Pins
follow the prose-pin rule: an affirmative verb before the pinned literal, no
negation token in that sentence, and synthetic self-tests for one
affirmative and one negated example. A rule sentence carrying its own
negation is pinned whole instead.
"""
from __future__ import annotations

from pathlib import Path

from prose_pin import affirms, flat_prose, pins_exact_sentence, rule_prose

REPO = Path(__file__).resolve().parents[2]
STANDARD = REPO / "loom-code/references/docs-standard.md"
BASELINE = REPO / "loom-code/references/engineering-baseline.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"
LENS_CITE = "`../../../references/docs-standard.md`"
DOCS_DIMENSIONS = (
    "omission", "ambiguity", "inconsistency", "incorrect-fact", "missing-population", "deletion-first",
)

# One literal per moved rule; each lives in the standard only.
MOVED_RULES = (
    "a required diagram or comparison table missing",
    "a sentence with two live readings that fork what the executor does",
    "the delta says X and an untouched paragraph still says not-X",
    "A measured number with no denominator or scope",
    "compare each such sentence with its new form",
    "must ↔ may, never ↔ always, forbid ↔ allow",
    "names the already-observed failure it prevents",
    "raised in the same file across two consecutive changes is a design smell",
)
# Every rule sentence, pinned whole: a count-only pin lets "is a finding"
# flip to "is not a finding" unseen.
RULE_SENTENCES = (
    "An obligation or referent the text needs and lacks is a finding: a step the reader cannot execute, "
    "a term used but never defined, a promised section absent, a required diagram or comparison table "
    "missing (or declared not-applicable for a reason the text's own content contradicts).",
    'An absolute — "only", "never", "zero" — with no support is a finding, and so is a sentence with '
    "two live readings that fork what the executor does.",
    "Two passages contradicting is a finding, including changed against unchanged: the delta says X and "
    "an untouched paragraph still says not-X.",
    "A citation that does not support its claim is a finding, and so is a stated number or path that is "
    "wrong against the artifact it describes.",
    'A measured number with no denominator or scope is a finding: "0% false positives" without saying '
    "over what.",
    "This sharpens §3 for changed against base.",
    "When a change deletes or rewrites a sentence carrying a polarity word, read the base version with "
    "`git show <base>:<path>` and compare each such sentence with its new form.",
    "Polarity words are never, must not, only, always, 不得 and their kin (no, do not, may not, forbid, "
    "禁止, 絕不).",
    "A reversed direction, or a polarity clause dropped with nothing else in the delta or the unchanged "
    "tree carrying it, is an `inconsistency` finding.",
    "A reversed direction is must ↔ may, never ↔ always, forbid ↔ allow;",
    "a rewording that keeps the direction is not a finding.",
    "A new paragraph, mechanism, reserved task or fallback path in station text or a contract shows in "
    "the delta what it replaced, or names the already-observed failure it prevents by citing a concrete "
    "failure or a `docs/loom/memory` entry — otherwise it is a finding, and the finding names the "
    "smaller shape that does the same job.",
    "This is the rule [`code-design-standard.md`](code-design-standard.md) §2–3 states for code, applied "
    "to station text and agent contracts.",
    "A `*_CAP` constant raised in the same file across two consecutive changes is a design smell: the "
    "`deletion-first` dimension always names at least one deletion candidate for that file, standing "
    "until it is rebutted with evidence.",
)
LENS_SECTIONS = dict(zip(DOCS_DIMENSIONS, ("§1", "§2", "§3", "§4", "§5", "§7")))


def _owned_by_standard(rule: str, standard: str, *others: str) -> bool:
    return standard.count(rule) == 1 and all(rule not in other for other in others)


def _polarity_rule(text: str) -> bool:
    return affirms(text, "read the base version", "compare each such sentence with its new form") and affirms(
        text, "A reversed direction", "is an `inconsistency` finding", "polarity clause dropped"
    )


def _baseline_points(text: str) -> bool:
    return affirms(
        text, "Read", "docs-standard.md", "SKILL.md", "rule text", "the reviewer judges that prose against it"
    )


def _docs_rows() -> dict[str, str]:
    text = LENSES.read_text(encoding="utf-8")
    start = text.index("## Docs")
    section = text[start:text.index("\n## ", start + 1)]
    return {
        line.split("|")[1].strip(): line
        for line in section.splitlines()
        if line.startswith("| ") and line.split("|")[1].strip() in DOCS_DIMENSIONS
    }


def test_standard_exists_and_is_cited() -> None:
    """A1 positive (docs-standard-exists): lenses and the baseline cite the standard."""
    assert STANDARD.is_file()
    assert LENS_CITE in LENSES.read_text(encoding="utf-8")
    assert _baseline_points(rule_prose(BASELINE))


def test_baseline_matcher_rejects_missing_pointer() -> None:
    """A1 negative (missing), on synthetic text."""
    pointer = (
        "Read [`docs-standard.md`](docs-standard.md) before writing docs, a SKILL.md, a reference or "
        "rule text: the reviewer judges that prose against it."
    )
    assert _baseline_points(pointer)
    assert not _baseline_points("Docs and SKILL.md files are reviewed as rule text.")
    assert not _baseline_points(pointer.replace("Read", "Do not read"))


def test_polarity_rule_once_in_standard() -> None:
    """A2 positive (polarity-rule-once): the moved rules live in the standard alone."""
    standard, baseline, lenses = flat_prose(STANDARD), flat_prose(BASELINE), flat_prose(LENSES)
    for rule in MOVED_RULES:
        assert _owned_by_standard(rule, standard, baseline, lenses), rule
    sentences = rule_prose(STANDARD)
    for sentence in RULE_SENTENCES:
        assert pins_exact_sentence(sentences, sentence), sentence


def test_owned_matcher_rejects_polarity_rule_in_lenses() -> None:
    """A2 negative (polarity-rule-in-lenses), on synthetic text."""
    rule = MOVED_RULES[5]
    assert _owned_by_standard(rule, f"A reversed direction is {rule}.", "lens cites the standard")
    assert not _owned_by_standard(rule, f"A reversed direction is {rule}.", f"lens restates {rule}")
    assert not _owned_by_standard(rule, "", "lens cites the standard")


def test_five_dimensions_and_polarity_kept() -> None:
    """A9 positive (five-dimensions-and-polarity-kept): rows cite the standard; polarity stays a finding."""
    rows = _docs_rows()
    for name, section in LENS_SECTIONS.items():
        assert f", judged against {LENS_CITE} {section}" in rows[name], name  # "no population" bars affirms
    assert f"every changed sentence carrying a polarity word is judged against {LENS_CITE} §6" in flat_prose(LENSES)
    assert _polarity_rule(rule_prose(STANDARD))


def test_polarity_matcher_rejects_negated() -> None:
    """A9 negative (polarity-negated), on synthetic text."""
    text = (
        "When a change deletes or rewrites a sentence carrying a polarity word, read the base version "
        "and compare each such sentence with its new form. A reversed direction, or a polarity clause "
        "dropped with nothing else carrying it, is an `inconsistency` finding."
    )
    assert _polarity_rule(text)
    assert not _polarity_rule(text.replace("is an `inconsistency`", "is not an `inconsistency`"))


def test_reviewer_dimension_names_unchanged() -> None:
    """A9 boundary (reviewer-dimension-names-unchanged): the lens table keys match reviewer.md."""
    assert tuple(_docs_rows()) == DOCS_DIMENSIONS
    reviewer = (REPO / "loom-code/agents/reviewer.md").read_text(encoding="utf-8")
    assert f"| `docs` | {', '.join(DOCS_DIMENSIONS)} |" in reviewer
