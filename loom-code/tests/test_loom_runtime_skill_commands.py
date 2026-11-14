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
    assert ('"${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --repair '
            '--script checked_readonly.py contract --require 2.1') in plan
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
    prerequisite = plan.split("## Step 0 —", 1)[1].split("## Step 0b", 1)[0]
    policy = re.compile(r"Only\b(?P<scope>.*?)`rule_id: contract\.requires`"
                        r"(?P<effect>.*?)outdated-contract response", re.S)
    affirmative = ("Only an accepted blocked result whose diagnostics includes "
                   "`rule_id: contract.requires` establishes the outdated-contract response")
    for text, expected in ((prerequisite, True), (affirmative, True),
                           (affirmative.replace("includes", "does not include"), False)):
        match = policy.search(text)
        valid = bool(match and all(word in match["scope"] for word in ("accepted", "blocked", "includes"))
                     and "establishes" in match["effect"]
                     and not re.search(r"\b(?:not|never|no|cannot|mustn't|shouldn't)\b", match[0]))
        assert valid is expected
    assert re.search(r"launcher/startup failures stop this prerequisite with\s+their own diagnostics",
                     prerequisite)
