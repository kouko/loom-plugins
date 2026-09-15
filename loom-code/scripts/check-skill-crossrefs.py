#!/usr/bin/env python3
"""CI gate: dead-link validator for loom-code skill cross-references.

Walks every ``loom-code/skills/*/SKILL.md``, every single-level skill
subfolder file ``skills/*/*/*.md`` (references/, agents/, ...) and the
plugin-level ``agents/*.md`` and ``references/*.md``. For each RELATIVE markdown link
``](path)``, resolves the target against the reading file's directory and
asserts the target exists on disk. For each backtick span naming a
``.md`` path with a ``/``, asserts it exists relative to the file's
directory, its skill directory, the plugin root or the repository root;
placeholders (``< > * { } $``), URLs, absolute paths and ``docs/``
protocol paths are skipped.

Skipped (not a relative on-disk target):
- ``http://`` / ``https://`` URLs
- anchor-only links (``#section``)
- absolute paths (``/etc/...``)

A trailing ``#anchor`` on an otherwise-relative link is stripped before
the existence check (e.g. ``references/guide.md#step-2`` checks
``references/guide.md``).

Caveat: of markdown links, only INLINE links ``](target)`` are checked.
Reference-style link definitions (``[id]: path``) and inline links carrying a title
attribute (``](path "title")``) are NOT covered — the loom-code SKILL.md
convention is title-less inline links, so this matches today's corpus; a
future author adding a reference-style link should not assume coverage.

- Exit 0: every relative cross-ref resolves.
- Exit 1: one or more targets are missing; each is printed to stderr as
  ``<skill-md-path>: <link>``.

Pure stdlib. The core scan is the importable function
``find_broken_crossrefs(skills_dir) -> list[str]`` so it can be tested
hermetically; the ``__main__`` block runs it over the real skills tree
(resolved relative to this script's location, so it works from the repo
root) and sets the exit code.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Markdown inline link: `](target)`. We only need the target group; the
# link text before `[` is irrelevant to existence checking.
_LINK_RE = re.compile(r"\]\(([^)]+)\)")

# Default skills tree, relative to this script: <repo>/loom-code/skills.
_DEFAULT_SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def _is_relative_ondisk_link(target: str) -> bool:
    """True only for links that name a relative on-disk path.

    Excludes URLs (scheme://), anchor-only links (#...), and absolute
    paths (/...). Protocol-relative ``//host`` is treated as external.
    """
    if target.startswith("#"):
        return False
    if target.startswith("/"):
        return False
    if "://" in target:
        return False
    return True


def _strip_anchor(target: str) -> str:
    """Drop a trailing ``#anchor`` fragment before the existence check."""
    return target.split("#", 1)[0]


def _scanned_documents(skills_dir: Path) -> list[Path]:
    """Every prose file whose relative links have to resolve.

    Agent files carry the same `](path)` links a SKILL.md does, and a
    station rename leaves them dangling just as easily — the five-station
    rewrite left a dead reference in `agents/implementer.md` that only an
    isolated-install test noticed. Both the per-skill `agents/` directory
    and the plugin-level one beside `skills/` are read.
    """
    found = list(skills_dir.glob("*/SKILL.md"))
    # Every single-level skill subfolder (references/, agents/, protocols/
    # ...): the flat-folder convention makes `*/*/*.md` exactly that set,
    # and a path copied one level down dangles in any of them alike.
    found += skills_dir.glob("*/*/*.md")
    found += skills_dir.parent.glob("agents/*.md")
    # Plugin-level shared rule files (dispatch-profile.md, ...) that
    # stations link; their paths resolve from their own directory, the
    # plugin root or the repository root.
    found += skills_dir.parent.glob("references/*.md")
    return sorted(set(found))


# A backtick span naming a `.md` path: at least one `/`, no whitespace.
_BACKTICK_MD_RE = re.compile(r"`([^`\s]+/[^`\s]*\.md)(?:#[^`\s]*)?`")

# A slash-free backtick `.md` name (`one-way-door.md`).
_BARE_MD_RE = re.compile(r"`([^`\s/]+\.md)(?:#[^`\s]*)?`")

# A backtick span used as link text: the link itself is checked above.
_LINK_TEXT_RE = re.compile(r"\[`[^`]*`\]\([^)]*\)")

# Bare names that are repository-root protocol files, not skill-relative.
_ROOT_PROTOCOL_NAMES = frozenset({
    "DESIGN.md", "PRINCIPLES.md", "README.md", "CHANGELOG.md", "AGENTS.md",
    "CLAUDE.md", "SKILL.md", "KICKOFF-DEFAULTS.md",
})

# A sentence that tells the reader to read or load a file.
_LOAD_VERB_RE = re.compile(r"\b(?:read|reads|load|loads|loaded)\b", re.I)


def _loaded_bare_names(text: str) -> list[str]:
    """Bare `.md` names inside a sentence that says to read or load a file.

    A bare name is only checked where the prose loads it: elsewhere it
    usually names a user-repo artifact (`plan.md`) or tool trivia
    (`report.md`) that is not a file beside the scanning document.
    Root protocol names and placeholders are skipped.
    """
    flat = " ".join(_LINK_TEXT_RE.sub(" ", text).split())
    names: list[str] = []
    for sentence in re.split(r"(?<=[.;!?])\s+", flat):
        if not _LOAD_VERB_RE.search(sentence):
            continue
        for name in _BARE_MD_RE.findall(sentence):
            if name in _ROOT_PROTOCOL_NAMES or _PLACEHOLDER_CHARS & set(name):
                continue
            names.append(name)
    return names

# Placeholder or glob characters: the span names a pattern, not a file.
_PLACEHOLDER_CHARS = set("<>*{}$")


def _is_checkable_backtick_path(path: str) -> bool:
    """True for a backtick path that should name a real file in this tree.

    Skips placeholders and globs, URLs, absolute or home paths, and
    `docs/` paths — those are runtime-repo protocol paths an adopting
    repo creates, not files this plugin ships.
    """
    if _PLACEHOLDER_CHARS & set(path):
        return False
    if "://" in path or path.startswith(("/", "~")):
        return False
    if path.startswith("docs/"):
        return False
    return True


def _backtick_bases(document: Path, skills_dir: Path) -> list[Path]:
    """Directories a backtick path may be written relative to.

    Prose names paths from the file's own directory, from its skill
    directory (a references file saying `references/lenses.md`), from the
    plugin root (`agents/reviewer.md`, `skills/x/SKILL.md`) or from the
    repository root (`loom-code/skills/...`). Resolving against any of
    them counts, so only a path that exists nowhere is reported.
    """
    plugin_root = skills_dir.parent
    bases = [document.parent]
    try:
        skill_name = document.relative_to(skills_dir).parts[0]
        bases.append(skills_dir / skill_name)
    except ValueError:
        pass
    bases += [plugin_root, plugin_root.parent]
    return bases


def find_broken_crossrefs(skills_dir) -> list[str]:
    """Return one ``<skill-md-path>: <link>`` string per broken cross-ref.

    Scans ``<skills_dir>/*/SKILL.md``, ``<skills_dir>/*/*/*.md`` and
    the plugin-level ``agents/*.md`` and ``references/*.md`` beside
    ``skills/``. A link is broken when its target (relative, anchor
    stripped) does not exist on disk relative to the reading file's own
    directory; a checkable backtick ``.md`` path is broken when it resolves
    against none of ``_backtick_bases``; a bare backtick name in a
    read/load sentence (``_loaded_bare_names``) is broken when it is not
    beside the reading file. Empty list == all references resolve.
    """
    skills_dir = Path(skills_dir)
    broken: list[str] = []
    for skill_md in _scanned_documents(skills_dir):
        text = skill_md.read_text(encoding="utf-8")
        base = skill_md.parent
        for raw_target in _LINK_RE.findall(text):
            target = raw_target.strip()
            if not _is_relative_ondisk_link(target):
                continue
            path_part = _strip_anchor(target)
            if not path_part:
                # Link was anchor-only after stripping (e.g. `]( #x)`).
                continue
            resolved = (base / path_part)
            if not resolved.exists():
                broken.append(f"{skill_md}: {target}")
        for path in _BACKTICK_MD_RE.findall(text):
            if not _is_checkable_backtick_path(path):
                continue
            bases = _backtick_bases(skill_md, skills_dir)
            if not any((b / path).exists() for b in bases):
                broken.append(f"{skill_md}: `{path}`")
        for name in _loaded_bare_names(text):
            if not (base / name).exists():
                broken.append(f"{skill_md}: `{name}`")
    return broken


def main() -> int:
    broken = find_broken_crossrefs(_DEFAULT_SKILLS_DIR)
    if broken:
        for entry in broken:
            print(entry, file=sys.stderr)
        print(
            f"\nFAIL: {len(broken)} broken skill cross-reference(s) "
            f"(target missing on disk).",
            file=sys.stderr,
        )
        return 1
    print("OK: all relative skill cross-references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
