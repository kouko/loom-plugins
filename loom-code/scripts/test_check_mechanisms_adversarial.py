"""Adversarial probes for check_mechanisms.recompute_hooks with loom-workflow hooks.

A loom-workflow hooks.json is now counted in the hook population. These
probes feed it malformed JSON, a malformed shape, and a hook whose basename
collides with a loom-code hook id.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_mechanisms as cm  # noqa: E402

SESSION = {"hooks": {"SessionStart": [{"matcher": "startup|clear|compact", "hooks": [
    {"type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/session-start\""}]}]}}


def _repo(tmp_path, workflow_text):
    for plugin, text in (("loom-code", json.dumps(SESSION)), ("loom-workflow", workflow_text)):
        (tmp_path / plugin / "hooks").mkdir(parents=True)
        (tmp_path / plugin / "hooks" / "hooks.json").write_text(text, encoding="utf-8")
    return tmp_path


def test_check_mechanisms_malformed_workflow_hooks_json_fails_closed(tmp_path):
    """Malformed loom-workflow hooks.json raises instead of counting zero hooks."""
    with pytest.raises(json.JSONDecodeError):
        cm.recompute_hooks(_repo(tmp_path, "{bad"))


def test_check_mechanisms_non_object_hook_entry_fails_closed(tmp_path):
    """A string where a hook entry object belongs raises instead of being skipped."""
    with pytest.raises(AttributeError):
        cm.recompute_hooks(_repo(tmp_path, '{"hooks": {"SessionStart": ["x"]}}'))


def test_check_mechanisms_distinct_workflow_hook_counted(tmp_path):
    """A loom-workflow hook with a distinct basename adds its own id."""
    wf = {"hooks": {"SessionStart": [{"matcher": "startup|clear|compact", "hooks": [
        {"type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/visualization-card\""}]}]}}
    ids = cm.recompute_hooks(_repo(tmp_path, json.dumps(wf)))
    assert ids == {"SessionStart:startup|clear|compact:session-start",
                   "SessionStart:startup|clear|compact:visualization-card"}


@pytest.mark.xfail(strict=True, reason="finding: loom-workflow qualifier is '' so a colliding "
                   "basename merges into the loom-code id and one hook goes uncounted")
def test_check_mechanisms_colliding_workflow_basename_counted_separately(tmp_path):
    """Two hooks in two plugins with the same event, matcher and basename yield two ids."""
    repo = _repo(tmp_path, json.dumps(SESSION))
    ids = cm.recompute_hooks(repo)
    entries = cm._count_hooks_json_entries(SESSION) * 2
    assert len(ids) == entries
