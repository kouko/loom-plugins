"""Adversarial probes for the widened skill cross-reference checker.

Change 2026-09-16-loom-rule-text-consolidation extended
loom-code/scripts/check-skill-crossrefs.py to scan references files and
backtick `.md` paths (intent Acceptance 4). These probes build synthetic
plugin trees and try to slip a dead path past the scan, or make it flag a
valid one. Set LOOM_ROOT to run them against another checkout.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(os.environ.get("LOOM_ROOT", Path(__file__).resolve().parents[5]))
CHECKER = ROOT / "loom-code/scripts/check-skill-crossrefs.py"


def _checker():
    spec = importlib.util.spec_from_file_location("crossrefs_probe", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _plugin(tmp_path: Path, files: dict[str, str]) -> Path:
    plugin = tmp_path / "repo" / "plug"
    for rel, text in files.items():
        path = plugin / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return plugin / "skills"


def test_crossrefs_skillReferencesDeadLink_reported(tmp_path):
    """A dead inline link inside a skill's references file is reported."""
    skills = _plugin(tmp_path, {
        "skills/a/SKILL.md": "x\n",
        "skills/a/references/r.md": "see [gone](missing.md)\n",
    })
    assert _checker().find_broken_crossrefs(skills)


def test_crossrefs_pluginLevelReferencesDeadLink_reported(tmp_path):
    """A dead link inside a plugin-level references/*.md file is reported.

    loom-code/references/dispatch-profile.md is a changed rule file that
    stations link; Acceptance 4 names links written inside a references file.
    """
    skills = _plugin(tmp_path, {
        "skills/a/SKILL.md": "x\n",
        "references/shared.md": "see [gone](missing.md) and `skills/nope/SKILL.md`\n",
    })
    assert _checker().find_broken_crossrefs(skills)


def test_crossrefs_bareBacktickMissingName_reported(tmp_path):
    """A slash-free backtick `.md` name that exists nowhere is reported.

    confirm-intent.md tells the agent to load `one-way-door.md` and
    `second-vendor-ask-and-docs-lint.md` by bare name; a typo there dangles.
    """
    skills = _plugin(tmp_path, {
        "skills/a/SKILL.md": "x\n",
        "skills/a/references/r.md": "load `one-way-dor.md` before deciding\n",
        "skills/a/references/one-way-door.md": "classes\n",
    })
    assert _checker().find_broken_crossrefs(skills)


def test_crossrefs_wrongSkillBacktickPath_reported(tmp_path):
    """A backtick path valid only inside a sibling skill is reported."""
    skills = _plugin(tmp_path, {
        "skills/a/SKILL.md": "read `references/lenses.md`\n",
        "skills/b/SKILL.md": "x\n",
        "skills/b/references/lenses.md": "lenses\n",
    })
    assert _checker().find_broken_crossrefs(skills)


def test_crossrefs_traversalBacktickPath_reported(tmp_path):
    """A traversal path to a missing file above the repository is reported."""
    skills = _plugin(tmp_path, {
        "skills/a/SKILL.md": "read `../../../../../../nowhere/secret.md`\n",
    })
    assert _checker().find_broken_crossrefs(skills)


def test_crossrefs_placeholderAndProtocolPaths_skipped(tmp_path):
    """Placeholder, glob, URL and docs/ protocol paths are skipped."""
    skills = _plugin(tmp_path, {
        "skills/a/SKILL.md": (
            "`docs/loom/<change-id>/plan.md` `docs/loom/README.md` "
            "`skills/*/SKILL.md` `https://x.test/a/b.md` `~/.claude/x/y.md`\n"
        ),
    })
    assert _checker().find_broken_crossrefs(skills) == []


def test_crossrefs_nonUtf8ReferencesFile_failsLoudly(tmp_path):
    """An undecodable newly scanned references file fails, never passes silently."""
    skills = _plugin(tmp_path, {"skills/a/SKILL.md": "x\n"})
    bad = skills / "a/references/bad.md"
    bad.parent.mkdir(parents=True)
    bad.write_bytes(b"\xff\xfe `x/\xff.md`")
    with pytest.raises(Exception):
        _checker().find_broken_crossrefs(skills)


def test_crossrefs_consolidatedTree_passes():
    """The consolidated tree passes the extended checker (Acceptance 4)."""
    run = subprocess.run([sys.executable, str(CHECKER)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
