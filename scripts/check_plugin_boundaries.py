#!/usr/bin/env python3
"""Reject references that couple one plugin to another's files.

The checker scans Markdown, ``hooks*.json`` files, shell scripts (``.sh`` files
and extensionless files with any other shebang, such as hooks) and Python
scripts (``.py`` files and extensionless files with a python shebang) below a
single plugin root.  In Markdown it reports relative
links whose lexically resolved path leaves that root.  In all of them it
reports path references to another ``loom-*`` plugin's
private ``hooks/``, ``skills/``, ``scripts/``, ``contract/`` or ``agents/``
tree, a ``<loom-*>`` placeholder naming another plugin, and ``loom_checker``
outside loom-code.  Scripts are scanned outside loom-code only, whose own
scripts are repository-wide tools.  In scripts, comments and docstrings are
skipped (they are never executed as a path), and so is the plugin's top-level
``tests/`` tree, which is development-only.  In Python it also reports a
logical line where a literal ``"loom-*"`` plugin name is followed by a literal
private tree name (a path join); a join whose plugin name is a variable is a
known blind spot.  In shell, a ``#`` after whitespace is cut as a comment even
inside quotes, so a path later on that line is a known blind spot too.
Plugin-qualified skill names such as
``loom-code:using-loom-code`` are public names and are therefore allowed.

The files it scans are what git says belongs to the repository under that
plugin root, via ``repo_files.repository_files``: passing a subdirectory scopes
the listing to that subtree, so an ignored directory and a linked worktree
checked out inside the plugin contribute no violation.  That module ships with
loom-code and is reached across trees by sys.path, as
``loom-design/tests/spec/test_write_spec_contract.py`` already does.

Stdlib only, that module included.  ``find_boundary_violations`` is the
hermetic test surface; the CLI exits non-zero and prints each violation when
passed a plugin root.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import sys
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "loom-code" / "scripts"))

from repo_files import repository_files  # noqa: E402


_LINK_RE = re.compile(r"\]\((?P<target>[^)]+)\)")
_REFERENCE_LINK_RE = re.compile(
    r"^\s{0,3}\[[^]]+\]:\s*(?P<target><[^>]+>|\S+)"
)
_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_SIBLING_INTERNAL_RE = re.compile(
    r"(?<![A-Za-z0-9_./:-])"
    r"(?P<target>(?:(?:/|(?:\.{1,2}|[A-Za-z0-9_.-]+)/))*"
    r"(?P<plugin>loom-[a-z0-9-]+)"
    r"/(?:hooks|skills|scripts|contract|agents)/[A-Za-z0-9_./-]+)"
)
_PLACEHOLDER_RE = re.compile(r"<(?P<plugin>loom-[a-z0-9-]+)>")
_CHECKER_RE = re.compile(r"\bloom_checker\b")
# loom-code owns the checker; its scripts are repository-wide tools that name
# sibling paths as repository data, so scripts are scanned in the other plugins.
_CHECKER_OWNER = "loom-code"
_SHELL_COMMENT_RE = re.compile(r"(?:^|\s)#.*$")
_PLUGIN_NAME_RE = re.compile(r"loom-[a-z0-9-]+")
_PRIVATE_TREES = {"hooks", "skills", "scripts", "contract", "agents"}


def _is_python_script(path: Path) -> bool:
    """A ``.py`` file, or an extensionless file with a python shebang."""
    if path.suffix == ".py":
        return True
    if path.suffix:
        return False
    try:
        with path.open("rb") as handle:
            first = handle.readline()
    except OSError:
        return False
    return first.startswith(b"#!") and b"python" in first


def _is_shell_script(path: Path) -> bool:
    """A ``.sh`` file, or an extensionless file with a non-python shebang."""
    if path.suffix == ".sh":
        return True
    if path.suffix:
        return False
    try:
        with path.open("rb") as handle:
            first = handle.readline()
    except OSError:
        return False
    return first.startswith(b"#!") and b"python" not in first


def _script_lines(text: str) -> list[tuple[int, str]]:
    """Numbered code lines with comments cut and docstring lines dropped."""
    docstring_lines: set[int] = set()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        tree = None
    if tree is not None:
        for node in ast.walk(tree):
            if not isinstance(
                node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ) or not node.body:
                continue
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                docstring_lines.update(range(first.lineno, first.end_lineno + 1))
    comment_cols: dict[int, int] = {}
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type == tokenize.COMMENT:
                comment_cols[token.start[0]] = token.start[1]
    except (tokenize.TokenError, SyntaxError):
        comment_cols = {}
        for number, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("#"):
                comment_cols[number] = 0
    return [
        (number, line[: comment_cols.get(number, len(line))])
        for number, line in enumerate(text.splitlines(), start=1)
        if number not in docstring_lines
    ]


def _shell_lines(text: str) -> list[tuple[int, str]]:
    """Numbered shell lines with ``#`` comments (line or trailing) cut."""
    return [
        (number, _SHELL_COMMENT_RE.sub("", line))
        for number, line in enumerate(text.splitlines(), start=1)
    ]


def _path_joins(text: str) -> list[tuple[int, str, str]]:
    """``(line, plugin, tree)`` for each logical Python line where a string
    literal equal to a ``loom-*`` name is followed by one equal to a private
    tree name, as in ``root / "loom-code" / "contract"``."""
    hits: list[tuple[int, str, str]] = []
    strings: list[str] = []
    start = 0
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type == tokenize.STRING:
                start = start or token.start[0]
                try:
                    value = ast.literal_eval(token.string)
                except (ValueError, SyntaxError):
                    continue
                if isinstance(value, str):
                    strings.append(value)
            elif token.type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                # The tree must follow the plugin name, so an own skill named
                # like a plugin ("skills", "loom-visualization") stays clean.
                hits.extend(
                    (start, plugin, tree)
                    for plugin, tree in zip(strings, strings[1:])
                    if _PLUGIN_NAME_RE.fullmatch(plugin) and tree in _PRIVATE_TREES
                )
                strings, start = [], 0
    except (tokenize.TokenError, SyntaxError):
        pass
    return hits


def _is_archival_markdown(root: Path, markdown: Path) -> bool:
    """Return whether a Markdown file records history, not install behavior."""
    relative = markdown.relative_to(root)
    return (
        (len(relative.parts) == 1 and markdown.name.startswith("CHANGELOG"))
        or (len(relative.parts) == 1 and markdown.name == "TECH-SPEC.md")
        or relative.parts[0] == "research"
    )


def _link_path(raw_target: str) -> str | None:
    """Return the filesystem portion of a relative Markdown link."""
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        # This checker follows the repository's title-less-link convention,
        # while tolerating a conventional quoted title if one appears.
        target = re.split(r'\s+["\']', target, maxsplit=1)[0]
    if not target or target.startswith(("#", "/", "//")):
        return None
    if _SCHEME_RE.match(target):
        return None
    return target.split("#", 1)[0].split("?", 1)[0]


def _escapes(root: Path, source: Path, target: str) -> bool:
    resolved = (source.parent / target).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        return True
    return False


def _plugin_name(root: Path) -> str:
    """Read installed identity from the Claude manifest, else use dirname."""
    manifest = root / ".claude-plugin" / "plugin.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        name = data.get("name")
        if isinstance(name, str) and name:
            return name
    return root.name


def _is_internal_path(root: Path, plugin: str, target: str) -> bool:
    """Whether a ``loom-*``-shaped match names this plugin's OWN skill folder
    rather than a sibling plugin's private tree.

    A plugin may ship a skill whose directory name happens to look like a
    sibling plugin — ``loom-workflow/skills/loom-memory/`` is the case this
    exists for. Only that shape is exempt: the target must resolve to a real
    path under this plugin's ``skills/<plugin>/``.

    An earlier version exempted anything that merely resolved to an existing
    path under the plugin root, which let a decoy defeat the gate: a file
    planted at ``<root>/loom-code/scripts/loom_checker.py`` made a genuine
    reference to the real sibling's private script read as internal. Requiring
    the ``skills/<plugin>/`` prefix, and refusing the exemption outright when a
    real sibling plugin of that name exists, closes that.
    """
    if _sibling_plugin_exists(root, plugin):
        return False
    candidate = target[1:] if target.startswith("/") else target
    resolved = (root / candidate).resolve(strict=False)
    own_skill = (root / "skills" / plugin).resolve(strict=False)
    try:
        resolved.relative_to(own_skill)
    except ValueError:
        return False
    return resolved.exists()


def _sibling_plugin_exists(root: Path, plugin: str) -> bool:
    """True when ``plugin`` is a real installable plugin beside this one.

    Checks both the flat install shape (``<plugin>/.claude-plugin/
    plugin.json``) and the versioned-install shape this repo's own suite
    proves is real (``<plugin>/<version>/.claude-plugin/plugin.json``), and
    checks both from ``root``'s own parent (when ``root`` itself is flat)
    and from ``root``'s grandparent (when ``root`` itself is a version
    directory, e.g. ``.../loom-design/0.4.0``, so the sibling's install
    root sits beside ``loom-design``, not beside ``0.4.0``).

    An earlier version checked only the flat shape from ``root``'s parent,
    so a sibling installed under a version directory went undetected — the
    bare ``root/skills/<plugin>/`` existence check in ``_is_internal_path``
    then let a same-named decoy through exactly as before the flat-layout
    fix.
    """
    resolved_root = root.resolve(strict=False)
    bases = {resolved_root.parent, resolved_root.parent.parent}
    for base in bases:
        sibling_base = base / plugin
        if (sibling_base / ".claude-plugin" / "plugin.json").is_file():
            return True
        if sibling_base.is_dir():
            for child in sibling_base.iterdir():
                if child.is_dir() and (child / ".claude-plugin" / "plugin.json").is_file():
                    return True
    return False


def find_boundary_violations(plugin_root: str | Path) -> list[str]:
    """Return stable ``file:line: reason: target`` boundary violations."""
    root = Path(plugin_root).resolve(strict=True)
    plugin_name = _plugin_name(root)
    violations: list[str] = []

    for source in sorted(repository_files(root)):
        if source.suffix == ".md":
            if _is_archival_markdown(root, source):
                continue
            lines = list(
                enumerate(source.read_text(encoding="utf-8").splitlines(), start=1)
            )
            is_markdown = True
        elif source.suffix == ".json" and source.name.startswith("hooks"):
            lines = list(
                enumerate(source.read_text(encoding="utf-8").splitlines(), start=1)
            )
            is_markdown = False
        elif _is_shell_script(source) or _is_python_script(source):
            if plugin_name == _CHECKER_OWNER or source.relative_to(root).parts[0] == "tests":
                continue
            text = source.read_text(encoding="utf-8")
            is_markdown = False
            if _is_shell_script(source):
                lines = _shell_lines(text)
            else:
                lines = _script_lines(text)
                violations.extend(
                    f"{source}:{number}: sibling path join: {plugin}/{tree}"
                    for number, plugin, tree in _path_joins(text)
                    if plugin != plugin_name
                )
        else:
            continue
        for line_number, line in lines:
            reported_link_spans: list[tuple[int, int]] = []
            link_matches = list(_LINK_RE.finditer(line)) if is_markdown else []
            reference_match = _REFERENCE_LINK_RE.match(line) if is_markdown else None
            if reference_match:
                link_matches.append(reference_match)
            for match in sorted(link_matches, key=lambda item: item.start("target")):
                target = _link_path(match.group("target"))
                if target and _escapes(root, source, target):
                    reported_link_spans.append(match.span("target"))
                    violations.append(
                        f"{source}:{line_number}: escaping relative link: {target}"
                    )

            for match in _SIBLING_INTERNAL_RE.finditer(line):
                if match.group("plugin") == plugin_name:
                    continue
                if _is_internal_path(root, match.group("plugin"), match.group("target")):
                    continue
                start, end = match.span("target")
                if any(
                    start >= link_start and end <= link_end
                    for link_start, link_end in reported_link_spans
                ):
                    continue
                reported_link_spans.append((start, end))
                violations.append(
                    f"{source}:{line_number}: sibling internal path: "
                    f"{match.group('target')}"
                )

            for match in _PLACEHOLDER_RE.finditer(line):
                if match.group("plugin") != plugin_name:
                    violations.append(
                        f"{source}:{line_number}: sibling placeholder path: "
                        f"{match.group(0)}"
                    )
            # A checker token already inside a reported path is not reported twice.
            if plugin_name != _CHECKER_OWNER and any(
                not any(s <= m.start() and m.end() <= e for s, e in reported_link_spans)
                for m in _CHECKER_RE.finditer(line)
            ):
                violations.append(
                    f"{source}:{line_number}: sibling checker reference: loom_checker"
                )

    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_root", type=Path)
    args = parser.parse_args(argv)
    violations = find_boundary_violations(args.plugin_root)
    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        print(f"FAIL: {len(violations)} plugin-boundary violation(s).", file=sys.stderr)
        return 1
    print(f"OK: {args.plugin_root} is filesystem-boundary clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
