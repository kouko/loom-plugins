"""Loom station commands use the plugin runtime, not the host Python."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SURFACES = [*sorted((ROOT / "skills").rglob("*.md")),
            ROOT / "references" / "dispatch-profile.md"]
SCRIPTS = ("loom_checker", "dispatch_profile", "second_vendor_policy",
           "external_review")


def test_plugin_script_commands_use_repair_launcher() -> None:
    texts = {path: path.read_text(encoding="utf-8") for path in SURFACES}
    direct = re.compile(
        r"python3?\s+[^\s`]*?/scripts/(?:" + "|".join(SCRIPTS) + r")\.py"
    )
    for path, content in texts.items():
        assert not direct.search(content), path

    plan = texts[ROOT / "skills/write-plan/SKILL.md"]
    assert '"${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --repair contract --require 2.1' in plan
    assert ('"${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --repair '
            '--script second_vendor_policy.py') in plan
    assert ('"<loom-code>/scripts/loom-python" --repair '
            '--script external_review.py') in texts[ROOT / "skills/external-review/SKILL.md"]
    assert ('"<loom-code>/scripts/loom-python" --repair '
            '--script dispatch_profile.py') in texts[ROOT / "references/dispatch-profile.md"]


def test_project_python_commands_stay_project_owned() -> None:
    review = (ROOT / "skills/closing-review/SKILL.md").read_text(encoding="utf-8")
    adversarial = (ROOT / "skills/closing-review/references/adversarial.md").read_text(encoding="utf-8")
    assert '"command":"python3 -m pytest <path>"' in review
    assert '"command": "python3 -m pytest docs/loom/<change-id>/evidence/probes/test_abuse_empty_input.py"' in adversarial


def test_bootstrap_failure_is_not_reported_as_stale_contract() -> None:
    plan = (ROOT / "skills/write-plan/SKILL.md").read_text(encoding="utf-8")
    assert "Only a `contract.requires` result means the plugin contract is outdated" in plan
