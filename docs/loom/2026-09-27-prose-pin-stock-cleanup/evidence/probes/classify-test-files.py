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
       python3 classify-test-files.py --candidates  (batch 4: every literal asserted against
       skill/agent/reference markdown, classed prose or structural by literal_class, whose
       docstring holds the structural rules; batch-3 kept items print as kept-batch3)
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


PLACEHOLDER = re.compile(r"<[A-Za-z][\w -]*>|\{[\w-]*\}")
KEY_LINE = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*|\")?[a-z][\w.-]*(?:\*\*|\")?:(?:\s|$)")
COMMIT_SUBJECT = re.compile(r"^[a-z]+\([\w-]+\): ")
FILE_EXT = re.compile(r"\w\.[A-Za-z][A-Za-z0-9]{0,4}\b")
MERMAID_KEYWORDS = {"flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram", "stateDiagram-v2",
                    "erDiagram", "journey", "gantt", "pie", "quadrantChart", "requirementDiagram", "gitGraph",
                    "mindmap", "timeline", "sankey-beta", "xychart-beta", "block-beta", "packet-beta", "kanban",
                    "architecture-beta"}
MERMAID_DIRECTIONS = {"LR", "RL", "TD", "TB", "BT"}
CODE_MARK = re.compile(r"_|\(\)|\[\]|`|\w\.\w|=|\$|\\|^-|-$|[A-Za-z]\d|\w:\w")
REGEX_NORM = ((re.compile(r"\(\?[aimsxu]+\)|\\b|\\A|\\Z|(?<!\\)[\^$]"), ""),
              (re.compile(r"\\s[+*?]?"), " "), (re.compile(r"\\([.|()\[\]?*+-])"), r"\1"),
              (re.compile(r"\(\?:"), "("))


def _top_alternatives(pattern: str) -> list[str]:
    """A regex split on its top-level unescaped `|` (alternatives inside groups stay whole)."""
    alts, depth, cur, i = [], 0, "", 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == "\\":
            cur += pattern[i:i + 2]
            i += 2
            continue
        depth += (ch in "([") - (ch in ")]")
        if ch == "|" and depth == 0:
            alts.append(cur)
            cur = ""
        else:
            cur += ch
        i += 1
    return alts + [cur]


def literal_class(s: str, regex: bool = False) -> tuple[str, str] | None:
    """Class a literal asserted against prose: (`prose`|`structural`, reason), or None.

    None when the literal has no word with a letter (not a candidate). A regex pattern with
    top-level alternatives is prose when any alternative is prose, else the first alternative's
    class. Each pattern is first normalized: flags, anchors and `\\b` removed, `\\s`/`\\s+` read as a space, escaped
    punctuation unescaped. Then, first rule that matches wins:
      structural — markdown heading: starts with `#`
      structural — gate or HTML marker: contains `<!--` or `-->`
      structural — table row or cell: starts or ends with `|`, or contains ` | `
      structural — line grammar placeholder: contains `<word>` or `{word}`
      structural — field key or label: a lowercase `key:` opening the literal (optionally a
                   list item or bold), a single word ending in `:`, or a whole `**bold**` label
      structural — command: first word is a command (git, python3, uv, claude ...) or ` --flag`
      structural — commit subject grammar: opens with `type(scope): `
      3+ words   — path if the first word has `/` or ends in .py/.sh; otherwise prose
      1-2 words  — path: contains `/` or a file extension (`x.md`, or `.md` alone)
                 — repo name: a word is a hyphenated skill, plugin or script name found on
                   disk (loom-code, write-spec, sync-trunk ...)
                 — Mermaid diagram keyword: first word opens a Mermaid block (flowchart, erDiagram,
                   stateDiagram-v2 ...), any other word a direction token (LR, TD ...)
                 — generator name: a single word that is `<name>` of a gen_<name> script on disk
                 — code identifier: contains `_`, `()`, `[]`, a backtick, `a.b` (also dotted
                   rule and gate ids), `=`, `$`, a backslash (regex grammar), `a:b` (a skill id), a leading or
                   trailing `-` (a name fragment), or a letter followed by a digit (sha1, v3)
                 — ALL_CAPS token, rule id or verdict: no lowercase letter (PASS, RL-12, REQ-3)
                 — capitalized label: its first word starts with an uppercase letter (heading text, a
                   table-header cell, a bold field label or a name)
                 — otherwise prose (a 1-2 word phrase or single term)
    """
    t = s
    if regex:
        alts = _top_alternatives(s)
        if len(alts) > 1:
            got = [(a, g) for a, g in ((a, literal_class(a, regex=True)) for a in alts) if g]
            prose = [a for a, g in got if g[0] == "prose"]
            if prose:
                return "prose", f"regex alternative {prose[0]!r} is prose"
            return got[0][1] if got else None
        for pat, rep in REGEX_NORM:
            t = pat.sub(rep, t)
    t = t.strip()
    words = [w for w in t.split() if any(ch.isalpha() for ch in w)]
    if not words:
        return None
    if t.startswith("#"):
        return "structural", "markdown heading"
    if "<!--" in t or "-->" in t:
        return "structural", "gate or HTML marker"
    if t.startswith("|") or t.endswith("|") or " | " in t:
        return "structural", "table row or cell"
    if PLACEHOLDER.search(t):
        return "structural", "line grammar placeholder"
    if KEY_LINE.match(t) or (len(t.split()) == 1 and t.endswith(":")) or re.fullmatch(r"\*\*[^*]+\*\*:?", t):
        return "structural", "field key or label"
    first = words[0].strip("`$")
    if first in COMMAND_WORDS or " --" in f" {t}":
        return "structural", "command"
    if COMMIT_SUBJECT.match(t):
        return "structural", "commit subject grammar"
    if len(words) >= 3:
        if "/" in first or first.endswith((".py", ".sh")):
            return "structural", "path"
        return "prose", "phrase of 3+ words"
    if "/" in t or FILE_EXT.search(t) or re.fullmatch(r"\.\w{1,5}", t):
        return "structural", "path"
    if any(w.strip("`'\".,:;()") in _repo_names() for w in words):
        return "structural", "names a skill, plugin or script (a hyphenated repo name)"
    if words[0] in MERMAID_KEYWORDS and set(words[1:]) <= MERMAID_DIRECTIONS:
        return "structural", "Mermaid diagram keyword"
    if len(words) == 1 and words[0] in _generator_names():
        return "structural", "generator name (a gen_<name> script on disk)"
    if CODE_MARK.search(t):
        return "structural", "code identifier"
    if not any(ch.islower() for ch in t):
        return "structural", "ALL_CAPS token, rule id or verdict"
    if words[0][0].isupper():
        return "structural", "capitalized label (heading text, table-header cell, bold label or name)"
    return "prose", "1-2 word phrase or term"


_PROD_CACHE: dict[Path, set[str]] = {}
_NAMES_CACHE: dict[Path, set[str]] = {}


def _repo_names() -> set[str]:
    """Hyphenated skill, plugin and script names on disk (`loom-code`, `write-spec`, `sync-trunk`)."""
    if REPO not in _NAMES_CACHE:
        found = {d.name for d in REPO.glob("*/skills/*") if d.is_dir()}
        found |= {d.name for d in REPO.iterdir() if d.is_dir()}
        found |= {q.stem for q in REPO.glob("*/skills/*/scripts/*")} | {q.stem for q in REPO.glob("*/scripts/*")}
        _NAMES_CACHE[REPO] = {n for n in found if "-" in n}
    return _NAMES_CACHE[REPO]


def _generator_names() -> set[str]:
    """Generator names from `gen_<name>` scripts on disk (`seq` from gen_seq.py)."""
    return {q.stem[4:] for q in REPO.glob("*/skills/*/scripts/gen_*.py")}


def _repo_production_modules() -> set[str]:
    if REPO not in _PROD_CACHE:
        _PROD_CACHE[REPO] = production_modules(REPO)
    return _PROD_CACHE[REPO]


def direct_pin_lines(text: str) -> list[int]:
    """Lines of a direct prose pin: the lines of every `prose`-class pin_candidates row."""
    return sorted({c["line"] for c in pin_candidates(text) if c["cls"] == "prose"})


def pin_candidates(text: str) -> list[dict]:
    """Every literal asserted against text read from a markdown file, classed by literal_class.

    Each row: line, func (the top-level function read), literal, form, cls, reason.

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
      A json/yaml parse taints only its parsed value: a helper is output when it returns a
      parsed value, and when it returns a tuple only the parsed positions are output, so a
      markdown body returned beside parsed frontmatter stays markdown text.
    - One exception to output-wins: a plain read of a path naming a skill, agent or reference
      file (SKILL.md, agents/, references/ ...) is markdown text even under a temp dir, since an
      installed copy of a plugin's own skill file is still its prose.
    - A literal (any length with a letter; an inline string, a module-level string name, or an
      f-string's constant parts) is a candidate when it is asserted with `in`, `==`,
      `.startswith()` or `.endswith()` against markdown text inside an `assert` (also
      `text.count(<literal>) == N`, `>=`/`>` N with N >= 1; `<= 1` is a one-home check and
      does not count), as is each literal of a collection (module-level or local tuple, list
      or set) whose comprehension variable is asserted `in` it or collected when `not in` it.
    - Batch 4 forms: a literal required by an `if` (`if "x" not in text`, or `in` under an
      odd number of `not`; an `if` whose body is only `continue`/`pass` is a filter and does
      not count) or returned (`return "x" in text`); a `.index()`/`.rindex()` lookup of a
      literal on markdown text (it raises when the literal is gone); and a `re.search`/
      `match`/`fullmatch`/`findall`/`finditer` (or the same method on a name bound to
      `re.compile(<literal>)`) whose pattern is a literal and whose subject is markdown text,
      unless directly negated (`not re.search(...)`, an absence); in an `if` test it counts
      only under an odd number of `not` (and not as a continue/pass filter), and in a
      comprehension condition it is a filter and does not count.
    - A local helper, validator-named or not, whose parameter receives markdown text at any
      call site in the file (to a fixed point) reads that parameter as markdown text, so a
      literal it requires of its input is a candidate on the helper's own line.
      Nested functions are read with their enclosing one.
    - Needles routed through containers (W1-07): in every form above, a needle may be a name
      that a `for` or comprehension target binds (tuple targets too) over a collection, a dict
      (its keys), `.items()`/`.values()`/`.keys()`, or another such bound name, or a
      `pytest.mark.parametrize` parameter; each string it can hold is a candidate, classed on
      its own. `.lower()`-style calls on the needle are looked through. A positive `in` whose
      statement stores or passes its value (`facts = {"k": any("x" in b for b in blocks)}`)
      counts too, unless negated or in a comprehension filter; a filter of a `next(...)`
      first-match lookup still counts, since a miss yields the default.
    - A literal (or a collection, spread with `*`) passed to a local helper that requires it
      of markdown text is a candidate on the call line, for calls that pass markdown text in.
    - literal_class then classes each candidate prose or structural; only prose ones count as
      pins (direct_pin_lines), the census `--candidates` mode lists both.
    Not seen: a needle passed through two helper levels, a subscript (`phrases[0]`), a
    non-literal regex, and asserts on names the file-wide judgment calls output. A stored
    `in` later asserted absent is counted anyway (a false candidate, judged by hand).
    Known limits: a local helper named like a validator word (`_checklist()` matches
    'check') is taken as output; and a variable name is judged file-wide, so one name
    holding README.md in one test and SKILL.md in another counts as non-prose everywhere.
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
                 and isinstance(n.value, (ast.Tuple, ast.List, ast.Set, ast.Dict))
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

    def raw_output(node, parse: bool = True) -> bool:
        called = calls(node)
        return any(isinstance(c, ast.Attribute) and c.attr in OUTPUT_ATTRS for c in ast.walk(node)) or bool(
            called & (RUNNER_CALLS | (PARSE_CALLS if parse else set()))) or bool(
            names(node) & TMP_NAMES or {c.split(".")[-1] for c in called} & TMP_NAMES) or any(
            c.split(".")[0] in prod or (c in funcs and VALIDATOR_NAME.search(c)) for c in called)

    # A helper that parses (json/yaml) is output only in what it returns from the parse:
    # a whole parsed return makes it a runner; in a returned tuple only the parsed
    # positions are output (tuple_out), so a markdown body returned beside them stays prose.
    runners = {n for n, f in funcs.items() if raw_output(f, parse=False)}
    tuple_out: dict[str, tuple[bool, ...]] = {}

    def shape(f):
        parsed: set[str] = set()

        def derived(e) -> bool:
            return bool(calls(e) & PARSE_CALLS or names(e) & parsed
                        or {c.split(".")[-1] for c in calls(e)} & runners)
        while True:
            size = len(parsed)
            for targets, value, forced in bindings(f):
                if forced or derived(value):
                    parsed |= {t.id for t in targets}
            if len(parsed) == size:
                break
        rets = [r.value for r in ast.walk(f) if isinstance(r, ast.Return) and r.value is not None]
        if any(not isinstance(r, ast.Tuple) and derived(r) for r in rets):
            return True
        tups = [r for r in rets if isinstance(r, ast.Tuple)]
        width = max((len(r.elts) for r in tups), default=0)
        flags = tuple(any(len(r.elts) == width and derived(r.elts[i]) for r in tups) for i in range(width))
        return flags if any(flags) else None

    def bindings(scope):
        for n in ast.walk(scope):
            if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and n.value is not None:
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                flags = tuple_out.get(_dotted(n.value.func).split(".")[-1]) if isinstance(n.value, ast.Call) else None
                if flags and len(targets) == 1 and isinstance(targets[0], (ast.Tuple, ast.List)) \
                        and len(targets[0].elts) == len(flags):
                    for elt, flag in zip(targets[0].elts, flags):
                        yield [t for t in ast.walk(elt) if isinstance(t, ast.Name)], n.value, flag
                    continue
                yield [t for tg in targets for t in ast.walk(tg) if isinstance(t, ast.Name)], n.value, False
            elif isinstance(n, (ast.For, ast.comprehension)):
                yield [t for t in ast.walk(n.target) if isinstance(t, ast.Name)], n.iter, False
            elif isinstance(n, ast.withitem) and n.optional_vars is not None:
                yield [t for t in ast.walk(n.optional_vars) if isinstance(t, ast.Name)], n.context_expr, False

    while True:
        more_r = {n for n, f in funcs.items() if n not in runners
                  and {c.split(".")[-1] for c in calls(f)} & runners}
        shapes = {n: shape(f) for n, f in funcs.items() if n not in runners | more_r}
        more_r |= {n for n, s in shapes.items() if s is True}
        new_t = {n: s for n, s in shapes.items() if isinstance(s, tuple) and n not in more_r}
        if not more_r and new_t == tuple_out:
            break
        runners |= more_r
        tuple_out = new_t
    readers = {n for n, f in funcs.items() if raw_read(f) and n not in runners}
    while True:
        more_m = {n for n, f in funcs.items() if n not in readers | runners
                  and {c.split(".")[-1] for c in calls(f)} & readers}
        if not more_m:
            break
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

    def copy_read(node) -> bool:
        """The value is a plain read of a path naming a skill, agent or reference file (a copy
        of prose, even under a temp dir), with no runner or parse call on the way."""
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in READ_ATTRS):
            return False
        seg = ast.get_source_segment(text, node.func.value) or ""
        called = calls(node.func.value)
        return bool(PRODUCTION_MD.search(seg)) and not NON_PROSE_PATH.search(seg) and not (
            called & (RUNNER_CALLS | PARSE_CALLS) or {c.split(".")[-1] for c in called} & runners)

    def taint(scope, md, out):
        md, out = set(md), set(out)
        while True:
            size = len(md) + len(out)
            for targets, value, parsed in bindings(scope):
                ids = {t.id for t in targets}
                if not parsed and copy_read(value):
                    md |= ids
                elif parsed or is_output(value, out):
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
        if isinstance(node, ast.JoinedStr):  # an f-string: its constant parts, `{}` for each value
            return "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in node.values)
        return None

    def re_bound(scope) -> dict[str, str]:
        """Names bound to `re.compile(<literal>)` in scope (not descending into functions for the module)."""
        nodes = scope.body if isinstance(scope, ast.Module) else list(ast.walk(scope))
        return {t.id: literal(n.value.args[0]) for n in nodes if isinstance(n, ast.Assign)
                and isinstance(n.value, ast.Call) and _dotted(n.value.func) == "re.compile"
                and n.value.args and literal(n.value.args[0]) is not None
                for t in n.targets if isinstance(t, ast.Name)}

    parent = {id(ch): p for p in ast.walk(tree) for ch in ast.iter_child_nodes(p)}

    def nots(node, root) -> int:
        n, x = 0, node
        while x is not root and id(x) in parent:
            x = parent[id(x)]
            n += isinstance(x, ast.UnaryOp) and isinstance(x.op, ast.Not)
        return n

    mod_md, mod_out = taint(ast.Module(body=[n for n in tree.body if not isinstance(
        n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))], type_ignores=[]), set(), set())
    mod_re = re_bound(tree)
    nested = {id(g) for f in funcs.values() for g in ast.walk(f) if g is not f and g in funcs.values()}
    top = [f for f in funcs.values() if id(f) not in nested]  # a nested helper is read with its parent
    fed: dict[str, set[str]] = {}  # helper -> parameters that receive markdown text at some call site

    def scope_taint(f):
        own = {a.arg for a in f.args.args}  # a local fixture of that name decides the parameter
        fed_here = set().union(*(fed.get(g.name, set()) for g in ast.walk(f)
                                 if isinstance(g, (ast.FunctionDef, ast.AsyncFunctionDef))))
        return taint(f, mod_md | (own & readers) | fed_here, mod_out | (own & runners))

    while True:
        size = sum(map(len, fed.values()))
        for f in top:
            md, out = scope_taint(f)
            for c in ast.walk(f):
                if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in funcs:
                    gp = [a.arg for a in funcs[c.func.id].args.args]
                    got = {gp[i] for i, a in enumerate(c.args) if i < len(gp)
                           and not isinstance(a, ast.Starred) and is_md(a, md, out)}
                    got |= {k.arg for k in c.keywords if k.arg in gp and is_md(k.value, md, out)}
                    if got:
                        fed.setdefault(c.func.id, set()).update(got)
        if sum(map(len, fed.values())) == size:
            break

    rows: list[dict] = []
    seen: set[tuple] = set()

    def add(line, fname, lit, form, regex=False) -> None:
        got = literal_class(lit, regex) if lit is not None else None
        if got and (line, lit, form) not in seen:
            seen.add((line, lit, form))
            rows.append({"line": line, "func": fname, "literal": lit, "form": form,
                         "cls": got[0], "reason": got[1]})

    comps = (ast.ListComp, ast.SetComp, ast.GeneratorExp)
    str_methods = {"lower", "casefold", "strip", "upper"}

    def local_colls(f) -> dict:
        return {**mod_colls, **{t.id: n.value for n in ast.walk(f) if isinstance(n, ast.Assign)
                                and isinstance(n.value, (ast.Tuple, ast.List, ast.Set, ast.Dict))
                                for t in n.targets if isinstance(t, ast.Name)}}

    def parametrized(f) -> dict[str, list]:
        """Test parameters bound by `@pytest.mark.parametrize("a,b", [...])` to the values they take."""
        got: dict[str, list] = {}
        for d in f.decorator_list:
            if isinstance(d, ast.Call) and _dotted(d.func).endswith("parametrize") and len(d.args) >= 2 \
                    and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str) \
                    and isinstance(d.args[1], (ast.List, ast.Tuple)):
                argn = [a.strip() for a in d.args[0].value.split(",") if a.strip()]
                for row in d.args[1].elts:
                    vals = [row] if len(argn) == 1 else (
                        row.elts if isinstance(row, (ast.Tuple, ast.List)) else [])
                    for a, v in zip(argn, vals):
                        got.setdefault(a, []).append(v)
        return got

    # ctx = (collections by name, parameter values by name). A needle is followed through a
    # named collection or dict, `.items()`/`.values()`/`.keys()`, loop and comprehension targets
    # (tuple targets too) and parameters, to the string values it can hold.
    def values_of(node, ctx, depth=0) -> list:
        if depth > 8:
            return []
        if isinstance(node, ast.Name):
            got = bound(node, ctx, depth)
            if got is not None:
                return got
            if node.id in ctx[0]:
                return [ctx[0][node.id]]
            if node.id in ctx[1]:
                return ctx[1][node.id]
        return [node]

    def elems(it, ctx, depth=0) -> list:
        if depth > 8:
            return []
        if isinstance(it, ast.Call):
            fn = it.func
            if isinstance(fn, ast.Name) and fn.id in ("sorted", "list", "tuple", "set", "reversed") and it.args:
                return elems(it.args[0], ctx, depth + 1)
            if isinstance(fn, ast.Attribute) and fn.attr in ("items", "values", "keys") and not it.args:
                got = []
                for d in values_of(fn.value, ctx, depth + 1):
                    if isinstance(d, ast.Dict):
                        for k, v in zip(d.keys, d.values):
                            if k is not None:
                                got.append(ast.Tuple(elts=[k, v]) if fn.attr == "items"
                                           else k if fn.attr == "keys" else v)
                return got
            return []
        got = []
        for v in values_of(it, ctx, depth + 1):
            if isinstance(v, (ast.Tuple, ast.List, ast.Set)):
                got += v.elts
            elif isinstance(v, ast.Dict):
                got += [k for k in v.keys if k is not None]
        return got

    def destructure(target, name, value, ctx, depth) -> list:
        if isinstance(target, ast.Name):
            return [value] if target.id == name else []
        got = []
        if isinstance(target, (ast.Tuple, ast.List)):
            for v in values_of(value, ctx, depth + 1):
                if isinstance(v, (ast.Tuple, ast.List)) and len(v.elts) == len(target.elts):
                    for t, e in zip(target.elts, v.elts):
                        got += destructure(t, name, e, ctx, depth + 1)
        return got

    def bound(node, ctx, depth):
        """What the nearest enclosing `for` or comprehension binding node's name iterates, or None."""
        x = node
        while id(x) in parent:
            p = parent[id(x)]
            gens = p.generators if isinstance(p, comps) else [p] if isinstance(p, ast.For) and x is not p.iter else []
            for g in gens:
                if any(isinstance(t, ast.Name) and t.id == node.id for t in ast.walk(g.target)):
                    return [v for e in elems(g.iter, ctx, depth + 1)
                            for v in destructure(g.target, node.id, e, ctx, depth + 1)]
            x = p
        return None

    def lits(node, ctx, pids) -> list[str]:
        """Needle literals of an expression (with pids, only values a call site passed in)."""
        while isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in str_methods and not node.args:
            node = node.func.value
        vals = values_of(node, ctx) if isinstance(node, ast.Name) else [node]
        return [literal(v) for v in vals if literal(v) is not None and (pids is None or id(v) in pids)]

    def stored(c) -> bool:
        """A positive `in` whose statement stores or passes its value (not assert, if or return,
        which have their own forms), outside a comprehension filter unless that comprehension is
        a `next(...)` first-match lookup (a miss yields the default)."""
        n, x = 0, c
        while id(x) in parent:
            p = parent[id(x)]
            n += isinstance(p, ast.UnaryOp) and isinstance(p.op, ast.Not)
            if isinstance(p, ast.comprehension) and any(x is i for i in p.ifs):
                comp = parent.get(id(p))
                up = parent.get(id(comp))
                if not (isinstance(up, ast.Call) and _dotted(up.func) == "next" and up.args and up.args[0] is comp):
                    return False
            if isinstance(p, ast.stmt):
                return isinstance(p, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Expr)) and n % 2 == 0
            x = p
        return False

    def scan(f, fname, ctx, pids=None, at=None) -> None:
        md, out = scope_taint(f)
        bound_re = {**mod_re, **re_bound(f)}

        def put(line, lit, form, regex=False) -> None:
            add(at or line, fname, lit, form if at is None else f"{form} via {f.name}()", regex)

        def required(c, form) -> None:
            if is_md(c.comparators[0], md, out):
                for s in lits(c.left, ctx, pids):
                    put(c.lineno, s, form)

        for node in ast.walk(f):
            if isinstance(node, ast.Assert):
                for c in ast.walk(node.test):
                    if isinstance(c, ast.Compare) and len(c.ops) == 1:
                        left, right = c.left, c.comparators[0]
                        if isinstance(c.ops[0], ast.In):
                            required(c, "assert in")
                        elif isinstance(c.ops[0], ast.Eq) and not isinstance(left, ast.Call):
                            for a, b in ((left, right), (right, left)):
                                if is_md(b, md, out):
                                    for s in lits(a, ctx, pids):
                                        put(c.lineno, s, "assert ==")
                        if isinstance(c.ops[0], (ast.Eq, ast.GtE, ast.Gt)) and isinstance(left, ast.Call) \
                                and isinstance(left.func, ast.Attribute) and left.func.attr == "count" \
                                and left.args and isinstance(right, ast.Constant) \
                                and isinstance(right.value, int) and right.value >= 1 \
                                and is_md(left.func.value, md, out):
                            # `text.count(<literal>) == 1`: present, not "at most once"
                            for s in lits(left.args[0], ctx, pids):
                                put(c.lineno, s, "assert count")
                    elif isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) \
                            and c.func.attr in ("startswith", "endswith") and c.args \
                            and is_md(c.func.value, md, out):
                        arg = c.args[0]
                        for e in (arg.elts if isinstance(arg, ast.Tuple) else [arg]):
                            for s in lits(e, ctx, pids):
                                put(c.lineno, s, f"assert .{c.func.attr}()")
            elif isinstance(node, ast.If):
                if all(isinstance(b, (ast.Continue, ast.Pass)) for b in node.body):
                    continue  # a filter, not a requirement
                for c in ast.walk(node.test):
                    if isinstance(c, ast.Compare) and len(c.ops) == 1 and isinstance(c.ops[0], (ast.In, ast.NotIn)) \
                            and isinstance(c.ops[0], ast.NotIn) != (nots(c, node.test) % 2 == 1):
                        required(c, "if requires")
            elif isinstance(node, ast.Return) and node.value is not None:
                for c in ast.walk(node.value):
                    if isinstance(c, ast.Compare) and len(c.ops) == 1 and isinstance(c.ops[0], ast.In) \
                            and nots(c, node.value) == 0:
                        required(c, "return in")
            elif isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], ast.In) \
                    and stored(node):
                required(node, "stored in")
            elif isinstance(node, comps):
                for g in node.generators:
                    if not isinstance(g.target, ast.Name):
                        continue
                    for cond in g.ifs:
                        for c in ast.walk(cond):
                            if isinstance(c, ast.Compare) and isinstance(c.left, ast.Name) \
                                    and c.left.id == g.target.id and isinstance(c.ops[0], ast.NotIn) \
                                    and is_md(c.comparators[0], md, out):
                                for s in [s for e in elems(g.iter, ctx) for s in lits(e, ctx, pids)]:
                                    put(c.lineno, s, "collected when not in")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                attr, recv = node.func.attr, node.func.value
                if attr in ("index", "rindex") and node.args and is_md(recv, md, out):
                    for s in lits(node.args[0], ctx, pids):
                        put(node.lineno, s, f".{attr}()")
                elif attr in ("search", "match", "fullmatch", "findall", "finditer"):
                    pats = []
                    if isinstance(recv, ast.Name) and recv.id == "re":
                        if len(node.args) >= 2 and is_md(node.args[1], md, out):
                            pats = lits(node.args[0], ctx, pids)
                    elif node.args and is_md(node.args[0], md, out):
                        if isinstance(recv, ast.Call) and recv.args and _dotted(recv.func) == "re.compile":
                            pats = lits(recv.args[0], ctx, pids)
                        elif isinstance(recv, ast.Name) and recv.id in bound_re and pids is None:
                            pats = [bound_re[recv.id]]
                    up = parent.get(id(node))
                    negated = (isinstance(up, ast.UnaryOp) and isinstance(up.op, ast.Not)) or (
                        isinstance(up, ast.Compare) and isinstance(up.ops[0], ast.Is))
                    x = node  # in an `if` test it is required only when negated; a filter never is
                    while id(x) in parent and not isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        p = parent[id(x)]
                        if isinstance(p, ast.If) and x is p.test:
                            negated = nots(node, p.test) % 2 == 0 or all(
                                isinstance(b, (ast.Continue, ast.Pass)) for b in p.body)
                            break
                        if isinstance(p, ast.comprehension) and x in p.ifs:
                            negated = True
                            break
                        x = p
                    if not negated:
                        for pat in pats:
                            put(node.lineno, pat, f"re.{attr}", regex=True)

    for f in top:
        ctx = (local_colls(f), parametrized(f))
        scan(f, f.name, ctx)
        # A literal passed to a local helper that requires it of markdown text: judged on the
        # call line, only for calls that pass markdown text in (a synthetic self-test does not).
        md, out = scope_taint(f)
        for c in ast.walk(f):
            if not (isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in funcs
                    and funcs[c.func.id] is not f):
                continue
            args = [a.value if isinstance(a, ast.Starred) else a for a in c.args] + [k.value for k in c.keywords]
            if not any(is_md(a, md, out) for a in args):
                continue
            h = funcs[c.func.id]
            gp = [a.arg for a in h.args.args]
            params: dict[str, list] = {}
            i = 0
            for a in c.args:
                vals = [values_of(e, ctx) for e in elems(a.value, ctx)] if isinstance(a, ast.Starred) else [
                    values_of(a, ctx)]
                for v in vals:
                    if i < len(gp):
                        params.setdefault(gp[i], []).extend(v)
                    i += 1
            for k in c.keywords:
                if k.arg in gp:
                    params.setdefault(k.arg, []).extend(values_of(k.value, ctx))
            pids = {id(n) for vs in params.values() for v in vs for n in ast.walk(v)}
            scan(h, f.name, (local_colls(h), params), pids, c.lineno)
    return sorted(rows, key=lambda r: (r["line"], r["literal"]))


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
    # Batch 3 (W3-01): the graduated build-adversary program.
    "loom-code/tests/test_adversarial_batch3_census_misses.py": (
        "behavior",
        "runs this classifier (path-loaded) and asserts on its result; the "
        "direct-pin hit is a synthetic test source string fed to "
        "direct_pin_lines, and the residual check asserts named files carry "
        "no skill sentence, an absence",
    ),
}


# Batch 3 kept these on purpose (census-report "Known limits"); --candidates lists each
# matching line as class kept-batch3 instead of prose or structural.
KEPT_BATCH3 = {
    "loom-workflow/tests/loom-visualization/test_templates.py": (
        r"assert .*pinned_sentence_ok\(s\b",
        "batch-3 kept gate polarity check (MERMAID_PIN, TABLE_ASCII_PIN, CHAT_PROCEEDS_PIN): "
        "reads only sentences in the mermaid-only-when-confirmed and obsidian-boundary gate "
        "blocks and fails a negated sentence; the literals pass through a parameter",
    ),
    "loom-workflow/tests/decision-map/test_skill_doc.py": (
        r"defaultPrompt",
        "batch-3 kept interface string: the Codex manifest defaultPrompt, not skill prose",
    ),
}
PLUGIN_ORDER = (("tests", "root tests"), ("loom-code", "loom-code"),
                ("loom-design", "loom-design"), ("loom-workflow", "loom-workflow"))


def candidates_report(roots: list[str]) -> str:
    """Markdown of every pin_candidates row under roots, grouped by plugin then file."""
    import ast

    by_plugin: dict[str, dict[str, list[dict]]] = {label: {} for _, label in PLUGIN_ORDER}
    for root in roots:
        for p in sorted((REPO / root).rglob("*.py")):
            key = p.relative_to(REPO).as_posix()
            text = code_only(p.read_text(encoding="utf-8", errors="replace"))
            rows = pin_candidates(text)
            if key in KEPT_BATCH3:
                pat, reason = KEPT_BATCH3[key]
                tops = [(n.lineno, n.end_lineno, n.name) for n in ast.parse(text).body
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                for i, line in enumerate(text.splitlines(), 1):
                    if re.search(pat, line):
                        rows = [r for r in rows if r["line"] != i]
                        func = next((nm for a, b, nm in tops if a <= i <= b), "<module>")
                        rows.append({"line": i, "func": func, "literal": line.strip(), "form": "kept line",
                                     "cls": "kept-batch3", "reason": reason})
            if rows:
                label = next((lb for pre, lb in PLUGIN_ORDER[1:] if key.startswith(pre + "/")), "root tests")
                by_plugin[label][key] = sorted(rows, key=lambda r: (r["line"], r["literal"]))

    out = ["| plugin | prose | structural | kept-batch3 | files with >=1 prose candidate |",
           "|---|---|---|---|---|"]
    total = {"prose": 0, "structural": 0, "kept-batch3": 0, "files": 0}
    for _, label in PLUGIN_ORDER:
        rows = [r for rs in by_plugin[label].values() for r in rs]
        n = {c: sum(r["cls"] == c for r in rows) for c in ("prose", "structural", "kept-batch3")}
        n["files"] = sum(any(r["cls"] == "prose" for r in rs) for rs in by_plugin[label].values())
        total = {k: total[k] + n[k] for k in total}
        out.append(f"| {label} | {n['prose']} | {n['structural']} | {n['kept-batch3']} | {n['files']} |")
    out.append(f"| **total** | {total['prose']} | {total['structural']} | {total['kept-batch3']} | {total['files']} |")
    for _, label in PLUGIN_ORDER:
        out += ["", f"## {label}", ""]
        for key, rows in by_plugin[label].items():
            out += [f"### {key}", "", "| file:line | function | literal / form | class | reason |",
                    "|---|---|---|---|---|"]
            for r in rows:
                lit = repr(r["literal"]).replace("|", "\\|")
                out.append(f"| {key}:{r['line']} | {r['func']} | {lit} ({r['form']}) | {r['cls']} | {r['reason']} |")
            out.append("")
        out += [f"### Decisions — {label}", "", "(W1 implementers: one row per candidate judged.)"]
    return "\n".join(out) + "\n"


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Census classifier for the prose-pin stock cleanup.")
    parser.add_argument("--roots", default=",".join(DEFAULT_ROOTS), help="comma-separated test roots")
    parser.add_argument("--count-exec", metavar="DIR", help="count executing test functions under DIR")
    parser.add_argument("--list", action="store_true", help="with --count-exec, print each counted function")
    parser.add_argument("--candidates", action="store_true", help="print every pin candidate as markdown")
    args = parser.parse_args()
    if args.candidates:
        print(candidates_report([r for r in args.roots.split(",") if r]), end="")
        return 0
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
