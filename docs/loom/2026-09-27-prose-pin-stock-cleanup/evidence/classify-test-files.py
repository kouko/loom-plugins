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

# Program-executing signals.
EXECUTE = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)"
    r"|loom_checker\.py"
    r"|pytest\.raises"
    r"|\.returncode"
    r"|check_mechanisms\.py|check_doc_citations\.py|check_contract_citations\.py"
)
# Imports production logic (not the prose_pin matcher, not other tests).
PROD_IMPORT = re.compile(
    r"^from (?:loom_checker|scripts|check_|prose_pin|second_vendor|rehearse|dispatch|claude_reviewer|coldread|repo_files|git_exec)\b"
    r"|^import (?:loom_checker|prose_pin)\b"
)
PROSE_PIN_IMPORT = re.compile(r"^from prose_pin\b|^import prose_pin\b")
# Sentence-literal assertions on prose content.
SENTENCE_ASSERT = re.compile(
    r"assert[^\n]*\b(?:in|==) .*?[\"']"
    r"|pins_exact_sentence\("
    r"|_affirms\(|affirms\(|_stated_once\(|_flat\("
    r"|flat_prose\(|rule_prose\(|split_sentences\("
)
# Structural-only signals (headings, frontmatter, keys, gate markers).
STRUCTURE = re.compile(
    r"startswith\(\"#|## |frontmatter|yaml\.safe_load|json\.loads|\.get\(\"status|\"### |gate: |#+ .*——"
)


def classify(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if ".md" not in text and ".markdown" not in text:
        return "not-prose"
    if EXECUTE.search(text):
        return "behavior"
    if PROD_IMPORT.search(text):
        return "behavior"
    if SENTENCE_ASSERT.search(text):
        # matcher self-test or gate-marker grammar: retained
        if PROSE_PIN_IMPORT.search(text) and ("synthetic" in text or "gate" in text):
            return "grammar-invariant"
        return "sentence-pin"
    if STRUCTURE.search(text):
        return "structure"
    return "other"


def main() -> int:
    roots = DEFAULT_ROOTS if "--roots" not in sys.argv else sys.argv[sys.argv.index("--roots") + 1:].split(",")
    counts: dict[str, int] = {}
    rows = []
    for root in roots:
        for p in sorted((REPO / root).glob("*.py")):
            cls = classify(p)
            counts[cls] = counts.get(cls, 0) + 1
            if cls in {"sentence-pin", "structure", "grammar-invariant"}:
                rows.append((p.relative_to(REPO).as_posix(), cls))
    print(f"{'file':65s} class")
    for f, c in rows:
        print(f"{f:65s} {c}")
    print("\ncounts:", dict(sorted(counts.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
