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


def loop_pin_lines(text: str) -> list[int]:
    """Lines of the loop-form phrase pin: `for p in (<literals>): assert p in TEXT`.

    The loop runs over a tuple, list or set of string literals, written inline or
    bound to a module-level name, and at least one literal is a phrase of three
    or more words (a path, key or token list is not prose). Only a positive `in`
    on the loop variable counts; `not in` and `.exists()` loops do not.
    """
    import ast

    def phrases(node) -> bool:
        return isinstance(node, (ast.Tuple, ast.List, ast.Set)) and any(
            isinstance(e, ast.Constant) and isinstance(e.value, str) and len(e.value.split()) >= 3
            for e in node.elts)

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    consts = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if isinstance(t, ast.Name)}
    hits = []
    for loop in ast.walk(tree):
        if not (isinstance(loop, ast.For) and isinstance(loop.target, ast.Name)):
            continue
        it = consts.get(loop.iter.id) if isinstance(loop.iter, ast.Name) else loop.iter
        if not phrases(it):
            continue
        for node in ast.walk(loop):
            test = node.test if isinstance(node, ast.Assert) else None
            if (isinstance(test, ast.Compare) and isinstance(test.left, ast.Name)
                    and test.left.id == loop.target.id and isinstance(test.ops[0], ast.In)):
                hits.append(node.lineno)
    return hits


PRODUCTION_MD = re.compile(
    r"SKILL\.md|\b(?:agents|references|protocols|checklists|rubrics|standards|skills)\b\s*[/\"']")
READ_ATTRS = {"read_text", "read", "readlines"}
OUTPUT_ATTRS = {"stdout", "stderr", "output", "readouterr"}
PARSE_CALLS = {"json.loads", "json.load", "yaml.safe_load", "yaml.load", "tomllib.loads"}
NON_PROSE_PATH = re.compile(r"\.(?:json|ya?ml|py|toml|lock|txt|sh|html)\b|CHANGELOG|README|AGENTS\.md|CLAUDE\.md")
TMP_NAMES = {"tmp_path", "tmpdir", "tmp_path_factory", "mkdtemp", "TemporaryDirectory"}
VALIDATOR_NAME = re.compile(r"error|issue|violation|problem|finding|validate|check|lint|reason", re.I)
COMMAND_WORDS = {"git", "python", "python3", "uv", "gh", "bash", "sh", "pytest", "npm", "pnpm",
                 "pip", "claude", "codex", "make", "cd", "agy"}


def _prose_literal(s: str) -> bool:
    """A literal of 3+ words that is not a heading, table row, command or path."""
    words = [w for w in s.split() if any(ch.isalpha() for ch in w)]
    if len(words) < 3 or s.lstrip().startswith(("#", "|")):
        return False
    first = words[0].strip("`$")
    return not (first in COMMAND_WORDS or "/" in first or first.endswith((".py", ".sh")) or " --" in s)


_PROD_CACHE: dict[Path, set[str]] = {}


def _repo_production_modules() -> set[str]:
    if REPO not in _PROD_CACHE:
        _PROD_CACHE[REPO] = production_modules(REPO)
    return _PROD_CACHE[REPO]


def direct_pin_lines(text: str) -> list[int]:
    """Lines of a direct sentence pin: a prose literal asserted against text read from a markdown file.

    Heuristic, AST-based and conservative (it misses rather than guesses):
    - Only a file that names a production skill, agent or reference markdown path
      (SKILL.md, agents/, references/, protocols/, skills/ ...) is scanned.
    - Markdown text is an expression that calls `.read_text()`, `.read()`, `open()`, or a
      local helper (or a fixture parameter of that name) whose body reads a file, or a
      name assigned from such an expression (module or function scope, `for` and
      comprehension targets too). A read whose path (the receiver, or the argument of a
      reader helper, followed through the names it was assigned from) names a .json/.yaml/
      .py/.html/CHANGELOG/README/AGENTS.md/CLAUDE.md path is not skill prose.
    - Program output is never markdown text, and output wins over a read: an expression
      touching `.stdout`, `.stderr`, `.output`, `readouterr`, json/yaml parsing, a runner
      call (subprocess, os.system), `tmp_path`/`tmpdir`/a temp dir (files a program or
      fixture wrote), a call into production code (imported or path-loaded, as in the
      A5 count), a local function named like a validator (error, issue, violation,
      problem, finding, validate, check, lint, reason), a local helper (or a fixture
      parameter of that name) that does any of these, or a name assigned from any of these.
    - A prose literal (see _prose_literal: 3+ words with letters, no heading, table row,
      command or path), inline or a module-level string name, counts when asserted with
      `in`, `==`, `.startswith()` or `.endswith()` against markdown text inside an
      `assert` (also `text.count(<literal>) == N`, `>=`/`>` N with N >= 1; `<= 1` is a
      one-home check and does not count), as does a phrase-collection comprehension variable asserted `in` it or
      collected when `not in` it. Nested functions are read with their enclosing one.
    A comparison written in an `if` of a helper, a regex search, or on a helper parameter
    is not seen; such files need a reader.
    """
    import ast

    if not PRODUCTION_MD.search(text):
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    mod_strs = {t.id: n.value.value for n in tree.body if isinstance(n, ast.Assign)
                and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
                for t in n.targets if isinstance(t, ast.Name)}
    mod_colls = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
                 and isinstance(n.value, (ast.Tuple, ast.List, ast.Set))
                 for t in n.targets if isinstance(t, ast.Name)}
    src: dict[str, str] = {}  # every name's assigned source, any scope: where a read's path came from
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    src[t.id] = src.get(t.id, "") + (ast.get_source_segment(text, n.value) or "")
    funcs = {f.name: f for f in ast.walk(tree) if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
    prod = _production_names(tree, _repo_production_modules())

    def names(node) -> set[str]:
        return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}

    def calls(node) -> set[str]:
        return {_dotted(c.func) for c in ast.walk(node) if isinstance(c, ast.Call)}

    def receiver_is_prose(call) -> bool:
        seg = ast.get_source_segment(text, call.func.value) if isinstance(call.func, ast.Attribute) else (
            ast.get_source_segment(text, call.args[0]) if call.args else "")
        seg = seg or ""
        return not NON_PROSE_PATH.search("".join(src.get(i, "") for i in re.findall(r"\w+", seg)) + seg)

    def raw_read(node) -> bool:
        return any(isinstance(c, ast.Call) and (
            (isinstance(c.func, ast.Attribute) and c.func.attr in READ_ATTRS)
            or _dotted(c.func) == "open") and receiver_is_prose(c) for c in ast.walk(node))

    def raw_output(node) -> bool:
        called = calls(node)
        return any(isinstance(c, ast.Attribute) and c.attr in OUTPUT_ATTRS for c in ast.walk(node)) or bool(
            called & (RUNNER_CALLS | PARSE_CALLS)) or bool(
            names(node) & TMP_NAMES or {c.split(".")[-1] for c in called} & TMP_NAMES) or any(
            c.split(".")[0] in prod or (c in funcs and VALIDATOR_NAME.search(c)) for c in called)

    runners = {n for n, f in funcs.items() if raw_output(f)}
    readers = {n for n, f in funcs.items() if raw_read(f) and n not in runners}
    while True:
        more_r = {n for n, f in funcs.items() if n not in runners
                  and {c.split(".")[-1] for c in calls(f)} & runners}
        more_m = {n for n, f in funcs.items() if n not in readers | runners | more_r
                  and {c.split(".")[-1] for c in calls(f)} & readers}
        if not (more_r or more_m):
            break
        runners |= more_r
        readers |= more_m

    def is_output(node, out) -> bool:
        called = {c.split(".")[-1] for c in calls(node)}
        return raw_output(node) or bool(called & runners) or bool(names(node) & out)

    def is_md(node, md, out) -> bool:
        if is_output(node, out):
            return False
        read_helper = any(isinstance(c, ast.Call) and _dotted(c.func).split(".")[-1] in readers and not any(
            NON_PROSE_PATH.search(src.get(i, "") + i) for a in c.args for i in names(a)) for c in ast.walk(node))
        return raw_read(node) or read_helper or bool(names(node) & md)

    def bindings(scope):
        for n in ast.walk(scope):
            if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and n.value is not None:
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                yield [t for tg in targets for t in ast.walk(tg) if isinstance(t, ast.Name)], n.value
            elif isinstance(n, (ast.For, ast.comprehension)):
                yield [t for t in ast.walk(n.target) if isinstance(t, ast.Name)], n.iter
            elif isinstance(n, ast.withitem) and n.optional_vars is not None:
                yield [t for t in ast.walk(n.optional_vars) if isinstance(t, ast.Name)], n.context_expr

    def taint(scope, md, out):
        md, out = set(md), set(out)
        while True:
            size = len(md) + len(out)
            for targets, value in bindings(scope):
                ids = {t.id for t in targets}
                if is_output(value, out):
                    out |= ids
                elif is_md(value, md, out):
                    md |= ids - out
            if len(md) + len(out) == size:
                return md, out

    def literal(node) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name):
            return mod_strs.get(node.id)
        return None

    def phrase_coll(node) -> bool:
        node = mod_colls.get(node.id) if isinstance(node, ast.Name) else node
        return isinstance(node, (ast.Tuple, ast.List, ast.Set)) and any(
            _prose_literal(literal(e) or "") for e in node.elts)

    mod_md, mod_out = taint(ast.Module(body=[n for n in tree.body if not isinstance(
        n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))], type_ignores=[]), set(), set())
    hits: set[int] = set()
    nested = {id(g) for f in funcs.values() for g in ast.walk(f) if g is not f and g in funcs.values()}
    for f in (f for f in funcs.values() if id(f) not in nested):  # a nested helper is read with its parent
        params = {a.arg for a in f.args.args}  # a local fixture of that name decides the parameter
        md, out = taint(f, mod_md | (params & readers), mod_out | (params & runners))
        phrase_vars = {g.target.id for n in ast.walk(f) if isinstance(n, (ast.ListComp, ast.SetComp, ast.GeneratorExp))
                       for g in n.generators if isinstance(g.target, ast.Name) and phrase_coll(g.iter)}
        for node in ast.walk(f):
            if isinstance(node, ast.Assert):
                for c in ast.walk(node.test):
                    if isinstance(c, ast.Compare) and len(c.ops) == 1:
                        left, right = c.left, c.comparators[0]
                        pinned = _prose_literal(literal(left) or "") or (
                            isinstance(left, ast.Name) and left.id in phrase_vars)
                        if isinstance(c.ops[0], ast.In) and pinned and is_md(right, md, out):
                            hits.add(c.lineno)
                        elif isinstance(c.ops[0], ast.Eq) and any(
                                _prose_literal(literal(a) or "") and is_md(b, md, out)
                                for a, b in ((left, right), (right, left))):
                            hits.add(c.lineno)
                        elif isinstance(c.ops[0], (ast.Eq, ast.GtE, ast.Gt)) and isinstance(left, ast.Call) \
                                and isinstance(left.func, ast.Attribute) and left.func.attr == "count" \
                                and left.args and _prose_literal(literal(left.args[0]) or "") \
                                and isinstance(right, ast.Constant) and isinstance(right.value, int) \
                                and right.value >= 1 and is_md(left.func.value, md, out):
                            hits.add(c.lineno)  # `text.count(<sentence>) == 1`: present, not "at most once"
                    elif isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) \
                            and c.func.attr in ("startswith", "endswith") and c.args:
                        arg = c.args[0]
                        lits = [literal(e) for e in arg.elts] if isinstance(arg, ast.Tuple) else [literal(arg)]
                        if any(_prose_literal(s or "") for s in lits) and is_md(c.func.value, md, out):
                            hits.add(c.lineno)
            elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
                for g in node.generators:
                    if not (isinstance(g.target, ast.Name) and phrase_coll(g.iter)):
                        continue
                    for cond in g.ifs:
                        for c in ast.walk(cond):
                            if isinstance(c, ast.Compare) and isinstance(c.left, ast.Name) \
                                    and c.left.id == g.target.id and isinstance(c.ops[0], ast.NotIn) \
                                    and is_md(c.comparators[0], md, out):
                                hits.add(c.lineno)
    return sorted(hits)


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


def _production_names(tree, prod: set[str]) -> set[str]:
    """Names bound to production code: imported from a production module, or a module-level
    name bound to a path-loaded module or a production attribute."""
    import ast

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
    return prod_names


def executing_test_names(src: str, prod: set[str]) -> list[str]:
    """Test functions that run a program: a subprocess/os call, a production-code call, or a
    local helper (or fixture parameter) that does either. String literals never count."""
    import ast

    tree = ast.parse(src)
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    prod_names = _production_names(tree, prod)

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
    direct_pin = bool(direct_pin_lines(text))  # a sentence asserted against markdown text, no helper needed
    # the loop form of a phrase pin or a direct pin, neither of which the regex can see
    phrase_pin = bool(loop_pin_lines(text)) or direct_pin
    if is_behavior:
        secondary = {}
        # Check for sentence pins (secondary marker for behavior files that also pin prose)
        secondary["has_pins"] = "yes" if (SENTENCE_ASSERT.search(text) and PROSE_PIN_IMPORT.search(text)) or phrase_pin else "no"
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
    has_sentence_assert = SENTENCE_ASSERT.search(text) or phrase_pin

    is_sentence_pin_candidate = (has_sentence_assert and (
        has_prose_pin_import or has_prose_helpers or has_prose_normalization)) or direct_pin

    # Check for grammar-invariant (when not also sentence-pin, or when sentence-pin doesn't win)
    if is_grammar_invariant_candidate:
        secondary = {}
        secondary["has_pins"] = "yes" if has_sentence_assert else "no"
        if has_sentence_assert:
            secondary["note"] = "mixed-grammar-and-pin"
        return "grammar-invariant", secondary

    # Check for sentence-pin (has sentence assertions about prose, no behavior)
    if is_sentence_pin_candidate:
        secondary = {}
        secondary["has_pins"] = "yes"
        return "sentence-pin", secondary

    # Check for structure
    if STRUCTURE.search(text):
        return "structure", ({"has_pins": "yes"} if phrase_pin else {})

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
        "artifact-to-station mapping, and §1-§2 repeat none of the rule; the "
        "block cites the three manifest keys (path pointers); split_sentences "
        "feeds the scan, no sentence is asserted present; RL-12 is the eval of "
        "build.absence-recovery",
    ),
    "loom-code/tests/test_closing_review_recovery_rules.py": (
        "structure",
        "one-home scan only: the review.absence-recovery gate block restates no "
        "artifact-to-station mapping; split_sentences feeds that scan, no "
        "sentence is asserted present; RL-04 is the eval of review.absence-recovery",
    ),
    "loom-code/tests/test_dispatch_profile_contract.py": (
        "structure",
        "resolver one-home scan (no invocation phrase restated in a station; "
        "the presence-in-profile half was removed in closing review round 1), "
        "gate markers with their eval registration, and the packaged profile "
        "link resolving",
    ),
    "loom-workflow/tests/goal-create/test_skill_md.py": (
        "structure",
        "mode headings, reference paths resolving, the floor command shape, the "
        "session-activation gate blocks, template non-restatement and the "
        "offer-site count (its number recomputed from the sites scanned in the "
        "repo); eval of goal-create.session-activation, no sentence asserted",
    ),
    # Batch 2 residual fix: the pruned batch-2 files, each read in full after
    # their last sentence pins were removed.
    "loom-code/tests/test_acceptance_test_report_shape.py": (
        "structure",
        "template table columns, rows and markers, the evidence block heading, "
        "the template path pointer in the tester contract, a full-suite "
        "absence scan fed by split_sentences, no gate marker, and the evidence "
        "path pointer outside every gate block; the two station phrases it "
        "once looped over were pruned in the batch-2 loop-form fix, so no "
        "sentence is asserted present",
    ),
    "loom-code/tests/test_adversary_protocol.py": (
        "behavior",
        "imports MAX_PROBE_PROGRAMS from loom_checker for the case-count scan; "
        "the rest is a one-home absence scan and YAML keys of the return "
        "block; no sentence asserted present",
    ),
    "loom-code/tests/test_adversary_routing.py": (
        "behavior",
        "runs the adversary tests in repo copies after real add, remove and "
        "reword edits; literals are a recipe's link back to the protocol, "
        "exception messages and pytest stdout; split_sentences only picks a "
        "sentence to reword; no sentence asserted present",
    ),
    "loom-code/tests/test_lenses_deletion_first.py": (
        "structure",
        "reviewer.md lens table rows end with the deletion-first dimension "
        "token; no sentence asserted",
    ),
    "loom-code/tests/test_plan_simplicity_text.py": (
        "structure",
        "absence checks, the write-plan step's path pointer to "
        "plan-simplicity.md, and a scan that every user sentence of the step is "
        "negated (split_sentences); no sentence asserted present",
    ),
    "loom-code/tests/test_review_convergence_contract.py": (
        "structure",
        "gate-marker presence, heading-anchored sections, and absence or "
        "negation scans fed by split_sentences; no sentence asserted present",
    ),
    "loom-code/tests/test_reviewer_mechanical_evidence.py": (
        "structure",
        "the lenses path pointer count in reviewer.md and absence or negation "
        "scans; no sentence asserted present",
    ),
    "loom-code/tests/test_ship_station_text.py": (
        "behavior",
        "recomputes the refusal premise from publish.py source; the rest is "
        "headings, absences and gate-region placement; no sentence asserted present",
    ),
    "loom-code/tests/test_simplified_station_text.py": (
        "behavior",
        "imports the checker's STEP_PLAIN_NAMES; the rest is absence and "
        "negation scans (split_sentences), summary-table rows and a manifest "
        "YAML value; no sentence asserted present",
    ),
    "loom-code/tests/test_sync_before_review_text.py": (
        "behavior",
        "runs sync-trunk on real repositories and asserts its stdout and the "
        "digest; the prose half is absences under the §2 heading and a count "
        "of sync-trunk; no sentence asserted present",
    ),
    "loom-code/tests/test_test_budget_text.py": (
        "structure",
        "no line-number threshold in implementer.md and a gate-marker count; "
        "no sentence asserted",
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
    # Batch 2 loop-form fix: files whose only loop-form hit is not prose. The
    # reason names that hit; other asserts in the file are not re-judged here.
    "loom-code/tests/test_adversary_layout.py": (
        "behavior",
        "loop-form hit is SHARED_HEADINGS asserted in the protocol's parsed "
        "heading list: section headings, not prose",
    ),
    "loom-code/tests/test_loom_publish.py": (
        "behavior",
        "loop-form hit is CONTEXT_HEADINGS asserted in the reason the checker's "
        "validate_contextual_pr_body returns: headings in program output",
    ),
    "loom-workflow/tests/decision-map/test_skill_doc.py": (
        "behavior",
        "loop-form hit is DOCUMENTED_COMMANDS: command shapes, which the same "
        "test also runs (start_delivery.py excepted; test_start_delivery.py owns "
        "it). The direct sentence asserts batch 2 left were pruned in batch 3 "
        "(W1-01, W1-07); the rest is operation headings, fixed terms, re-entry "
        "and phase code tokens recomputed from the scripts, the ticket template "
        "grammar, schema_version, manifest fields, and the Codex manifest "
        "defaultPrompt sentence, kept as an interface string, not skill prose",
    ),
    "loom-workflow/tests/scripts/test_loom_visualization_compaction.py": (
        "structure",
        "loop-form hit is a list of `## ` headings in SKILL.md",
    ),
    "tests/test_agy_install_docs.py": (
        "structure",
        "loop-form hit is agy and git command shapes in the Antigravity CLI section",
    ),
    "loom-design/tests/interface/test_design_system_skill.py": (
        "structure",
        "loop-form hit is the eight canonical DESIGN.md section names in the schema",
    ),
    "loom-design/tests/architecture-design/test_architecture_skill.py": (
        "structure",
        "loop-form hit is the four bold field labels of the schema's Guard "
        "failure message section (rule id, offending path, conform, change the "
        "rule and its guard): schema field labels. The rest is path pointers, "
        "the ratified-by line and commit subject shape, the re-design and "
        "re-ratify tokens, the two-word terms never required and never blocks, "
        "the SKILL.md mention of the Guard failure message section name, and a "
        "heading-bounded Step 5 scan; the direct sentence "
        "asserts (single answer, re-design procedure) were pruned in closing "
        "review round 1",
    ),
    # Batch 3 (W2-01): files whose remaining direct-pin hit is not prose.
    "loom-code/tests/test_architecture_doc_consumers.py": (
        "structure",
        "direct-pin hits are the `ratified-by: <name> <date>` line grammar in "
        "write-plan Step 5 and the lenses code table; the rest is the Risk "
        "line and rule id terms, lens-table row regexes, a heading-bounded "
        "N/A bullet check and the reviewer code row; the sentence asserts "
        "were pruned in batch 3 (W1-01)",
    ),
    "loom-workflow/tests/decision-map/test_decision_map_intent_binding.py": (
        "behavior",
        "direct-pin hit is the Map line format `- delivery-intent: DA-<n> | "
        "docs/loom/intent/<change-id>.md` in map-format.md: line grammar, not "
        "prose; the rest is path and front-matter tokens, status tokens, "
        "absences, and the citation checker's scope loaded by path",
    ),
    "loom-workflow/tests/loom-visualization/test_templates.py": (
        "behavior",
        "direct-pin hit is the client-matrix table column header 'Form in a "
        "chat reply'. The three pinned_sentence_ok polarity checks "
        "(MERMAID_PIN, TABLE_ASCII_PIN, CHAT_PROCEEDS_PIN) are kept on purpose "
        "(agent-decided): they read only sentences inside the "
        "mermaid-only-when-confirmed and obsidian-boundary `<!-- gate: -->` "
        "blocks, whose mechanisms.yaml evals (L357, L354) sit in this file, "
        "and each fails a negated sentence, so they check the rule's "
        "polarity, not only its wording",
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
