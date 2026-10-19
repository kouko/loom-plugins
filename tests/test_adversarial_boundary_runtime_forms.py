"""Adversarial probe: runtime files that read a loom-code file stay reported.

concern: the boundary check misses a cross-plugin read written in a runtime
file form it does not scan (shell hook script, hooks.json command) or as a
Python path join, so a new loom-code dependency can land unblocked.
"""
from pathlib import Path

import pytest

import check_plugin_boundaries as checker

FORMS = {
    "scripts/run.sh": '#!/bin/sh\npython3 "${CLAUDE_PLUGIN_ROOT}/../loom-code/scripts/review_context.py"\n',
    "hooks/hooks.json": '{"hooks": {"SessionStart": [{"hooks": [{"type": "command", '
    '"command": "${CLAUDE_PLUGIN_ROOT}/../loom-code/hooks/session-start"}]}]}}\n',
    "scripts/load.py": 'from pathlib import Path\n'
    'MANIFEST = Path(__file__).parents[2] / "loom-code" / "contract" / "manifest.yaml"\n',
}


@pytest.mark.parametrize("rel", sorted(FORMS))
def test_boundary_check_runtime_loom_code_read_is_reported(tmp_path: Path, rel: str) -> None:
    """A loom-code read planted in a shell script, a hooks.json command or a
    Python path join under loom-workflow yields at least one violation."""
    plugin = tmp_path / "loom-workflow"
    target = plugin / rel
    target.parent.mkdir(parents=True)
    target.write_text(FORMS[rel], encoding="utf-8")

    assert checker.find_boundary_violations(plugin), rel
