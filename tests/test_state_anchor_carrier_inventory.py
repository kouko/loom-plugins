"""Drift guard: the "state anchor" wording's carrier inventory across loom-*/.

Source: docs/loom/specs/2026-08-07-loom-mechanical-dedup-arc1.md (B1) +
docs/loom/plans/2026-08-07-loom-mechanical-dedup-arc1.md (Task 1). Deep recon
found "state anchor" / "state-anchor" is NOT one hand-copied text — it is a
deliberate paraphrase repeated at different compression levels across the
loom family (asking-the-user discipline). None of the locations are
byte-identical, so a byte-SSOT would rewrite rendered prose; instead this
test pins the CARRIER LIST (which files mention it, how many times) so a
semantic change to the phrase gets a machine-readable sweep list instead of
a silent, ungrepped drift.

Population: `grep -rnE 'state anchor|state-anchor' loom-*/`, excluding
loom-code/CHANGELOG.md (changelog prose, not a live carrier) and
loom-code/hooks/test-prompts.json and compaction-oracle files (test fixtures,
not live carriers).
Re-derived directly against the working tree at pin time — NOT copied from
the brief's recon list. The brief's recon figure (10 files / 11 hits) was
simply miscounted against main; verified against branch base d1e50685 the
count was already 9 files / 12 hits. After the five-station rewrite deleted every loom-code carrier (routers,
brainstorming, requesting-code-review, subagent-driven-development and the
ask-triage hook), the live measurement is 4 files / 5 hits, all in
loom-design and loom-workflow.

Granularity is file -> hit-count, not file:line — per the plan's Kickoff
decision, line numbers churn on unrelated edits; a count change in any file
is the drift signal that matters.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from repo_files import repository_files  # noqa: E402

PATTERN = re.compile(r"state anchor|state-anchor")

EXCLUDED_RELATIVE_PATHS = frozenset(
    {
        "loom-code/CHANGELOG.md",
    }
)

# The pinned carrier inventory (file -> hit count). Any addition, removal, or
# count change to a "state anchor" / "state-anchor" mention anywhere under
# loom-*/ must update this map in the same PR.
# Three of the four carriers were loom-design's entry router, its relay
# references and the test that guarded them; loom 1.0 deleted all three, so
# the phrase now lives in one place. The pin is a sweep list, not a budget:
# one carrier is a legitimate state for it, and the guard below still fails
# loud if a fifth appears or this one goes quiet.
EXPECTED_INVENTORY = {
    "loom-workflow/skills/handoff/references/handoff-schema.md": 1,
}


def scan_state_anchor_carriers(root: Path) -> dict[str, int]:
    """Grep `state anchor|state-anchor` over root/loom-*/, count hits per file.

    Mirrors `grep -rnE 'state anchor|state-anchor' loom-*/` with
    EXCLUDED_RELATIVE_PATHS removed. Returns {posix relative path: hit count}
    for every file with >=1 hit; files with zero hits are absent from the
    map (matching how the file->hit-count pin is authored).

    The population is the repository's own files under those `loom-*`
    directories, per `repo_files.repository_files` — an ignored directory and a
    linked worktree checked out inside the tree carry no live carrier, exactly
    as `grep` with a `.gitignore`-aware tool would report.
    """
    counts: dict[str, int] = {}
    for path in sorted(repository_files(root)):
        relative = path.relative_to(root)
        if len(relative.parts) < 2 or not relative.parts[0].startswith("loom-"):
            continue
        rel = relative.as_posix()
        if rel in EXCLUDED_RELATIVE_PATHS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits = len(PATTERN.findall(text))
        if hits:
            counts[rel] = hits
    return counts


def format_mismatch(expected: dict[str, int], actual: dict[str, int]) -> str:
    """Full expected-vs-actual carrier list — the sweep list for a real
    semantic change to "state anchor" wording (Task 1 GREEN acceptance)."""
    lines = ["state-anchor carrier inventory mismatch (expected vs actual):"]
    for rel in sorted(set(expected) | set(actual)):
        exp = expected.get(rel, 0)
        act = actual.get(rel, 0)
        flag = "  " if exp == act else "!="
        lines.append(f"  {flag} {rel}: expected={exp} actual={act}")
    return "\n".join(lines)


def test_state_anchor_carrier_inventory_matches_pin():
    actual = scan_state_anchor_carriers(REPO_ROOT)
    assert actual == EXPECTED_INVENTORY, format_mismatch(EXPECTED_INVENTORY, actual)


def test_scan_state_anchor_carriers_catches_a_removed_carrier(tmp_path):
    """Proves the checker is load-bearing, not vacuous.

    The real tree currently matches EXPECTED_INVENTORY exactly, so the test
    above alone would stay green even if scan_state_anchor_carriers were
    broken (e.g. always returning the pin unchanged). This test extracts the
    pinned carrier files' REAL content into an isolated tmp_path copy (zero
    mutation residue in the real tree — house RED-on-extracted-copy pattern),
    removes one carrier phrase, and shows the scan actually detects it.
    """
    for rel in EXPECTED_INVENTORY:
        src = REPO_ROOT / rel
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    baseline = scan_state_anchor_carriers(tmp_path)
    assert baseline == EXPECTED_INVENTORY

    mutated_rel = "loom-workflow/skills/handoff/references/handoff-schema.md"
    mutated_path = tmp_path / mutated_rel
    text = mutated_path.read_text(encoding="utf-8")
    assert "state anchor" in text or "state-anchor" in text
    mutated_path.write_text(
        text.replace("state anchor", "situational context", 1).replace(
            "state-anchor", "situational-context", 1
        ),
        encoding="utf-8",
    )

    actual = scan_state_anchor_carriers(tmp_path)
    assert actual != EXPECTED_INVENTORY
    assert mutated_rel not in actual  # the carrier's only hit was removed


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_gitignored_dir_not_counted(tmp_path):
    """A directory `.gitignore` excludes holds no carrier: its copy of the
    phrase is build output, not a live mention to sweep."""
    repo = tmp_path / "repo"
    (repo / "loom-workflow" / "build").mkdir(parents=True)
    (repo / ".gitignore").write_text("loom-workflow/build/\n", encoding="utf-8")
    (repo / "loom-workflow" / "live.md").write_text(
        "the state anchor discipline\n", encoding="utf-8"
    )
    (repo / "loom-workflow" / "build" / "generated.md").write_text(
        "the state anchor discipline\n", encoding="utf-8"
    )
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")

    assert scan_state_anchor_carriers(repo) == {"loom-workflow/live.md": 1}
