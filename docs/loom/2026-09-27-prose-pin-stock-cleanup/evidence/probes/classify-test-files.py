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

REPO = Path(__file__).resolve().parents[5]
DEFAULT_ROOTS = ["loom-code/tests", "loom-workflow/tests", "tests", "loom-design/tests"]

# Program-executing signals (in test functions, not just module-level setup).
# Matches subprocess.run/check_output/Popen/call WHEN combined with a program name
# (pytest, python3, loom_checker.py, check_*.py, git) OR when .returncode is asserted.
# This catches behavior tests while potentially including module-level setup calls.
EXECUTE = re.compile(
    r"(subprocess\.(?:run|check_output|Popen|call).*["
    r"py]|pytest\.raises"
    r"|\.returncode"
    r"|check_mechanisms\.py|check_doc_citations\.py|check_contract_citations\.py"
    r"|loom_checker\.py|loom_check)"
)
# Simpler approach: just look for subprocess.run AND git/pytest/python3
# Matches: subprocess.run(["git", ...]), subprocess.run("git ...", ...), etc.
# But exclude git rev-parse --show-toplevel and --absolute-git-dir (repo root lookup, not behavior)
# Uses DOTALL flag to match across newlines
# We use multiple specific patterns to avoid matching commands far from the subprocess call
SUBPROCESS_GIT_LIST = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)\s*\(\s*\[[^]]*?\"git\"(?!.*?(?:rev-parse.*?--show-toplevel|rev-parse.*?--absolute-git-dir))[^]]*?\]",
    re.DOTALL
)
SUBPROCESS_GIT_STR = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)\s*\(\s*\"git\s(?!.*?(?:rev-parse.*?--show-toplevel|rev-parse.*?--absolute-git-dir))[^\"]*\"",
    re.DOTALL
)
SUBPROCESS_PYTEST = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)\s*\(\s*(\[.*?\"pytest\"|\"pytest\s)",
    re.DOTALL
)
SUBPROCESS_PYTHON = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)\s*\(\s*(\[.*?\"python3\"|\"python3\s)",
    re.DOTALL
)
SUBPROCESS_LOOM = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)\s*\([^)]*?loom_checker\.py",
    re.DOTALL
)
SUBPROCESS_CHECK = re.compile(
    r"subprocess\.(?:run|check_output|Popen|call)\s*\([^)]*?check_.*?\.py",
    re.DOTALL
)
# Imports production logic (not the prose_pin matcher, not other tests).
PROD_IMPORT = re.compile(
    r"from (?:loom_checker|scripts|check_|second_vendor|rehearse|dispatch|claude_reviewer|coldread|repo_files|git_exec)\b"
    r"|import (?:loom_checker)\b"
)
PROSE_PIN_IMPORT = re.compile(r"from prose_pin\b|import prose_pin\b")
# Sentence-literal assertions on prose content.
# Matches both: assert ... in/== "literal" and assert "literal" in/== ...
SENTENCE_ASSERT = re.compile(
    r"assert[^\n]*\b(?:in|==)\s*[\"']"  # assert ... in/== "literal"
    r"|assert\s*[\"'][^\"'\n]{5,}[\"']\s*\b(?:in|==)\b"  # assert "literal" in/== ...
    r"|pins_exact_sentence\("
    r"|_affirms\(|affirms\(|_stated_once\(|_flat\("
    r"|flat_prose\(|rule_prose\(|split_sentences\("
)
# Structural-only signals (headings, frontmatter, keys, gate markers).
STRUCTURE = re.compile(
    r"startswith\(\"#|## |frontmatter|yaml\.safe_load|json\.loads|\.get\(\"status|\"### |gate: |#+ .*——"
)
# Grammar-invariant signals: pins matcher rules or gate-marker grammar.
# Does NOT fire on adversary.md/engineering-baseline.md references alone —
# those are contract/reference filenames many behavior files mention.
# Fires only on signals that the file is pinning MATCHER RULES or
# GATE-MARKER GRAMMAR specifically, or is a MATCHER SELF-TEST.
# Self-test signals: NEGATION_RE (shared matcher), self-test/synthetic keywords,
# testing of prose_pin internal matchers (_has_negation, etc.)
GRAMMAR_INVARIANT_CONTENT = re.compile(
    r"prose_pin.*matcher.*rule|matcher.*rule.*prose_pin|"
    r"gate.*marker|<!--\s*gate:|version.*format|"
    r"NEGATION_RE|_SELFTEST_KW_RE|_has_negation|prose_pin.*self[- ]?test|self[- ]?test.*prose_pin"
)


def classify(path: Path) -> tuple[str, dict]:
    """Return (primary_class, secondary_markers)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    has_md = ".md" in text or ".markdown" in text

    if not has_md:
        return "not-prose", {}

    # Check for behavior FIRST (executes programs or imports production logic)
    # Behavior wins ties per the spec
    # For subprocess calls, also require assertions on subprocess results
    has_subprocess_assert = bool(re.search(r'\.(?:stdout|stderr|returncode)|pytest\.raises', text))
    is_behavior_from_execution = (
        EXECUTE.search(text)
        or (
            (
                SUBPROCESS_GIT_LIST.search(text)
                or SUBPROCESS_GIT_STR.search(text)
                or SUBPROCESS_PYTEST.search(text)
                or SUBPROCESS_PYTHON.search(text)
                or SUBPROCESS_LOOM.search(text)
                or SUBPROCESS_CHECK.search(text)
            )
            and has_subprocess_assert
        )
        or PROD_IMPORT.search(text)
    )

    # Additional behavior check: imports of production modules located in a scripts directory
    is_behavior_from_script_import = False
    if not is_behavior_from_execution:  # only check if we haven't already found behavior
        # Look for import statements that import a top-level module
        # Allows trailing comments
        import_pattern = re.compile(r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:#.*)?$|^\s*from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import', re.MULTILINE)
        # Known test helper modules in scripts/ that should NOT trigger behavior classification
        TEST_HELPER_MODULES = {"prose_pin", "rehearse_probes"}
        for match in import_pattern.finditer(text):
            mod = match.group(1) or match.group(2)
            if mod and mod not in TEST_HELPER_MODULES:
                # Skip if mod is a known stdlib or common test dependency to avoid false positives
                # We'll skip if we can't find the module in a scripts directory (not under tests)
                found = False
                for scripts_dir in REPO.rglob('scripts'):
                    if 'tests' in scripts_dir.parts:
                        continue
                    mod_file = scripts_dir / (mod + '.py')
                    if mod_file.is_file():
                        found = True
                        break
                if found:
                    is_behavior_from_script_import = True
                    break

    is_behavior = is_behavior_from_execution or is_behavior_from_script_import
    if is_behavior:
        secondary = {}
        # Check for sentence pins (secondary marker for behavior files that also pin prose)
        secondary["has_pins"] = "yes" if (SENTENCE_ASSERT.search(text) and PROSE_PIN_IMPORT.search(text)) else "no"
        # Check if it also has grammar-invariant content (additional marker)
        if GRAMMAR_INVARIANT_CONTENT.search(text):
            secondary["marker"] = "grammar-invariant-content"
        return "behavior", secondary

    # Check for grammar-invariant candidate (imports prose_pin AND has grammar-invariant content)
    is_grammar_invariant_candidate = PROSE_PIN_IMPORT.search(text) and GRAMMAR_INVARIANT_CONTENT.search(text)
    # Check for sentence-pin candidate (has sentence assertions about prose)
    # Requires prose_pin import OR prose_pin helper function calls (flat_prose, split_sentences, etc.)
    # OR prose normalization helpers (_normalize, _flat) used for sentence pinning compaction tests
    has_prose_pin_import = PROSE_PIN_IMPORT.search(text)
    has_prose_helpers = bool(re.search(r'flat_prose\(|rule_prose\(|split_sentences\(|_flat\(', text))
    has_prose_normalization = bool(re.search(r'_normalize|_flat\s*=', text))
    has_sentence_assert = SENTENCE_ASSERT.search(text)

    is_sentence_pin_candidate = has_sentence_assert and (has_prose_pin_import or has_prose_helpers or has_prose_normalization)

    # Check for grammar-invariant (when not also sentence-pin, or when sentence-pin doesn't win)
    if is_grammar_invariant_candidate:
        secondary = {}
        secondary["has_pins"] = "yes" if SENTENCE_ASSERT.search(text) else "no"
        if SENTENCE_ASSERT.search(text):
            secondary["note"] = "mixed-grammar-and-pin"
        return "grammar-invariant", secondary

    # Check for sentence-pin (has sentence assertions about prose, no behavior)
    if is_sentence_pin_candidate:
        secondary = {}
        secondary["has_pins"] = "yes"
        return "sentence-pin", secondary

    # Check for structure
    if STRUCTURE.search(text):
        return "structure", {}

    return "other", {}


def main() -> int:
    roots = DEFAULT_ROOTS if "--roots" not in sys.argv else sys.argv[sys.argv.index("--roots") + 1:].split(",")
    counts: dict[str, int] = {}
    rows = []  # (file, class, secondary_markers)
    for root in roots:
        for p in sorted((REPO / root).rglob("*.py")):
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
