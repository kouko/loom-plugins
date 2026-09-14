"""Adversarial probe: hand-typed `gh pr merge` forms against the publication hook.

Each case asserts the SAFE behaviour (the hook blocks). A failing case is a
form that slips past `contains_pr_merge`, which is the sole gate for
intent Acceptance #11 ("a hand-typed gh pr merge is still refused").
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.command_handlers.push import contains_pr_merge  # noqa: E402

VERB = "gh pr " + "merge"

BASELINE = [
    f"{VERB} 7 --squash",
    f"GH_TOKEN=x {VERB} 7",
    f"/opt/homebrew/bin/{VERB} 7",
    f"command {VERB} 7",
    f"'gh' 'pr' 'merge' 7",
    f"GH pr merge 7",
    f"eval '{VERB} 7'",
    f"bash -c '{VERB} 7'",
    f"echo $({VERB} 7)",
    f"cd /tmp && {VERB} 7",
    f"exec {VERB} 7",
]

# Wrapper words the classifier already strips (PREFIX_WORDS) or shells it
# already unwraps (SHELL_PROGRAMS -c), written with ordinary options.
UNWRAPPED_WITH_OPTIONS = [
    f"bash -lc '{VERB} 7'",
    f"bash -ec '{VERB} 7'",
    f"sudo -u me {VERB} 7",
    f"nice -n 5 {VERB} 7",
    f"time -p {VERB} 7",
    f"command -p {VERB} 7",
    f"echo 7 | xargs -n1 {VERB}",
    f"exec -a x {VERB} 7",
]

# Plain shell grammar around a literal merge; no obfuscation.
COMPOUND_GRAMMAR = [
    f"({VERB} 7)",
    f"{{ {VERB} 7; }}",
    f"if true; then {VERB} 7; fi",
    f"for n in 7; do {VERB} $n; done",
    f"! {VERB} 7",
    "gh pr \\\nmerge 7",
]

# Deliberate obfuscation outside the spec's classifier scope: recorded as notes.
OBFUSCATED = [
    "sh -c \"$(printf 'gh pr %s 7' merge)\"",
    f"env -S '{VERB} 7'",
    "gh api -X PUT repos/o/r/pulls/7/merge",
]


@pytest.mark.parametrize("command", BASELINE)
def test_hookClassifier_canonicalForms_blocked(command: str) -> None:
    """Forms the spec names (direct, prefixed, eval, bash -c) are blocked."""
    assert contains_pr_merge(command), command


@pytest.mark.parametrize("command", UNWRAPPED_WITH_OPTIONS)
def test_hookClassifier_wrapperWithOptions_blocked(command: str) -> None:
    """A wrapper the hook already strips or unwraps, given an option, still blocks."""
    assert contains_pr_merge(command), command


@pytest.mark.parametrize("command", COMPOUND_GRAMMAR)
def test_hookClassifier_compoundGrammar_blocked(command: str) -> None:
    """A literal merge inside subshell, group, if/for, negation or line continuation blocks."""
    assert contains_pr_merge(command), command


@pytest.mark.xfail(strict=False, reason="note: obfuscated form outside the spec classifier scope")
@pytest.mark.parametrize("command", OBFUSCATED)
def test_hookClassifier_obfuscatedForms_blocked(command: str) -> None:
    """Obfuscated merges are recorded; a slip-through is a note, not a finding."""
    assert contains_pr_merge(command), command


@pytest.mark.parametrize("command", [f"{VERB} 7", f"({VERB} 7)"])
def test_installedHook_mergeCommand_exitsTwo(command: str, tmp_path: Path) -> None:
    """The installed `push --hook` entry point refuses the command end to end."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command},
                          "cwd": str(tmp_path)})
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "loom_checker.py"), "push", "--hook"],
        input=payload, capture_output=True, text=True, cwd=tmp_path, timeout=60,
    )
    assert result.returncode == 2, (result.returncode, result.stderr)
    assert "BLOCK push.merge" in result.stderr
