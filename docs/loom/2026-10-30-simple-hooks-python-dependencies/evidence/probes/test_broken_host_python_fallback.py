"""A broken host Python must not hide an available Loom hook runtime."""

# concern: a command found on PATH can fail to start the hook, losing context despite a ready cached runtime

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[5] / "loom-code"


@pytest.mark.parametrize("manifest,event,matcher,payload", [
    ("hooks/hooks.json", "UserPromptSubmit", "", {"hook_event_name": "UserPromptSubmit"}),
    ("hooks/hooks-opencode.json", "PostToolUse", "Skill",
     {"hook_event_name": "PostToolUse", "tool_name": "Skill"}),
    ("hooks.json", "PreInvocation", "", {"conversationId": "broken-host-python",
                                               "invocationNum": 0, "initialNumSteps": 1}),
])
def test_broken_host_python_uses_ready_runtime(manifest, event, matcher, payload, tmp_path):
    data = json.loads((ROOT / manifest).read_text())
    entries = (data["loom-code"] if manifest == "hooks.json" else data["hooks"])[event]
    entry = next(item for item in entries if item.get("matcher", "") == matcher)
    command = entry["command"] if manifest == "hooks.json" else entry["hooks"][0]["command"]

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    broken = bin_dir / "python3"
    broken.write_text("#!/bin/sh\necho broken-system-python >&2\nexit 42\n")
    broken.chmod(0o755)
    cached_bin = tmp_path / "cache/loom-code/python-3.11-pyyaml-6.0.2-v1/bin"
    cached_bin.mkdir(parents=True)
    cached = cached_bin / "python"
    cached.write_text(f'#!/bin/sh\nif [ "$3" = "-c" ]; then exit 0; fi\nexec "{sys.executable}" "$@"\n')
    cached.chmod(0o755)
    payload = {**payload, "workspacePaths": [str(tmp_path)]}
    env = {**os.environ, "PATH": f"{bin_dir}:/bin:/usr/bin", "XDG_CACHE_HOME": str(tmp_path / "cache"),
           "TMPDIR": str(tmp_path), "CLAUDE_PLUGIN_ROOT": str(ROOT), "PLUGIN_ROOT": str(ROOT)}
    result = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(payload),
                            text=True, capture_output=True, cwd=ROOT, env=env, timeout=30)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    if manifest == "hooks.json":
        assert output["injectSteps"]
    else:
        assert output["hookSpecificOutput"]["additionalContext"]
