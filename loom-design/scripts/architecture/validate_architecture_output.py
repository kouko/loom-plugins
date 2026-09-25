"""Validate a repository's ARCHITECTURE.md against the architecture tool's
authoring contract.

Valid iff:
  1. Exactly one well-formed `ratified-by: <name> <YYYY-MM-DD>` line is
     present. `--draft` also accepts a file without one (the
     pre-ratification check the tool runs before read-back); a malformed
     or second line is always invalid.
  2. A `## Decisions` section and the four rule sections appear as `## `
     headings — Module boundaries, File placement, File size, CI stages —
     and no other `## ` section (an Overview does not change agent
     behaviour). Decisions holds at least one non-blank line; its entries
     are prose and their wording is not checked. Rule sections may be empty.
  3. Every non-blank line under those sections is a rule line
     `- <ID> — <rule> — check: <guard path>` or `... — check: review`.
  4. Rule ids are unique across the file.
  5. Every `check:` guard path other than `review` is relative, stays inside
     the repository root (the file's parent directory) and exists there.
  6. No `## ` heading appears twice, and the sections come in schema order:
     Decisions, then the four rule sections in the order above.
  7. Above the first `## ` heading there is only the `# ` title, the
     `ratified-by:` line and blank lines.

Like design-system's validator, this blocks nothing downstream: it is the
authoring-side check the tool runs on its own output.

CLI: `python validate_architecture_output.py <ARCHITECTURE.md> [--draft]`
-> exit 0 if valid, exit 1 with agent-actionable messages on stderr.

Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

DECISIONS = "Decisions"
SECTIONS = ("Module boundaries", "File placement", "File size", "CI stages")

_RULE = re.compile(r"^- ([A-Z][A-Z0-9]*-\d+) — (\S.*?) — check: (\S+)\s*$")
_RATIFIED_BY_ANY = re.compile(r"^ratified-by:.*$", re.MULTILINE)
_RATIFIED_BY_WELLFORMED = re.compile(
    r"^ratified-by:\s*\S.*\s(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE
)


def _sections(text: str) -> dict[str, list[str]]:
    """Heading -> body lines, for every `## ` section, in file order."""
    sections: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def _check_top_matter(text: str) -> list[str]:
    """Above the first `## ` heading: one `# ` title, the ratified-by line, blanks."""
    problems = []
    title_seen = False
    for line in text.splitlines():
        if line.startswith("## "):
            break
        if line.startswith("# ") and not title_seen:
            title_seen = True
        elif line.strip() and not line.startswith("ratified-by:"):
            problems.append(f"line above the first '## ' section is not allowed; only the "
                            f"'# ' title and the 'ratified-by:' line go there: {line.strip()!r}")
    return problems


def _check_ratified_by(text: str, draft: bool) -> list[str]:
    if len(_RATIFIED_BY_ANY.findall(text)) > 1:
        return ["more than one 'ratified-by:' line; keep exactly one, replacing the old "
                "line when re-ratifying"]
    if _RATIFIED_BY_ANY.search(text) is None:
        if draft:
            return []
        return [
            "no 'ratified-by:' line; write 'ratified-by: <name> <YYYY-MM-DD>' "
            "under the title only after the user has said yes to the "
            "restatement (run with --draft to check a file before that)"
        ]
    match = _RATIFIED_BY_WELLFORMED.search(text)
    if match is None:
        return [
            "'ratified-by:' line is malformed; the grammar is "
            "'ratified-by: <name> <YYYY-MM-DD>'"
        ]
    try:
        date.fromisoformat(match.group(1))
    except ValueError:
        return [f"'ratified-by:' names {match.group(1)!r}, which is not a real date"]
    return []


def _check_rules(text: str, repo_root: Path) -> list[str]:
    problems = []
    sections = _sections(text)
    if DECISIONS not in sections:
        problems.append(f"missing section '## {DECISIONS}'; record each design choice "
                        f"there (choice, options considered, reason)")
    elif not any(line.strip() for line in sections[DECISIONS]):
        problems.append(f"section '## {DECISIONS}' is empty; record each design choice "
                        f"there (choice, options considered, reason)")
    for name in SECTIONS:
        if name not in sections:
            problems.append(f"missing section '## {name}'; the four rule sections are "
                            f"{', '.join(SECTIONS)}")
    for name in sections:
        if name not in SECTIONS and name != DECISIONS:
            problems.append(f"section '## {name}' is not allowed; ARCHITECTURE.md holds "
                            f"only '## {DECISIONS}' and the four rule sections "
                            f"({', '.join(SECTIONS)})")
    headings = [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]
    for name in dict.fromkeys(h for h in headings if headings.count(h) > 1):
        problems.append(f"section '## {name}' appears more than once; merge the copies")
    order = [h for h in dict.fromkeys(headings) if h == DECISIONS or h in SECTIONS]
    if order != [h for h in (DECISIONS, *SECTIONS) if h in order]:
        problems.append(f"sections are out of order; the order is '## {DECISIONS}', "
                        f"then {', '.join(SECTIONS)}")
    seen: set[str] = set()
    for name in SECTIONS:
        for line in sections.get(name, []):
            if not line.strip():
                continue
            match = _RULE.match(line)
            if match is None:
                problems.append(
                    f"line under '## {name}' breaks the rule grammar "
                    f"'- <ID> — <rule> — check: <guard path>|review': {line.strip()!r}"
                )
                continue
            rule_id, _, guard = match.groups()
            if rule_id in seen:
                problems.append(f"rule id {rule_id} is used twice; ids must be unique")
            seen.add(rule_id)
            if guard != "review" and (Path(guard).is_absolute() or not
                                      (repo_root / guard).resolve().is_relative_to(repo_root)):
                problems.append(f"rule {rule_id} names guard '{guard}', which is not a path "
                                f"inside the repository; write it relative to {repo_root}")
            elif guard != "review" and not (repo_root / guard).is_file():
                problems.append(
                    f"rule {rule_id} names guard '{guard}', which does not exist "
                    f"under {repo_root}; write the guard or mark the rule 'check: review'"
                )
    return problems


def validate(path: Path, draft: bool = False) -> tuple[bool, list[str]]:
    """Run all checks against the ARCHITECTURE.md at `path`.

    Returns (ok, problems). ok is True iff problems is empty.
    """
    path = Path(path)
    if not path.is_file():
        return False, [f"ARCHITECTURE.md does not exist: {path}"]
    text = path.read_text(encoding="utf-8")
    problems = _check_top_matter(text) + _check_ratified_by(text, draft) + _check_rules(text, path.resolve().parent)
    return (not problems), problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a repository's ARCHITECTURE.md against the "
                    "architecture tool's authoring contract.")
    parser.add_argument("architecture_md", help="path to ARCHITECTURE.md")
    parser.add_argument("--draft", action="store_true",
                        help="accept a file with no 'ratified-by:' line yet")
    args = parser.parse_args(argv)

    ok, problems = validate(Path(args.architecture_md), draft=args.draft)
    if ok:
        print(f"OK: {args.architecture_md} conforms to the ARCHITECTURE.md contract.")
        return 0
    print(f"INVALID: {args.architecture_md} does not conform to the "
          f"ARCHITECTURE.md contract.", file=sys.stderr)
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
