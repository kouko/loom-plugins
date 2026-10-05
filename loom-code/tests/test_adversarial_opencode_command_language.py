# concern: an OpenCode entry command writes the English SKILL.md body into the user's prompt record, so the language anchor loses the user's own language
"""Adversarial probe: running a newly registered OpenCode entry command in a
Traditional Chinese conversation must keep the Chinese language anchor.

The command's `execute` sends `/<id> <args>` followed by the skill body as the
prompt; the loader's prompt hook records that whole text as a user turn, and
the language detector then reads the English skill body as the user's words.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "tests"))
from test_opencode_loader import SKILL_CALL, ZH  # noqa: E402

# Wires ctx.session.prompt to the registered prompt hook, as OpenCode delivers
# a command's prompt: user prompt, then the command, then a Skill tool call.
DRIVER = r"""
import { pathToFileURL } from "node:url";
const hooks = {}, commands = {};
const ctx = {
  skill: { transform: async (fn) => fn({ add: () => {} }) },
  agent: { transform: async (fn) => fn({ update: () => {} }) },
  command: { transform: async (fn) => fn({ add: (c) => { commands[c.name] = c; } }) },
  session: {
    prompt: async (p) => hooks.prompt({ sessionID: p.sessionID, messageID: "m2", prompt: { text: p.text } }),
    hook: async (name, fn) => { hooks[name] = fn; },
    get: async ({ sessionID }) => ({ data: { id: sessionID } }),
  },
  tool: { hook: async (name, fn) => { hooks[name] = fn; } },
};
await (await import(pathToFileURL(process.argv[1]).href)).default.setup(ctx);
const [zh, command, call] = JSON.parse(process.argv[2]);
await hooks.prompt({ sessionID: "root", messageID: "m1", prompt: { text: zh } });
await commands[command].execute({ sessionID: "root", prompt: { text: "" } });
await hooks["execute.after"](call);
console.log(JSON.stringify(call.result.content.map((part) => part.text)));
"""


def test_entry_command_chinese_conversation_keeps_chinese_anchor(tmp_path: Path):
    """After a Chinese prompt and /loom-code:using-loom-code, a Skill call still gets the Chinese anchor."""
    args = json.dumps([ZH, "loom-code:using-loom-code", SKILL_CALL])
    proc = subprocess.run(
        [shutil.which("node"), "--input-type=module", "-e", DRIVER,
         str(REPO_ROOT / "loom-code" / "index.js"), args],
        capture_output=True, text=True, timeout=60, cwd=tmp_path,
        env={**os.environ, "TMPDIR": str(tmp_path)},
    )
    assert proc.returncode == 0, proc.stderr
    texts = json.loads(proc.stdout)
    assert any("使用者在對話中所用的語言" in text for text in texts), texts
