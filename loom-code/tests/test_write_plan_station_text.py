"""W2-01 -- write-plan's station text cites the plan
row of the artifact charter (`contract/manifest.yaml`, `artifacts.plan.charter`)
instead of restating its caps or its edits-after policy list.
"""

from __future__ import annotations

# Version sync constant - updated only on releases
CURRENT_VERSION = "3.39.0"

# One literal is load-bearing and pinned here: the SKILL.md sentence naming
# `artifacts.plan.charter`.

import json
import re
from pathlib import Path

import pytest

from prose_pin import NEGATION_RE

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / "loom-code" / "skills" / "write-plan" / "SKILL.md"
SECOND_VENDOR_REFERENCE = (
    REPO
    / "loom-code"
    / "skills"
    / "write-plan"
    / "references"
    / "second-vendor-ask-and-docs-lint.md"
)


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"section {heading!r} missing"
    return match.group(0)


def test_decision_boundary_owns_implementation_not_product_behaviour() -> None:
    section = _section(SKILL.read_text(encoding="utf-8"), "## Decision boundary")
    assert len(section.split()) <= 90


def _has_negation(sentence: str) -> bool:
    return bool(NEGATION_RE.search(sentence))


def _flat_sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [p for p in re.split(r"(?<=[.!?])\s+", flat) if p.strip()]


def test_skill_names_the_plan_charter_row() -> None:
    text = SKILL.read_text(encoding="utf-8")
    hits = [
        s for s in _flat_sentences(text)
        if "artifacts.plan.charter" in s and not _has_negation(s)
    ]
    assert hits, (
        "SKILL.md has no affirmative sentence naming artifacts.plan.charter "
        "-- the task fields' content kinds and caps must cite the charter "
        "row instead of restating it"
    )


# --- W1-02 -- suggest is visible after risk evidence, without becoming a
# fourth decision point ----------------------------------------------------


LANE_WORDING_RE = re.compile(r"(?i)\b(small|full)[- ]lanes?\b|\blanes?\b")


def test_second_vendor_reference_drops_second_reader_wording() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    assert "第二位讀者" not in text
    assert "second reader" not in text.lower()


RUNTIME_DIRS = ("skills", "agents", "contract", "hooks", "commands", "scripts", "references")
RUNTIME_SUFFIXES = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".toml", ".ini", ""}
DATED_NAME_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def runtime_files() -> list[Path]:
    """Every runtime file of loom-code and loom-design, walked from disk so the
    scan also runs in a `git archive` copy. Excluded: tests (they assert the
    absence), CHANGELOGs and dated records."""
    files = []
    for plugin in ("loom-code", "loom-design"):
        for sub in RUNTIME_DIRS:
            for path in sorted((REPO / plugin / sub).rglob("*")):
                if (
                    path.is_file()
                    and path.suffix in RUNTIME_SUFFIXES
                    and not {"__pycache__", ".pytest_cache"} & set(path.parts)
                    and not re.fullmatch(r"test_.*\.py", path.name)
                    and not path.name.upper().startswith("CHANGELOG")
                    and not DATED_NAME_RE.search(path.name)
                ):
                    files.append(path)
    return files


def lane_hits(text: str) -> list[str]:
    return [m.group(0) for m in LANE_WORDING_RE.finditer(" ".join(text.split()))]


def test_laneHits_syntheticText_matchesOnlyLaneWords() -> None:
    assert lane_hits("ask blocks once per full-lane change")
    assert lane_hits("In the small\n lane it is omitted")
    assert not lane_hits("planes and a planet on the plane explained")


def test_runtime_tree_names_no_lane() -> None:
    """A2 positive (runtime-tree-lane-scan): no runtime file in either plugin
    names a lane; the only lane guard, so it is not repeated per file."""
    files = runtime_files()
    assert len(files) > 50, "scan scope collapsed"
    assert REPO / "loom-code" / "hooks" / "session-start" in files
    assert REPO / "loom-code" / "references" / "dispatch-profile.md" in files
    offenders = {
        str(path.relative_to(REPO)): hits
        for path in files
        if (hits := lane_hits(path.read_text(encoding="utf-8", errors="replace")))
    }
    assert offenders == {}


def _policy_accepted_fields() -> set[str]:
    """The `allowed` set literal inside second_vendor_policy.resolve, read by
    AST so the pin follows the script rather than a copied list."""
    import ast

    tree = ast.parse(
        (REPO / "loom-code" / "scripts" / "second_vendor_policy.py").read_text(encoding="utf-8")
    )
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "allowed" for t in node.targets)
            and isinstance(node.value, ast.Set)
        ):
            return {elt.value for elt in node.value.elts}
    raise AssertionError("allowed set not found in second_vendor_policy.py")


def test_suggest_station_names_every_policy_input_key() -> None:
    section = _section(
        SKILL.read_text(encoding="utf-8"), "### Resolve `second-vendor: suggest`"
    )
    named = set(re.findall(r"`([a-z_]+)`", section))
    assert _policy_accepted_fields() <= named


def test_reference_has_no_none_mode_or_per_change_none_answer() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    assert "second-vendor: <cli> | none" not in text
    assert "`<cli>` / `none`" not in text


# --- typed-branch-names W1-02 -- the branch is `<type>/<change-id>` -------


def test_write_plan_names_typed_branch_and_types() -> None:
    section = _section(
        SKILL.read_text(encoding="utf-8"), "## Step 6 — Commit and hand off"
    )
    # The type list in Step 6 matches implementer.md: every sentence listing
    # branch types lists exactly the implementer's set.
    types = {"feat", "fix", "docs", "refactor", "test", "chore", "ci"}
    listed = [set(re.findall(r"`([a-z]+)`", s)) for s in _flat_sentences(section)]
    listed = [found for found in listed if len(found & types) >= 3]
    assert listed and all(found == types for found in listed), listed


# Split literals so a repo grep for the bare form never matches this file.
_BARE_BRANCH_RE = re.compile(
    r"(?:switch (?:-c|--create)|checkout -[bB]|git branch|worktree add -b"
    r"|branch named)\s+[`'\"]?" + "<change" + r"-id>"
)

_CID = "<change" + "-id>"


@pytest.mark.parametrize(
    "line",
    [
        f"git switch -c {_CID}",
        f"git switch --create {_CID}",
        f"git switch -c `{_CID}`",
        f"git switch -c '{_CID}'",
        f'git switch -c "{_CID}"',
        f"git checkout -b {_CID}",
        f"git checkout -B {_CID}",
        f"git branch {_CID}",
        f"git worktree add -b {_CID} ../wt",
        f"create a branch named `{_CID}`",
    ],
)
def test_bare_branch_re_catches_spelling(line: str) -> None:
    assert _BARE_BRANCH_RE.search(line), line


@pytest.mark.parametrize(
    "line",
    [
        f"git switch -c <type>/{_CID}",
        f"git switch --create `<type>/{_CID}`",
        f"git checkout -B <type>/{_CID}",
        f"git worktree add -b <type>/{_CID} ../wt",
        f"create a branch named `<type>/{_CID}`",
        f"write docs/loom/{_CID}/plan.md",
        f"see `docs/loom/{_CID}/spec.md`",
    ],
)
def test_bare_branch_re_ignores_typed_and_path(line: str) -> None:
    assert not _BARE_BRANCH_RE.search(line), line


def test_write_plan_bare_switch_absent() -> None:
    section = _section(
        SKILL.read_text(encoding="utf-8"), "## Step 6 — Commit and hand off"
    )
    assert not _BARE_BRANCH_RE.search(section), _BARE_BRANCH_RE.search(section)


def test_repo_grep_no_bare_branch() -> None:
    hits = []
    for plugin in ("loom-code", "loom-design", "loom-workflow"):
        for path in sorted((REPO / plugin).rglob("*")):
            if path.suffix not in {".md", ".py", ".sh"} or not path.is_file():
                continue
            rel = path.relative_to(REPO)
            if path.name.startswith("CHANGELOG") or {
                "node_modules", "__pycache__"
            } & set(rel.parts):
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if _BARE_BRANCH_RE.search(line):
                    hits.append(f"{rel}:{n}")
    assert not hits, hits


def test_current_release_metadata_is_synchronized() -> None:
    claude_manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    codex_manifest = json.loads(
        (REPO / "loom-code/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    changelog = (REPO / "loom-code/CHANGELOG.md").read_text(encoding="utf-8")
    agy_manifest = json.loads(
        (REPO / "loom-code/plugin.json").read_text(encoding="utf-8")
    )
    package = json.loads(
        (REPO / "loom-code/package.json").read_text(encoding="utf-8")
    )
    assert claude_manifest["version"] == CURRENT_VERSION
    assert codex_manifest["version"] == CURRENT_VERSION
    assert agy_manifest["version"] == CURRENT_VERSION
    assert package["version"] == CURRENT_VERSION
    assert f"## [{CURRENT_VERSION}]" in changelog


@pytest.mark.parametrize(
    ("readme", "label"),
    [
        ("README.md", "**Version**: "),
        ("README.ja.md", "**バージョン**: "),
        ("README.zh-TW.md", "**版本**："),
    ],
)
def test_readme_version_matches_manifest(readme: str, label: str) -> None:
    manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    text = (REPO / "loom-code" / readme).read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(label)}(\d+\.\d+\.\d+)", text, re.M)
    assert match, f"{readme}: version line missing"
    assert match.group(1) == manifest["version"]


def test_root_readme_plugin_table_row_version_matches_manifest() -> None:
    """The plugin table at the top of the repository README states the
    loom-code version too. The section prose below it is already pinned; a
    stale table row would still send a reader to a version the installer will
    not hand them."""
    manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    text = (REPO / "README.md").read_text(encoding="utf-8")
    row = re.search(r"^\| \[`loom-code`\]\(loom-code/\) \| (\d+\.\d+\.\d+) \|", text, re.M)
    assert row, "README.md: loom-code plugin table row missing"
    assert row.group(1) == manifest["version"]


def test_root_readme_loom_code_section_version_matches_manifest() -> None:
    manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    section = _section((REPO / "README.md").read_text(encoding="utf-8"), "## loom-code")
    match = re.search(r"^Version (\d+\.\d+\.\d+)\.", section, re.M)
    assert match, "README.md ## loom-code: version line missing"
    assert match.group(1) == manifest["version"]
