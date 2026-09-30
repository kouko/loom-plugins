# concern: loom-code's OpenCode prompt hook trims only loom-code's own command bodies, so a sibling plugin's command records its English skill body as the user's words
"""Adversarial probe: loom-code keeps the only OpenCode transcript, and its
prompt hook sees every prompt in the session, including a command prompt that
loom-workflow or loom-design built. That prompt must still be recorded as only
the typed command text, as the intent's Acceptance 2 says for a loom command.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# loom-code and a sibling plugin share one OpenCode session: the sibling's
# command prompt is delivered to loom-code's prompt hook.
DRIVER = r"""
import { pathToFileURL } from "node:url";
function stub(hooks, commands, onPrompt) {
  return {
    skill: { transform: async (fn) => fn({ add: () => {} }) },
    agent: { transform: async (fn) => fn({ update: () => {} }) },
    command: { transform: async (fn) => fn({ add: (c) => { commands[c.name] = c; } }) },
    session: {
      prompt: onPrompt,
      hook: async (name, fn) => { hooks[name] = fn; },
      get: async ({ sessionID }) => ({ data: { id: sessionID } }),
    },
    tool: { hook: async (name, fn) => { hooks[name] = fn; } },
  };
}
const [codeIndex, siblingIndex, command] = process.argv.slice(1);
const codeHooks = {}, siblingCommands = {};
await (await import(pathToFileURL(codeIndex).href)).default.setup(stub(codeHooks, {}, async () => {}));
const deliver = async (p) => codeHooks.prompt({ sessionID: "root", messageID: "m1", prompt: { text: p.text } });
await (await import(pathToFileURL(siblingIndex).href)).default.setup(stub({}, siblingCommands, deliver));
await siblingCommands[command].execute({ sessionID: "root", prompt: { text: "" } });
"""


def test_opencodePromptHook_siblingPluginCommand_recordsTypedTextOnly(tmp_path: Path):
    """A /loom-workflow:handoff prompt reaching loom-code's hook is recorded as '/loom-workflow:handoff'."""
    proc = subprocess.run(
        [shutil.which("node"), "--input-type=module", "-e", DRIVER,
         str(REPO_ROOT / "loom-code" / "index.js"), str(REPO_ROOT / "loom-workflow" / "index.js"),
         "loom-workflow:handoff"],
        capture_output=True, text=True, timeout=60, cwd=tmp_path,
        env={**os.environ, "TMPDIR": str(tmp_path)},
    )
    assert proc.returncode == 0, proc.stderr
    line = (tmp_path / "loom-opencode" / "root.jsonl").read_text(encoding="utf-8").splitlines()[0]
    assert json.loads(line)["message"]["content"] == "/loom-workflow:handoff"
