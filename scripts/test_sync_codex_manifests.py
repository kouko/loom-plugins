"""Tests for sync_codex_manifests.py — the REPO-LEVEL Codex manifest sync engine.

Unlike loom-code/scripts/sync_codex_manifest.py (self-locating to its own parent
plugin), this engine is repo-level: it takes a plugin (dir name or path) as input
and syncs that plugin's `.codex-plugin/plugin.json` shared fields from its
`.claude-plugin/plugin.json` SSOT, preserving the Codex-only `interface` block.

These tests build self-contained fixture plugin dirs under tmp_path so they never
touch any committed manifest. Stdlib only (json + subprocess to exercise the CLI).
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "sync_codex_manifests.py"

SHARED_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)


def _claude_ssot() -> dict:
    return {
        "name": "demo-plugin",
        "version": "1.4.0",
        "description": "new description",
        "author": {"name": "kouko", "url": "https://github.com/kouko"},
        "homepage": "https://example.com/home",
        "repository": "https://example.com/repo",
        "license": "MIT",
        "keywords": ["a", "b", "c"],
        "skills": "./skills/",
    }


def _interface() -> dict:
    return {
        "displayName": "demo-plugin",
        "shortDescription": "short",
        "capabilities": ["Interactive", "Read", "Write"],
        "brandColor": "#2563EB",
    }


def _stale_codex() -> dict:
    return {
        "name": "demo-plugin",
        "version": "0.9.0",
        "description": "old description",
        "author": {"name": "kouko", "url": "https://github.com/kouko"},
        "homepage": "https://old.example.com",
        "repository": "https://example.com/repo",
        "license": "MIT",
        "keywords": ["a"],
        "skills": "./skills/",
        "interface": _interface(),
    }


def _build_plugin(plugin_dir: Path, claude: dict, codex: dict) -> Path:
    """Create <plugin_dir>/.claude-plugin/plugin.json + .codex-plugin/plugin.json."""
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".codex-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(claude, indent=2) + "\n", encoding="utf-8"
    )
    (plugin_dir / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(codex, indent=2) + "\n", encoding="utf-8"
    )
    return plugin_dir


def _codex_path(plugin_dir: Path) -> Path:
    return plugin_dir / ".codex-plugin" / "plugin.json"


# --- the cohesive engine unit: sync copies shared fields, preserves interface --

def test_sync_copies_shared_fields_preserving_interface(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    interface_before = json.loads(_codex_path(plugin).read_text())["interface"]

    m.sync_plugin(plugin)

    written = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
    for field in SHARED_FIELDS:
        assert written[field] == _claude_ssot()[field], f"{field} not synced from SSOT"
    # interface block byte-identical (preserved verbatim, not merged with SSOT)
    assert written["interface"] == interface_before
    assert written["interface"] == _interface()


def test_sync_accepts_plugin_dir_as_string_path(tmp_path):
    """Public surface takes a plugin dir name/path, not a hardcoded parent."""
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    m.sync_plugin(str(plugin))

    written = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
    assert written["version"] == _claude_ssot()["version"]


# --- --check is a pure read; in-sync exits 0, divergence exits non-zero --------

def _run(argv, plugin_dir: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *argv, str(plugin_dir)],
        capture_output=True,
        text=True,
    )


def test_check_exits_zero_when_synced(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    m.sync_plugin(plugin)  # bring into sync first

    before = _codex_path(plugin).read_text(encoding="utf-8")
    proc = _run(["--check"], plugin)
    assert proc.returncode == 0, proc.stderr
    # --check must not mutate
    assert _codex_path(plugin).read_text(encoding="utf-8") == before


def test_check_exits_nonzero_after_mutating_one_shared_field(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    m.sync_plugin(plugin)

    # mutate exactly one shared field on the Codex manifest -> divergence
    codex = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
    codex["version"] = "9.9.9"
    _codex_path(plugin).write_text(json.dumps(codex, indent=2) + "\n", encoding="utf-8")

    proc = _run(["--check"], plugin)
    assert proc.returncode != 0, "divergent shared field must fail --check"


def test_sync_plugin_check_mode_returns_bool_without_mutating(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    before = _codex_path(plugin).read_text(encoding="utf-8")

    in_sync = m.sync_plugin(plugin, check=True)
    assert in_sync is False  # stale codex diverges
    assert _codex_path(plugin).read_text(encoding="utf-8") == before  # no mutation


def test_cli_sync_then_check_is_clean(tmp_path):
    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())

    assert _run([], plugin).returncode == 0
    assert _run(["--check"], plugin).returncode == 0


# --- --scaffold seeds a missing Codex manifest with mechanical + TODO fields ---

def _build_claude_only(plugin_dir: Path, claude: dict) -> Path:
    """Create only <plugin_dir>/.claude-plugin/plugin.json (no Codex manifest)."""
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(claude, indent=2) + "\n", encoding="utf-8"
    )
    return plugin_dir


def test_scaffold_seeds_mechanical_fields_and_todo_placeholders(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_claude_only(tmp_path / "demo-plugin", _claude_ssot())
    assert not _codex_path(plugin).exists()

    m.scaffold_plugin(plugin)

    written = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
    # shared fields seeded from the Claude SSOT
    for field in SHARED_FIELDS:
        assert written[field] == _claude_ssot()[field], f"{field} not seeded from SSOT"

    iface = written["interface"]
    # mechanically-derivable fields come from the Claude manifest
    assert iface["displayName"] == "demo-plugin"  # == name
    assert iface["developerName"] == "kouko"  # == author.name
    # websiteURL == repository + "/tree/main/" + name (canonical GitHub subdir form)
    assert iface["websiteURL"] == "https://example.com/repo/tree/main/demo-plugin"
    # judgment fields are literal "TODO" placeholders for Phase 2 to fill
    for todo in ("longDescription", "category", "capabilities", "defaultPrompt", "brandColor"):
        assert iface[todo] == "TODO", f"{todo} must be a TODO placeholder"


def test_website_url_falls_back_to_homepage_when_no_repository(tmp_path):
    """A plugin with `homepage` but NO `repository` must get a real URL.

    The Claude SSOT's `homepage` is the canonical GitHub tree URL; when
    `repository` is absent the websiteURL fallback must use it, not degrade to
    the bare plugin name (which is not a URL).
    """
    import sync_codex_manifests as m

    claude = _claude_ssot()
    del claude["repository"]
    claude["homepage"] = "https://github.com/kouko/monkey-skills/tree/main/demo-plugin"

    plugin = _build_claude_only(tmp_path / "demo-plugin", claude)
    m.scaffold_plugin(plugin)

    iface = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))["interface"]
    assert iface["websiteURL"] == claude["homepage"]
    assert iface["websiteURL"] != "demo-plugin"  # must not degrade to bare name


def test_check_all_reports_missing_manifest_cleanly(tmp_path):
    """`--all --check` on an eligible plugin with no Codex manifest must fail
    with a clean MISSING message, not a raw FileNotFoundError traceback."""
    dirs = _build_all_eligible(tmp_path)
    assert _run_all([], tmp_path).returncode == 0  # bring all into sync first

    # remove one eligible plugin's Codex manifest entirely
    _codex_path(dirs["loom-code"]).unlink()

    proc = _run_all(["--check"], tmp_path)
    assert proc.returncode != 0, "missing manifest must fail --all --check"
    assert "MISSING" in proc.stderr, proc.stderr
    assert "Traceback" not in proc.stderr, "must be a clean message, not a traceback"


def test_scaffold_does_not_clobber_existing_codex(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    iface_before = json.loads(_codex_path(plugin).read_text())["interface"]

    created = m.scaffold_plugin(plugin)
    assert created is False  # already exists -> not created

    after = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
    # human-authored interface preserved verbatim (not overwritten with TODOs)
    assert after["interface"] == iface_before
    # but shared fields are still brought into sync from the SSOT
    assert after["version"] == _claude_ssot()["version"]


# --- CODEX_ELIGIBLE: every repo plugin, derived from the filesystem ----------
# Why derived, not a hardcoded count: PR #523 shipped with a red loom-code CI
# because adding a plugin bumped the census past a hand-written "25" that no
# per-plugin suite runs. Deriving the expected set from the repo keeps the
# forgot-the-tuple gate (fails naming the plugin) with zero count maintenance.

# Every plugin that ships a .claude-plugin manifest also ships (and syncs) a
# .codex-plugin manifest — including loom-pipeline, whose skills are N/A at
# Codex RUNTIME (no Workflow primitive) but whose manifest still exists and
# must not drift. Manifest-sync eligibility ≠ runtime availability.
def _repo_plugin_dirs() -> set:
    """Every top-level dir that ships a Claude plugin manifest."""
    root = Path(__file__).resolve().parent.parent
    return {p.parent.parent.name
            for p in root.glob("*/.claude-plugin/plugin.json")}


def test_eligible_list_covers_every_repo_plugin():
    import sync_codex_manifests as m

    expected = _repo_plugin_dirs()
    assert expected, "filesystem scan found no plugins — glob broken?"

    eligible = set(m.CODEX_ELIGIBLE)
    missing = expected - eligible
    stale = eligible - expected
    assert not missing, (
        f"plugins on disk but absent from CODEX_ELIGIBLE (add them to the "
        f"tuple in sync_codex_manifests.py): {sorted(missing)}")
    assert not stale, (
        f"CODEX_ELIGIBLE names plugins that no longer exist on disk "
        f"(remove them): {sorted(stale)}")


# --- CLI: --scaffold creates a manifest; --all iterates; --all --check read-only

def test_cli_scaffold_creates_manifest(tmp_path):
    """`--scaffold <plugin>` over a claude-only dir creates the Codex manifest."""
    plugin = _build_claude_only(tmp_path / "demo-plugin", _claude_ssot())
    assert not _codex_path(plugin).exists()

    proc = _run(["--scaffold"], plugin)
    assert proc.returncode == 0, proc.stderr
    assert _codex_path(plugin).exists()
    written = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
    assert written["interface"]["displayName"] == "demo-plugin"


def _build_all_eligible(repo_root: Path) -> dict:
    """Build every CODEX_ELIGIBLE plugin under ``repo_root`` (stale Codex copy)."""
    import sync_codex_manifests as m

    dirs = {}
    for name in m.CODEX_ELIGIBLE:
        claude = _claude_ssot()
        claude["name"] = name
        dirs[name] = _build_plugin(repo_root / name, claude, _stale_codex())
    _write_card(dirs["loom-workflow"])
    return dirs


CARD_REL = ("skills", "loom-visualization", "assets", "trigger-card.md")
CARD_TEXT = "# Visualization trigger card (fixture)\nInvoke `loom-visualization` FIRST.\n"


def _write_card(plugin_dir: Path, text: str = CARD_TEXT) -> Path:
    card = plugin_dir.joinpath(*CARD_REL)
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text(text, encoding="utf-8")
    return card


def _run_all(argv, repo_root: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--all", *argv, "--repo-root", str(repo_root)],
        capture_output=True,
        text=True,
    )


def test_cli_all_iterates_and_syncs(tmp_path):
    """`--all` walks every eligible plugin under --repo-root and syncs each."""
    dirs = _build_all_eligible(tmp_path)

    proc = _run_all([], tmp_path)
    assert proc.returncode == 0, proc.stderr
    for name, plugin in dirs.items():
        written = json.loads(_codex_path(plugin).read_text(encoding="utf-8"))
        assert written["version"] == _claude_ssot()["version"], f"{name} not synced"


def test_cli_all_check_is_read_only_and_fails_on_drift(tmp_path):
    """`--all --check` is a pure read: exits non-zero on drift, mutates nothing."""
    dirs = _build_all_eligible(tmp_path)
    assert _run_all([], tmp_path).returncode == 0  # bring all into sync first

    # drift exactly one plugin's Codex shared field
    victim = dirs["loom-code"]
    codex = json.loads(_codex_path(victim).read_text(encoding="utf-8"))
    codex["version"] = "9.9.9"
    _codex_path(victim).write_text(
        json.dumps(codex, indent=2) + "\n", encoding="utf-8"
    )

    before = {n: _codex_path(p).read_text(encoding="utf-8") for n, p in dirs.items()}
    proc = _run_all(["--check"], tmp_path)
    after = {n: _codex_path(p).read_text(encoding="utf-8") for n, p in dirs.items()}

    assert proc.returncode != 0, "drift in one plugin must fail --all --check"
    assert "DRIFT" in proc.stderr, proc.stderr
    assert after == before, "--all --check must be pure read (no mutation)"


# --- repo-level regression guard: the REAL committed manifests must be in sync --
# Third drift-defense layer, independent of the git hook (shift-left) and the CI
# gate. Runs against the actual committed manifests (not a tmp fixture) so the
# pytest suite alone catches any plugin whose .codex-plugin/plugin.json has
# drifted from its .claude-plugin/plugin.json SSOT.

REPO_ROOT = SCRIPT.resolve().parent.parent


def test_all_eligible_codex_manifests_in_sync():
    import sync_codex_manifests as m

    # Sanity: the tuple mirrors the on-disk plugin census
    # (see test_eligible_list_covers_every_repo_plugin).
    assert set(m.CODEX_ELIGIBLE) == _repo_plugin_dirs()

    # Fold MISSING (no .codex-plugin manifest yet) into the offender list so a
    # future eligible plugin added before it is scaffolded fails CLEANLY (named),
    # not with a raw FileNotFoundError from sync_plugin's _load.
    offenders = []
    for name in m.CODEX_ELIGIBLE:
        plugin_dir = REPO_ROOT / name
        if not m.codex_manifest_path(plugin_dir).exists():
            offenders.append(f"{name} (MISSING .codex-plugin/plugin.json)")
        elif not m.sync_plugin(plugin_dir, check=True):
            offenders.append(name)
    assert not offenders, (
        "committed Codex manifests drifted or missing vs their Claude SSOT: "
        f"{offenders}. Run: python3 scripts/sync_codex_manifests.py --scaffold --all"
    )


# --- Antigravity CLI (agy) root manifest: <plugin>/plugin.json ----------------
# agy reads only a root plugin.json (Claude Code and Codex ignore it). It is
# fully derived from the Claude SSOT — no hand-authored keys — so any byte of
# difference from the derived form is drift.

AGY_FIELDS = ("name", "version", "description")


def _agy_path(plugin_dir: Path) -> Path:
    return plugin_dir / "plugin.json"


def test_root_manifest_generated_and_validates(tmp_path):
    """A1 positive: sync writes a minimal, deterministic root manifest."""
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    assert not _agy_path(plugin).exists()

    m.sync_agy_manifest(plugin)

    expected = {field: _claude_ssot()[field] for field in AGY_FIELDS}
    text = _agy_path(plugin).read_text(encoding="utf-8")
    assert json.loads(text) == expected
    assert list(json.loads(text)) == list(AGY_FIELDS)  # stable key order
    assert text == json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
    assert m.sync_agy_manifest(plugin, check=True) is True


def test_cli_sync_writes_root_manifest(tmp_path):
    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())

    assert _run([], plugin).returncode == 0
    assert json.loads(_agy_path(plugin).read_text(encoding="utf-8"))["name"] == "demo-plugin"


def test_drifted_root_manifest_fails_check(tmp_path):
    """A1 negative: a hand-edited root manifest fails --check, read-only."""
    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    assert _run([], plugin).returncode == 0

    drifted = json.loads(_agy_path(plugin).read_text(encoding="utf-8"))
    drifted["description"] = "hand-edited"
    _agy_path(plugin).write_text(json.dumps(drifted, indent=2) + "\n", encoding="utf-8")
    before = _agy_path(plugin).read_text(encoding="utf-8")

    proc = _run(["--check"], plugin)
    assert proc.returncode != 0
    assert "DRIFT" in proc.stderr and "plugin.json" in proc.stderr, proc.stderr
    assert _agy_path(plugin).read_text(encoding="utf-8") == before


def test_root_manifest_extra_key_is_drift(tmp_path):
    import sync_codex_manifests as m

    plugin = _build_plugin(tmp_path / "demo-plugin", _claude_ssot(), _stale_codex())
    m.sync_agy_manifest(plugin)
    extra = json.loads(_agy_path(plugin).read_text(encoding="utf-8"))
    extra["skills"] = "./skills/"
    _agy_path(plugin).write_text(json.dumps(extra, indent=2) + "\n", encoding="utf-8")

    assert m.sync_agy_manifest(plugin, check=True) is False


def test_all_check_fails_on_drifted_or_missing_root_manifest(tmp_path):
    dirs = _build_all_eligible(tmp_path)
    assert _run_all([], tmp_path).returncode == 0
    assert _run_all(["--check"], tmp_path).returncode == 0

    _agy_path(dirs["loom-design"]).write_text('{"name": "loom-design"}\n', encoding="utf-8")
    drift = _run_all(["--check"], tmp_path)
    assert drift.returncode != 0 and "DRIFT" in drift.stderr, drift.stderr

    _agy_path(dirs["loom-design"]).unlink()
    missing = _run_all(["--check"], tmp_path)
    assert missing.returncode != 0 and "MISSING" in missing.stderr, missing.stderr
    assert "Traceback" not in missing.stderr


def test_codex_manifests_unchanged_by_root_manifest_sync(tmp_path):
    """A8 positive: generating the agy manifest never touches host manifests."""
    import sync_codex_manifests as m

    for name in m.CODEX_ELIGIBLE:
        copy = tmp_path / name
        for host in (".claude-plugin", ".codex-plugin"):
            (copy / host).mkdir(parents=True)
            (copy / host / "plugin.json").write_bytes(
                (REPO_ROOT / name / host / "plugin.json").read_bytes()
            )
        before = {h: (copy / h / "plugin.json").read_bytes()
                  for h in (".claude-plugin", ".codex-plugin")}

        m.sync_agy_manifest(copy)

        after = {h: (copy / h / "plugin.json").read_bytes()
                 for h in (".claude-plugin", ".codex-plugin")}
        assert after == before, f"{name}: host manifests mutated"
        assert m.sync_plugin(copy, check=True), f"{name}: codex drift"


def test_all_eligible_agy_root_manifests_in_sync():
    import sync_codex_manifests as m

    offenders = []
    for name in m.CODEX_ELIGIBLE:
        plugin_dir = REPO_ROOT / name
        if not m.agy_manifest_path(plugin_dir).exists():
            offenders.append(f"{name} (MISSING plugin.json)")
        elif not m.sync_agy_manifest(plugin_dir, check=True):
            offenders.append(name)
    assert not offenders, (
        f"committed agy root manifests drifted or missing: {offenders}. "
        "Run: python3 scripts/sync_codex_manifests.py --all"
    )


@pytest.mark.skipif(shutil.which("agy") is None, reason="agy CLI not on PATH")
@pytest.mark.parametrize("name", ("loom-code", "loom-design", "loom-workflow"))
def test_agy_plugin_validate_accepts_committed_plugin(name):
    """A1 live: `agy plugin validate` passes and processes every skill folder."""
    proc = subprocess.run(
        ["agy", "plugin", "validate", str(REPO_ROOT / name)],
        capture_output=True, text=True, timeout=120,
    )
    out = re.sub(r"\x1b\[[0-9;]*m", "", proc.stdout + proc.stderr)
    assert proc.returncode == 0, out
    skills = len(list((REPO_ROOT / name / "skills").glob("*/SKILL.md")))
    assert re.search(rf"skills\s*:\s*{skills} processed", out), out


# --- agy plugin rule: loom-workflow/rules/AGENTS.md ----------------------------
# agy keeps a plugin's rules/AGENTS.md active in every session; Claude Code and
# Codex ignore it. The rule is generated from the trigger card so the card keeps
# one source: a one-line generated-file header, then the card verbatim.

def _rule_path(plugin_dir: Path) -> Path:
    return plugin_dir / "rules" / "AGENTS.md"


def _loom_workflow_fixture(tmp_path: Path) -> Path:
    claude = _claude_ssot()
    claude["name"] = "loom-workflow"
    plugin = _build_plugin(tmp_path / "loom-workflow", claude, _stale_codex())
    _write_card(plugin)
    return plugin


def test_agy_rule_matches_trigger_card_source(tmp_path):
    """A3 positive: sync writes header + card; the committed rule is in sync."""
    import sync_codex_manifests as m

    plugin = _loom_workflow_fixture(tmp_path)
    assert _run([], plugin).returncode == 0
    lines = _rule_path(plugin).read_text(encoding="utf-8").split("\n", 1)
    assert lines[0].startswith("<!--") and lines[0].endswith("-->"), lines[0]
    assert "/".join(CARD_REL) in lines[0] and "edit" in lines[0].lower()
    assert lines[1] == CARD_TEXT
    assert _run(["--check"], plugin).returncode == 0

    committed = REPO_ROOT / "loom-workflow"
    body = _rule_path(committed).read_text(encoding="utf-8").split("\n", 1)[1]
    assert body == committed.joinpath(*CARD_REL).read_text(encoding="utf-8")
    assert m.sync_agy_rule(committed, check=True) is True


def test_drifted_agy_rule_fails_check(tmp_path):
    """A3 negative: an edited rule, an edited card, or no rule fails --check."""
    plugin = _loom_workflow_fixture(tmp_path)
    assert _run([], plugin).returncode == 0

    rule = _rule_path(plugin)
    rule.write_text(rule.read_text(encoding="utf-8") + "hand-edited\n", encoding="utf-8")
    before = rule.read_text(encoding="utf-8")
    proc = _run(["--check"], plugin)
    assert proc.returncode != 0 and "DRIFT" in proc.stderr, proc.stderr
    assert "rules/AGENTS.md" in proc.stderr, proc.stderr
    assert rule.read_text(encoding="utf-8") == before  # --check is read-only

    assert _run([], plugin).returncode == 0
    _write_card(plugin, CARD_TEXT + "changed card\n")
    assert _run(["--check"], plugin).returncode != 0

    rule.unlink()
    missing = _run(["--check"], plugin)
    assert missing.returncode != 0 and "MISSING" in missing.stderr, missing.stderr
    assert "Traceback" not in missing.stderr


def test_agy_rule_only_for_mapped_plugin(tmp_path):
    """Only loom-workflow has a card; other plugins never get a rules dir."""
    dirs = _build_all_eligible(tmp_path)
    assert _run_all([], tmp_path).returncode == 0
    assert _rule_path(dirs["loom-workflow"]).exists()
    assert not (dirs["loom-code"] / "rules").exists()
    assert not (dirs["loom-design"] / "rules").exists()
    assert _run_all(["--check"], tmp_path).returncode == 0

    _rule_path(dirs["loom-workflow"]).write_text("drift\n", encoding="utf-8")
    drift = _run_all(["--check"], tmp_path)
    assert drift.returncode != 0 and "DRIFT" in drift.stderr, drift.stderr


def test_agy_rule_absent_source_writes_nothing_and_orphan_fails_check(tmp_path):
    """No card: sync writes no rule (no traceback); a leftover rule is drift."""
    plugin = _loom_workflow_fixture(tmp_path)
    plugin.joinpath(*CARD_REL).unlink()

    proc = _run([], plugin)
    assert proc.returncode == 0 and "Traceback" not in proc.stderr, proc.stderr
    assert not _rule_path(plugin).exists()
    assert _run(["--check"], plugin).returncode == 0

    _rule_path(plugin).parent.mkdir()
    _rule_path(plugin).write_text("orphan\n", encoding="utf-8")
    orphan = _run(["--check"], plugin)
    assert orphan.returncode != 0 and "DRIFT" in orphan.stderr, orphan.stderr


def test_hand_written_orphan_rule_tells_user_to_remove_it_by_hand(tmp_path):
    """No card and a rule without the generated header: sync would leave it,
    so --check must say to delete it by hand, not to rerun the sync."""
    plugin = _loom_workflow_fixture(tmp_path)
    plugin.joinpath(*CARD_REL).unlink()
    assert _run([], plugin).returncode == 0  # manifests in sync; only the rule is left
    _rule_path(plugin).parent.mkdir()
    _rule_path(plugin).write_text("hand-written\n", encoding="utf-8")

    proc = _run(["--check"], plugin)
    assert proc.returncode != 0, proc.stderr
    assert "remove" in proc.stderr.lower() and "by hand" in proc.stderr, proc.stderr
    assert "rules/AGENTS.md" in proc.stderr, proc.stderr
    assert "Run: python3" not in proc.stderr, proc.stderr


def test_claude_hook_still_injects_card_once(tmp_path):
    """A4 positive: one UserPromptSubmit card command; it injects the full card once."""
    plugin = REPO_ROOT / "loom-workflow"
    hooks = json.loads((plugin / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    assert "SessionStart" not in hooks["hooks"]
    commands = [h["command"] for group in hooks["hooks"]["UserPromptSubmit"]
                for h in group["hooks"] if h.get("type") == "command"]
    card_commands = [c for c in commands if "visualization-card" in c]
    assert len(card_commands) == 1, commands

    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    env["CLAUDE_CONFIG_DIR"] = str(tmp_path)  # no ascii-graph-toolkit installed
    proc = subprocess.run(
        [sys.executable, str(plugin / "hooks" / "visualization-card")],
        input=json.dumps({"cwd": str(tmp_path)}), capture_output=True,
        text=True, env=env, cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    context = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
    card = plugin.joinpath(*CARD_REL).read_text(encoding="utf-8")
    assert context == card
    assert context.count(card.splitlines()[0]) == 1


def test_claude_ignores_plugin_rules_dir():
    """A4 boundary: nothing Claude Code loads for loom-workflow points at rules/."""
    plugin = REPO_ROOT / "loom-workflow"
    assert _rule_path(plugin).exists()  # the agy rule is really there
    for rel in (".claude-plugin/plugin.json", "hooks/hooks.json",
                "hooks/visualization-card"):
        text = (plugin / rel).read_text(encoding="utf-8")
        assert "rules/" not in text and "AGENTS.md" not in text, rel
