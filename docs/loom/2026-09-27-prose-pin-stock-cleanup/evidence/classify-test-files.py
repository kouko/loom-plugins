#!/usr/bin/env python3
"""Census classifier for the prose-pin stock cleanup (W0-01).

Classifies every test file that reads prose (.md) into one of:
  behavior   — executes programs (subprocess/checker/scripts) or imports
               production logic and asserts on it
  structure  — asserts only on document shape (frontmatter, headings,
               section presence, gate markers, JSON keys); no execution,
               no sentence literals
  sentence-pin — asserts exact prose sentences (prose_pin matchers, or
               `in`-style literal checks) with no executable behavior
  grammar-invariant — pins a syntax/grammar rule the checker cannot express
               (gate marker form, version format, matcher self-tests)

A file is a prose reader if it names a .md path. `behavior` wins ties;
`grammar-invariant` wins over `sentence-pin` only for matcher self-tests
and gate-marker grammar, which the plan lists explicitly as retained.

Usage: python3 classify-test-files.py [--roots ...]  (prints a table)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
DEFAULT_ROOTS = ["loom-code/tests", "loom-workflow/tests/scripts", "tests", "loom-design/tests"]

# Program-executing signals (in test functions, not just module-level setup).
# Distinguishes real checker/script execution (returns .returncode, has
# assertions on results) from module-level path resolution setup that merely
# constructs a path string or runs git to find the repo root.
EXECUTE = re.compile(
    r"loom_checker\.py"
    r"|pytest\.raises"
    r"|check_mechanisms\.py|check_doc_citations\.py|check_contract_citations\.py"
    r"|loom_check"
)
# Imports production logic (not the prose_pin matcher, not other tests).
PROD_IMPORT = re.compile(
    r"from (?:loom_checker|scripts|check_|second_vendor|rehearse|dispatch|claude_reviewer|coldread|repo_files|git_exec)\b"
    r"|import (?:loom_checker)\b"
)
PROSE_PIN_IMPORT = re.compile(r"from prose_pin\b|import prose_pin\b")
# Sentence-literal assertions on prose content.
# Matches: assert "literal" in text, assert text == "literal", or prose_pin matcher calls
SENTENCE_ASSERT = re.compile(
    r"assert[^\n]*\b(?:in|==)\s*[\"']"
    r"|pins_exact_sentence\("
    r"|_affirms\(|affirms\(|_stated_once\(|_flat\("
    r"|flat_prose\(|rule_prose\(|split_sentences\("
)
# Structural-only signals (headings, frontmatter, keys, gate markers).
STRUCTURE = re.compile(
    r"startswith\(\"#|## |frontmatter|yaml\.safe_load|json\.loads|\.get\(\"status|\"### |gate: |#+ .*——"
)
# Grammar-invariant signals: pins matcher rules or gate markers specifically.
# Matches: pins the prose_pin matcher rules (adversary.md, engineering-baseline.md),
# gate marker grammar (<!-- gate: -->), version format grammar, or matcher self-tests.
GRAMMAR_INVARIANT_CONTENT = re.compile(
    r"adversary\.md|engineering-baseline\.md|"
    r"prose_pin.*matcher.*rule|matcher.*rule.*prose_pin|"
    r"gate.*marker|<!--\s*gate:|version.*format|"
    r"synthetic.*self-test|self-test.*synthetic"
)


def classify(path: Path) -> tuple[str, dict]:
    """Return (primary_class, secondary_markers)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    has_md = ".md" in text or ".markdown" in text

    if not has_md:
        return "not-prose", {}

    # Check for behavior FIRST (executes programs or imports production logic)
    # Behavior wins ties per the spec
    if EXECUTE.search(text) or PROD_IMPORT.search(text):
        secondary = {}
        # Check for sentence pins (secondary marker for behavior files that also pin prose)
        secondary["has_pins"] = "yes" if (SENTENCE_ASSERT.search(text) and PROSE_PIN_IMPORT.search(text)) else "no"
        # Check if it also has grammar-invariant content (additional marker)
        if GRAMMAR_INVARIANT_CONTENT.search(text):
            secondary["marker"] = "grammar-invariant-content"
        return "behavior", secondary

    # Check for sentence-pin conditions
    is_sentence_pin = PROSE_PIN_IMPORT.search(text) and SENTENCE_ASSERT.search(text)
    # Check for grammar-invariant conditions
    is_grammar_invariant = PROSE_PIN_IMPORT.search(text) and GRAMMAR_INVARIANT_CONTENT.search(text)

    # Check for sentence-pin (imports prose_pin and has sentence assertions, no behavior)
    if is_sentence_pin:
        # grammar-invariant wins over sentence-pin only for matcher self-tests and gate-marker grammar
        if is_grammar_invariant:
            # Check if it's matcher self-tests or gate-marker grammar (the cases where grammar-invariant wins)
            # For now, we'll use the existing GRAMMAR_INVARIANT_CONTENT to detect these cases
            # The plan specifies these are retained as grammar-invariant
            secondary = {}
            secondary["has_pins"] = "yes" if SENTENCE_ASSERT.search(text) else "no"
            if SENTENCE_ASSERT.search(text):
                secondary["note"] = "mixed-grammar-and-pin"
            return "grammar-invariant", secondary
        else:
            # Default case: sentence-pin wins
            secondary = {}
            secondary["has_pins"] = "yes"
            return "sentence-pin", secondary

    # Check for grammar-invariant (when not also sentence-pin, or when sentence-pin doesn't win)
    if is_grammar_invariant:
        secondary = {}
        secondary["has_pins"] = "yes" if SENTENCE_ASSERT.search(text) else "no"
        if SENTENCE_ASSERT.search(text):
            secondary["note"] = "mixed-grammar-and-pin"
        return "grammar-invariant", secondary

    # Check for structure
    if STRUCTURE.search(text):
        return "structure", {}

    return "other", {}


def main() -> int:
    roots = DEFAULT_ROOTS if "--roots" not in sys.argv else sys.argv[sys.argv.index("--roots") + 1:].split(",")
    counts: dict[str, int] = {}
    rows = []  # (file, class, secondary_markers)
    for root in roots:
        for p in sorted((REPO / root).glob("*.py")):
            cls, secondary = classify(p)
            counts[cls] = counts.get(cls, 0) + 1
            if cls in {"sentence-pin", "structure", "grammar-invariant", "behavior"}:
                secondary_str = ", ".join(f"{k}={v}" for k, v in secondary.items()) if secondary else ""
                rows.append((p.relative_to(REPO).as_posix(), cls, secondary_str))

    print(f"{'file':65s} {'class':20s} secondary")
    for f, c, s in rows:
        print(f"{f:65s} {c:20s} {s}")

    print("\ncounts:", dict(sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
