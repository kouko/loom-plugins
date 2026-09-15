"""Adversarial probes for `2026-09-15-closing-review-station-name`.

The change rewords "the review station" to "the closing-review station" in
eight skill, reference and agent-contract files. These probes try to make
that change fail: a legacy name that survives a line wrap or emphasis, a
capitalised "Review" used as the station noun, a reworded sentence whose
meaning drifted beyond the station name, an internal id that a sweep
over-replaced, runtime strings agents read that still carry the old name,
and a pinned-prose test that cannot tell the old wording from the new.

Probes that are expected to hold pass; probes that land a finding fail on
purpose and name the finding in their assertion message. Everything runs
read-only against committed content; the branch base is pinned by commit id
so the probes re-run in a clean clone.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "loom-code").is_dir() and (candidate / "loom-design").is_dir():
            return candidate
    raise RuntimeError(f"could not locate repo root above {start}")


REPO = _find_repo_root(Path(__file__).parent)
BASE = "8a27d66854833c21dfaf59b3bd35c4708064b604"

CHANGED = [
    "loom-code/skills/write-plan/SKILL.md",
    "loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md",
    "loom-code/agents/blind-runner.md",
    "loom-code/agents/reviewer.md",
    "loom-design/skills/write-spec/SKILL.md",
    "loom-design/skills/write-spec/references/spec-forms.md",
    "loom-design/skills/write-spec/references/ui-flows.md",
    "loom-design/skills/design-system/references/knowledge-triage.md",
]

# "review station" as the station name, tolerant of wraps, backticks and
# bold, but not when it is the tail of "closing-review".
LEGACY = re.compile(r"(?<![-\w*`])(\*\*)?`?review`?(\*\*)?\s+station", re.IGNORECASE)

# Capitalised "Review" used as a proper station noun (the way "Build" is).
PROPER_REVIEW = re.compile(
    r"\b(?:after|until|before|to|when|by)\s+Review\b(?![- ]?(?:record|verdict|finding|lens))"
    r"|\bReview\s+(?:generates|decides|hands|runs|dispatches)\b"
)


def _norm(text: str) -> str:
    return " ".join(text.split())


def _prose_files() -> list[Path]:
    roots = ["loom-code/skills", "loom-code/agents", "loom-design/skills", "loom-design/agents"]
    out: list[Path] = []
    for root in roots:
        base = REPO / root
        if base.is_dir():
            out.extend(sorted(base.rglob("*.md")))
    return out


def _git_show(rev: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), "show", f"{rev}:{path}"],
        check=True, capture_output=True, text=True,
    ).stdout


def test_legacyregex_syntheticsamples_classifiescorrectly() -> None:
    """The legacy-name matcher flags wrapped, bold and backticked forms and spares closing-review."""
    assert LEGACY.search("hand it to the review\nstation")
    assert LEGACY.search("hand the spec to the **review** station")
    assert LEGACY.search("a `review` station")
    assert not LEGACY.search("the closing-review station reads it")
    assert not LEGACY.search("the **closing-review**\nstation reads it")


def test_stationprose_wrapaware_nolegacyname() -> None:
    """No skill, reference or agent contract in either plugin names the review station after wrap normalisation."""
    hits = []
    for path in _prose_files():
        text = _norm(path.read_text(encoding="utf-8"))
        for m in LEGACY.finditer(text):
            hits.append(f"{path.relative_to(REPO)}: ...{text[max(0, m.start() - 50):m.end() + 10]}...")
    assert not hits, "legacy station name survives:\n" + "\n".join(hits)


def test_stationprose_capitalizedreview_noproperstationnoun() -> None:
    """No skill or agent contract uses a capitalised "Review" as the station's proper name."""
    hits = []
    for path in _prose_files():
        text = _norm(path.read_text(encoding="utf-8"))
        for m in PROPER_REVIEW.finditer(text):
            hits.append(f"{path.relative_to(REPO)}: ...{text[max(0, m.start() - 40):m.end() + 30]}...")
    assert not hits, (
        "FINDING: capitalised 'Review' still names the station (the renamed id is closing-review):\n"
        + "\n".join(hits)
    )


@pytest.mark.parametrize("path", CHANGED)
def test_changeddiff_stationnameonly_meaningunchanged(path: str) -> None:
    """Undoing only the station-name substitution restores the base text exactly, modulo whitespace."""
    head = _norm((REPO / path).read_text(encoding="utf-8"))
    base = _norm(_git_show(BASE, path))
    reverted = head.replace("**closing-review** station", "**review** station")
    reverted = reverted.replace("closing-review station", "review station")
    reverted = reverted.replace("The closing-review station", "The review station")
    # W2-01: a capitalised "Review" that named the station became closing-review
    reverted = reverted.replace("`closing-review`", "Review")
    reverted = reverted.replace("return to closing-review", "return to Review")
    reverted = _undo_description_station(reverted)
    # sentence-initial capital in the base
    assert reverted.lower() == base.lower(), f"{path}: reworded text differs beyond the station name"
    assert reverted == base or _case_only_initial(reverted, base), f"{path}: casing drift beyond sentence start"


def _undo_description_station(text: str) -> str:
    """Map a plain closing-review station noun in a skill description back to Review."""
    m = re.search(r"description: (.*?) (?:version:|---)", text)
    if not m:
        return text
    desc = re.sub(r"(?<![\w:-])closing-review(?![\w-])", "Review", m.group(1))
    return text[:m.start(1)] + desc + text[m.end(1):]


def _case_only_initial(a: str, b: str) -> bool:
    diffs = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return all(a[i].lower() == b[i].lower() and (i == 0 or a[i - 1] in " *`(") for i in diffs)


@pytest.mark.parametrize("path", CHANGED)
def test_gatemarkers_afterrename_unchanged(path: str) -> None:
    """Gate markers and backticked review-bearing ids are identical before and after the rename."""
    marker = re.compile(r"<!--\s*gate:[^>]*-->")
    ident = re.compile(r"`[\w.:/+-]*review[\w.:/+-]*`", re.IGNORECASE)
    head = (REPO / path).read_text(encoding="utf-8")
    base = _git_show(BASE, path)
    assert marker.findall(head) == marker.findall(base)
    head_ids = [i for i in ident.findall(head) if i != "`closing-review`"]
    base_ids = [i for i in ident.findall(base) if i != "`closing-review`"]
    assert sorted(head_ids) == sorted(base_ids)


def test_overreplace_internalids_absent() -> None:
    """A sweep did not mangle internal ids such as finalize-review or review.bounded-episode."""
    mangled = re.compile(
        r"closing-closing-review|finalize-closing-review|closing-review\.bounded-episode"
        r"|closing-review-station|closing-reviewer|closing-review-order"
    )
    hits = [
        str(p.relative_to(REPO)) for p in _prose_files()
        if mangled.search(p.read_text(encoding="utf-8"))
    ]
    assert not hits, f"over-replaced ids in: {hits}"


def test_checkerwarn_standingmessage_nolegacyname() -> None:
    """The checker's standing-docs WARN, which agents read at runtime, does not name the review station."""
    text = _norm((REPO / "loom-code/scripts/loom_checker/rule_checks/standing.py").read_text(encoding="utf-8"))
    m = LEGACY.search(text)
    assert m is None, (
        "FINDING: loom_checker standing WARN still prints 'the review station' to agents: ..."
        + text[max(0, m.start() - 40):m.end() + 40]
    )


def test_codexmanifest_longdescription_nolegacyname() -> None:
    """The loom-design Codex manifest description, shown to agents choosing a plugin, does not name the review station."""
    data = json.loads((REPO / "loom-design/.codex-plugin/plugin.json").read_text(encoding="utf-8"))
    blob = _norm(json.dumps(data, ensure_ascii=False))
    m = LEGACY.search(blob)
    assert m is None, (
        "FINDING: loom-design/.codex-plugin/plugin.json still says: ..."
        + blob[max(0, m.start() - 40):m.end() + 40]
    )


def test_installlayoutpin_legacysentence_rejected() -> None:
    """The install-layout test pin for write-plan's hand-off sentence rejects the pre-rename wording."""
    pin_src = (REPO / "scripts/test_loom_plugin_install_layout.py").read_text(encoding="utf-8")
    m = re.search(r'assert "([^"]*review station once at branch end[^"]*)" in', pin_src)
    assert m, "pin literal not found; probe needs updating"
    literal = m.group(1)
    old = _norm(_git_show(BASE, "loom-code/skills/write-plan/SKILL.md"))
    assert literal not in old, (
        f"FINDING: pinned literal {literal!r} also matches the pre-rename sentence, "
        "so the pin cannot detect a revert to 'the review station'"
    )
