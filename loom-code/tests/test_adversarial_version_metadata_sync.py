"""Adversarial probes for the loom-code release-metadata bump.

`test_current_release_metadata_is_synchronized` pins three manifest versions
and one changelog heading to a literal string. These probes attack the ways
that pinned test could pass while a real consumer — `claude plugin update`,
the Codex loader, or the Antigravity CLI root manifest reader — still saw an
inconsistent version.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "loom-code"
SSOT = PLUGIN / ".claude-plugin/plugin.json"


def _version(path: Path) -> str:
    return json.loads(path.read_text(encoding="utf-8"))["version"]


def _semver(text: str) -> tuple[int, int, int]:
    major, minor, patch = text.split(".")
    return int(major), int(minor), int(patch)


def test_every_manifest_under_the_plugin_agrees_with_the_ssot() -> None:
    """The pinned test names three files by hand. A fourth manifest copy added
    later would be read by a loader and ignored by that test. Enumerate instead
    of naming."""
    manifests = sorted(
        p
        for p in PLUGIN.rglob("plugin.json")
        if "node_modules" not in p.parts and "__pycache__" not in p.parts
    )
    assert len(manifests) >= 3, [str(p.relative_to(REPO)) for p in manifests]
    disagreeing = {
        str(p.relative_to(REPO)): _version(p)
        for p in manifests
        if _version(p) != _version(SSOT)
    }
    assert not disagreeing, disagreeing


def test_changelog_top_entry_is_the_shipped_version() -> None:
    """The pinned test asserts only that `## [3.7.3]` appears *somewhere*. An
    entry filed below an older one still satisfies it while a reader looking at
    the top of the changelog sees a stale version."""
    changelog = (PLUGIN / "CHANGELOG.md").read_text(encoding="utf-8")
    headings = re.findall(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.M)
    assert headings, "loom-code/CHANGELOG.md: no version headings"
    assert headings[0] == _version(SSOT)


def test_changelog_headings_descend() -> None:
    """A bump that lands below an existing entry, or a version that moves
    backwards, is a release-ordering error the pinned test cannot see.

    Scoped to the 3.x line: the pre-1.0 history carries a duplicated
    `## [0.2.1] — 2026-05-16` pair (CHANGELOG.md:7297 and :7434) that predates
    this rule and is not this change's to clean."""
    changelog = (PLUGIN / "CHANGELOG.md").read_text(encoding="utf-8")
    headings = [
        _semver(v) for v in re.findall(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.M)
    ]
    current_line = [v for v in headings if v >= (3, 0, 0)]
    out_of_order = [(a, b) for a, b in zip(current_line, current_line[1:]) if not a > b]
    assert not out_of_order, out_of_order


def test_shipped_version_is_above_the_version_it_replaces() -> None:
    """Acceptance 1 of the intent: the three manifests must read *higher* than
    3.7.2, not merely be equal to each other. Three synchronized copies of an
    unmoved string is the exact failure this change exists to fix."""
    assert _semver(_version(SSOT)) > (3, 7, 2)


def test_derived_manifests_are_not_hand_drifted() -> None:
    """`.codex-plugin/plugin.json` and the root `plugin.json` are generated from
    the Claude SSOT. A bump applied to one copy and not the others — in any
    order — is drift, and the generator's own check is what makes the ordering
    question moot."""
    proc = subprocess.run(
        [sys.executable, "scripts/sync_codex_manifests.py", "--check", "--all"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_marketplace_entry_pins_no_version() -> None:
    """The marketplace manifest is what `claude plugin install loom-code@loom`
    resolves through. If it ever gains its own version field it becomes a fourth
    cached copy; today it carries none, and that is what keeps the bump from
    needing a fifth edit."""
    marketplace = json.loads(
        (REPO / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
    )
    entry = next(p for p in marketplace["plugins"] if p["name"] == "loom-code")
    assert "version" not in entry, entry


def test_no_operative_file_still_carries_the_previous_version() -> None:
    """Changelog prose and the docs/loom record legitimately name 3.7.2. This
    probe's own source legitimately names it too, to describe and parse the
    boundary it tests. Any other tracked file still stating it is a copy the
    bump missed."""
    tracked = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split("\0")
    self_path = Path(__file__).resolve().relative_to(REPO).as_posix()
    stale: list[str] = []
    for rel in tracked:
        if not rel or rel.startswith("docs/") or rel.endswith("CHANGELOG.md") or rel == self_path:
            continue
        path = REPO / rel
        if not path.is_file() or "node_modules" in Path(rel).parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if "3.7.2" in line and path != SSOT:
                stale.append(f"{rel}:{n}: {line.strip()}")
    assert not stale, stale


@pytest.mark.parametrize(
    "readme",
    ["loom-code/README.md", "loom-code/README.ja.md", "loom-code/README.zh-TW.md",
     "README.md"],
)
def test_no_readme_states_a_loom_code_version_other_than_the_manifest(
    readme: str,
) -> None:
    """The per-README tests each match one labelled line. A second version
    string elsewhere in the same file — a quoted install example, a migration
    note — would go unseen."""
    text = (REPO / readme).read_text(encoding="utf-8")
    current = _version(SSOT)
    others = [
        f"{readme}:{n}: {line.strip()}"
        for n, line in enumerate(text.splitlines(), 1)
        for found in re.findall(r"\b3\.\d+\.\d+\b", line)
        if found != current
    ]
    assert not others, others


def test_contract_manifest_version_is_untouched_as_the_changelog_claims() -> None:
    """The 3.7.3 entry asserts the contract manifest version stays 2.3.1. Read
    the claim out of the changelog and check it against the file rather than
    trusting the sentence."""
    changelog = (PLUGIN / "CHANGELOG.md").read_text(encoding="utf-8")
    entry = changelog.split("## [3.7.2]")[0]
    claimed = re.search(r"contract manifest version stays (\d+\.\d+\.\d+)", entry)
    assert claimed, "3.7.3 entry: no contract-manifest-version claim to check"
    manifest = (PLUGIN / "contract/manifest.yaml").read_text(encoding="utf-8")
    actual = re.search(r"^version: (\d+\.\d+\.\d+)", manifest, re.M)
    assert actual, "loom-code/contract/manifest.yaml: no version line"
    assert actual.group(1) == claimed.group(1)


def test_pinned_metadata_test_pins_one_version_not_several() -> None:
    """The pinned test hand-edits four literals. A partial edit that left one
    assertion on the old string would still be a green-looking diff to a reader
    skimming it; make the file itself state a single version."""
    pinned = (
        PLUGIN / "tests/test_write_plan_station_text.py"
    ).read_text(encoding="utf-8")
    body = pinned.split("def test_current_release_metadata_is_synchronized")[1]
    body = body.split("\n@pytest.mark.parametrize")[0]
    literals = set(re.findall(r"\b\d+\.\d+\.\d+\b", body))
    assert literals == {_version(SSOT)}, literals
