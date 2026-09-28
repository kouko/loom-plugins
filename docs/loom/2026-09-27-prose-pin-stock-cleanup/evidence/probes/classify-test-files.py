#!/usr/bin/env python3
"""Census classifier for the prose-pin stock cleanup (W0-01).
concern: a test file that pins prose sentences but is counted as behavior, structure or grammar-invariant, hiding a pin from the census.

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
  gate-eval  — would be sentence-pin, but its path is named by an `eval:` value
               in docs/loom/evidence/mechanisms.yaml (a gate's execution evidence;
               kept in batch 1, W3-02)

A file is a prose reader if it names a .md path. `behavior` wins ties;
`grammar-invariant` wins over `sentence-pin` only for matcher self-tests
and gate-marker grammar, which the plan lists explicitly as retained.

Usage: python3 classify-test-files.py [--roots a,b,...]  (prints a table)
       python3 classify-test-files.py --count-exec <dir> [--list]  (A5: test
       functions that run a program, directly or through a helper, under <dir>'s
       four test roots; --list prints each counted file::function)
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
    r"|assert\s*[\"'](?!#)[^\"'\n]{5,}[\"']\s*\b(?:in|==)\b"  # assert "literal" in/== ... (a "#..." heading is structure)
    r"|pins_exact_sentence\("
    r"|_affirms\(|affirms\(|_stated_once\("
    # split_sentences stays: a phrase pin read sentence by sentence is seen by
    # no alternative above. Files that use it only for a one-home scan carry
    # a MANUAL_OVERRIDES row saying so.
    r"|split_sentences\("
    # Reader calls (_flat, flat_prose, rule_prose) are not pins: a pin
    # asserts a literal, which the first alternative catches.
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


def code_only(text: str) -> str:
    """The source with its `#` comments removed, so no comment can change a class.

    Docstrings are kept: stripping them reclassifies 15 files (none into
    sentence-pin), a wider census change than this fix round covers.
    """
    import io
    import tokenize

    lines = text.splitlines(keepends=True)
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (SyntaxError, tokenize.TokenError):
        return text
    for tok in reversed([t for t in tokens if t.type == tokenize.COMMENT]):
        (row, col), (_row, end) = tok.start, tok.end
        lines[row - 1] = lines[row - 1][:col] + lines[row - 1][end:]
    return "".join(lines)


def executes(text: str) -> bool:
    """Execution signal: a program run (subprocess/checker/script) whose result is asserted."""
    has_subprocess_assert = bool(re.search(r'\.(?:stdout|stderr|returncode)|pytest\.raises', text))
    return bool(
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
    )


def load_gate_evals(repo: Path = REPO) -> set[str]:
    """Repo paths named by any `eval:` value of mechanisms.yaml (the part before `::`)."""
    import yaml

    data = yaml.safe_load((repo / "docs/loom/evidence/mechanisms.yaml").read_text(encoding="utf-8"))
    found: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "eval" and isinstance(v, str):
                    found.add(v.strip().strip("\"'").split("::")[0].strip())
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(data)
    return found


def classify(path: Path, gate_evals: set[str] = frozenset()) -> tuple[str, dict]:
    """Return (primary_class, secondary_markers)."""
    cls, secondary = _classify(path)
    if cls == "sentence-pin":
        try:
            key = path.resolve().relative_to(REPO).as_posix()
        except ValueError:
            key = path.as_posix()
        if key in gate_evals:
            return "gate-eval", secondary
    return cls, secondary


RUNNER_CALLS = {"subprocess.run", "subprocess.check_output", "subprocess.check_call",
                "subprocess.call", "subprocess.Popen", "os.system", "os.popen"}
LOADER_CALLS = {"module_from_spec", "import_module", "run_path", "run_module"}
COUNT_HELPER_MODULES = {"prose_pin", "rehearse_probes", "__init__"}  # test helpers kept in scripts/


def production_modules(base: Path) -> set[str]:
    """Module names defined under a `scripts` dir of base that is not a test or docs dir."""
    names: set[str] = set()
    for d in base.rglob("scripts"):
        if not d.is_dir() or {"tests", "docs", ".claude", ".git"} & set(d.relative_to(base).parts):
            continue
        names.update(p.stem for p in d.rglob("*.py"))
        names.update(p.name for p in d.iterdir() if p.is_dir())
        names.add("scripts")  # `from scripts.<module> import ...`
    return names - COUNT_HELPER_MODULES


def _dotted(node) -> str:
    import ast

    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_dotted(node.value)}.{node.attr}"
    return ""


def executing_test_names(src: str, prod: set[str]) -> list[str]:
    """Test functions that run a program: a subprocess/os call, a production-code call, or a
    local helper (or fixture parameter) that does either. String literals never count."""
    import ast

    tree = ast.parse(src)
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    prod_names: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom) and n.module and n.module.split(".")[0] in prod:
            prod_names.update(a.asname or a.name for a in n.names)
        elif isinstance(n, ast.Import):
            prod_names.update((a.asname or a.name).split(".")[0] for a in n.names if a.name.split(".")[0] in prod)
    loaders = set(LOADER_CALLS) | {f.name for f in funcs if any(
        isinstance(c, ast.Call) and _dotted(c.func).split(".")[-1] in LOADER_CALLS for c in ast.walk(f))}
    for n in tree.body:  # module names bound to a path-loaded module or a production attribute
        if isinstance(n, ast.Assign):
            loaded = isinstance(n.value, ast.Call) and _dotted(n.value.func).split(".")[-1] in loaders
            if loaded or _dotted(n.value).split(".")[0] in prod_names:
                prod_names.update(t.id for t in n.targets if isinstance(t, ast.Name))

    def direct(fn) -> bool:
        for c in ast.walk(fn):
            if isinstance(c, ast.Call):
                name = _dotted(c.func)
                if name in RUNNER_CALLS or name.split(".")[-1] in LOADER_CALLS:
                    return True
                if name and name.split(".")[0] in prod_names:
                    return True
        return False

    def called(fn) -> set[str]:
        out = {_dotted(c.func).split(".")[-1] for c in ast.walk(fn) if isinstance(c, ast.Call)}
        return out | {a.arg for a in fn.args.args}  # fixture parameters

    runs = {f.name for f in funcs if direct(f)}
    while True:
        more = {f.name for f in funcs if f.name not in runs and called(f) & runs}
        if not more:
            break
        runs |= more
    return [f.name for f in funcs if f.name.startswith("test") and f.name in runs]


def count_executing_tests(base: Path) -> int:
    """Count test functions that run a program (see executing_test_names), under base's four test roots."""
    prod = production_modules(base)
    total = 0
    for root in DEFAULT_ROOTS:
        for p in sorted((base / root).rglob("*.py")):
            total += len(executing_test_names(p.read_text(encoding="utf-8", errors="replace"), prod))
    return total


def _classify(path: Path) -> tuple[str, dict]:
    text = code_only(path.read_text(encoding="utf-8", errors="replace"))
    has_md = ".md" in text or ".markdown" in text

    if not has_md:
        return "not-prose", {}

    # Check for behavior FIRST (executes programs or imports production logic)
    # Behavior wins ties per the spec
    # For subprocess calls, also require assertions on subprocess results
    is_behavior_from_execution = executes(text) or PROD_IMPORT.search(text)

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


# Explicit, visible overrides applied after automatic classification (fix
# round). Each row prints `auto=<class>, override=<class>` in the table.
MANUAL_OVERRIDES = {
    "loom-code/tests/test_adversary_recipe_shape.py": (
        "structure",
        "split_sentences feeds a duplicate-sentence check across recipe files; "
        "no prose literal is asserted",
    ),
    # W4-02: the files that fell through to `other`, each read in full.
    "loom-code/tests/test_adversary_recipe_skill_gate.py": (
        "structure",
        "one-home check: asserts no rule fragment sits in both the recipe and "
        "adversary.md; never asserts a sentence is present",
    ),
    "loom-code/tests/test_adversary_recipe_spec.py": (
        "structure",
        "one-home check: asserts no rule fragment sits in both the recipe and "
        "adversary.md; never asserts a sentence is present",
    ),
    # Fix round 2: restored with its structure checks only.
    "loom-code/tests/test_agy_tool_mapping.py": (
        "structure",
        "mapping-table column scan, per-role dispatch line and link resolution, "
        "plus synthetic self-tests; no sentence asserted",
    ),
    "loom-code/tests/test_check_skill_crossrefs.py": (
        "behavior",
        "loads check-skill-crossrefs.py by path and runs find_broken_crossrefs "
        "on temp fixtures",
    ),
    # Batch 2 (W1-01): kept one-home and resolver scans, and the gate-eval
    # files pruned to structure.
    "loom-code/tests/test_build_recovery_rules.py": (
        "structure",
        "one-home scans only: the build.absence-recovery gate block restates no "
        "artifact-to-station mapping, and §1-§2 repeat none of the rule; "
        "split_sentences feeds that scan, no sentence is asserted present; RL-12 "
        "is the eval of build.absence-recovery",
    ),
    "loom-code/tests/test_closing_review_recovery_rules.py": (
        "structure",
        "one-home scan only: the review.absence-recovery gate block restates no "
        "artifact-to-station mapping; split_sentences feeds that scan, no "
        "sentence is asserted present; RL-04 is the eval of review.absence-recovery",
    ),
    "loom-code/tests/test_dispatch_profile_contract.py": (
        "structure",
        "resolver one-home scan (each invocation phrase once in the profile, "
        "never in a station), gate markers with their eval registration, and "
        "the packaged profile link resolving",
    ),
    "loom-workflow/tests/goal-create/test_skill_md.py": (
        "structure",
        "mode headings, reference paths resolving, the floor command shape, the "
        "session-activation gate blocks, template non-restatement and the "
        "offer-site count; eval of goal-create.session-activation, no sentence asserted",
    ),
    "loom-workflow/tests/scripts/test_distill_sessions_compaction.py": (
        "structure",
        "token and path needles only (top.json, merged.json, --approved, the "
        "runtime-protocol pointer resolving); no sentence asserted",
    ),
    "loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py": (
        "structure",
        "asserts no retired loom-code skill name against the skills on disk, "
        "plus scanner self-tests; no sentence asserted",
    ),
    "loom-workflow/tests/scripts/test_skill_count.py": (
        "structure",
        "skill directory set and manifest tools agree; no sentence asserted",
    ),
    "tests/test_kickoff_defaults.py": (
        "structure",
        "the lock-file hash graph and the package-tests preset command shape; "
        "no prose literal",
    ),
    "tests/test_principles_ratification.py": (
        "structure",
        "exactly one ratified-by line and no pending-ratification line; no "
        "prose literal",
    ),
}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Census classifier for the prose-pin stock cleanup.")
    parser.add_argument("--roots", default=",".join(DEFAULT_ROOTS), help="comma-separated test roots")
    parser.add_argument("--count-exec", metavar="DIR", help="count executing test functions under DIR")
    parser.add_argument("--list", action="store_true", help="with --count-exec, print each counted function")
    args = parser.parse_args()
    if args.count_exec is not None:
        base = Path(args.count_exec).resolve()
        if args.list:
            prod = production_modules(base)
            for root in DEFAULT_ROOTS:
                for p in sorted((base / root).rglob("*.py")):
                    for name in executing_test_names(p.read_text(encoding="utf-8", errors="replace"), prod):
                        print(f"{p.relative_to(base).as_posix()}::{name}")
        print(f"executing test functions under {base}: {count_executing_tests(base)}")
        return 0
    roots = [r for r in args.roots.split(",") if r]
    gate_evals = load_gate_evals()
    counts: dict[str, int] = {"sentence-pin": 0, "gate-eval": 0, "other": 0}  # A1/A4 read these even at zero
    rows = []  # (file, class, secondary_markers)
    for root in roots:
        for p in sorted((REPO / root).rglob("*.py")):
            cls, secondary = classify(p, gate_evals)
            key = p.relative_to(REPO).as_posix()
            if key in MANUAL_OVERRIDES:
                forced, reason = MANUAL_OVERRIDES[key]
                secondary = {"auto": cls, "override": forced, "reason": reason, **secondary}
                cls = forced
            counts[cls] = counts.get(cls, 0) + 1
            secondary_str = ", ".join(f"{k}={v}" for k, v in secondary.items()) if secondary else ""
            rows.append((key, cls, secondary_str))  # every file, so no bucket is hidden

    print(f"{'file':65s} {'class':20s} secondary")
    for f, c, s in rows:
        print(f"{f:65s} {c:20s} {s}")

    print("\ncounts:", dict(sorted(counts.items())))
    if counts["other"]:
        print("FAIL: files in `other` belong to no named class; add a MANUAL_OVERRIDES row")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
