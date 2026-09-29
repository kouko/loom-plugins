"""OpenCode v2 loader: each plugin's root index.js registers plugin-qualified
skills and agents on a stub plugin context.

The stub records what `setup(ctx)` hands to `ctx.skill.transform`,
`ctx.agent.transform` and `ctx.command.transform`, and keeps the functions
handed to `ctx.tool.hook` / `ctx.session.hook` so a test can fire one with an
OpenCode event (a session id starting with `child` has a parent session).
Node is required: a missing node fails, it does not skip.
"""
from __future__ import annotations

import functools
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

HARNESS = r"""
import { pathToFileURL } from "node:url";
const seen = { skills: [], agents: [], commands: [] };
const hooks = {};
const ctx = {
  skill: { transform: async (fn) => fn({ add: (s) => seen.skills.push(s) }) },
  agent: { transform: async (fn) => fn({ update: (id, f) => { const info = {}; f(info); seen.agents.push({ id, ...info }); } }) },
  command: { transform: async (fn) => fn({ add: (c) => seen.commands.push({ name: c.name, execute: typeof c.execute }) }) },
  session: {
    prompt: async () => {},
    hook: async (name, fn) => { hooks[name] = fn; },
    get: async ({ sessionID }) => ({ data: { id: sessionID, parentID: sessionID.startsWith("child") ? "root" : undefined,
      location: process.env.STUB_SESSION_DIR ? { directory: process.env.STUB_SESSION_DIR } : undefined } }),
  },
  tool: { hook: async (name, fn) => { hooks[name] = fn; } },
};
const mod = (await import(pathToFileURL(process.argv[1]).href)).default;
await mod.setup(ctx);
if (process.argv[2]) {
  let threw = null, event = null;
  for (const fire of [].concat(JSON.parse(process.argv[2]))) {
    threw = null; event = fire.event;
    try { await hooks[fire.hook](fire.event); } catch (e) { threw = e.message; }
  }
  console.log(JSON.stringify({ threw, event }));
} else {
  console.log(JSON.stringify({ id: mod.id, ...seen }));
}
"""


def _node(plugin: str, *args: str, cwd=None, env=None) -> dict:
    node = shutil.which("node")
    assert node, "node is required to exercise the OpenCode loader"
    proc = subprocess.run(
        [node, "--input-type=module", "-e", HARNESS, str(REPO_ROOT / plugin / "index.js"), *args],
        capture_output=True, text=True, timeout=60, cwd=cwd, env=env,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


@functools.lru_cache(maxsize=None)
def _register(plugin: str) -> dict:
    return _node(plugin)


def _fire(plugin: str, hook: str, event: dict, cwd: Path, env=None) -> dict:
    return _node(plugin, json.dumps({"hook": hook, "event": event}), cwd=cwd, env=env)


def _skill_dirs(plugin: str) -> dict:
    return {p.parent.name: p.read_text(encoding="utf-8")
            for p in (REPO_ROOT / plugin / "skills").glob("*/SKILL.md")}


def _model_invocable(text: str) -> bool:
    front = text.split("---", 2)[1]
    return not re.search(r"^disable-model-invocation:\s*true\s*$", front, re.M)


def test_skills_registered_plugin_qualified():
    for plugin in ("loom-code", "loom-design", "loom-workflow"):
        seen = _register(plugin)
        assert seen["id"] == plugin
        expected = {f"{plugin}:{name}" for name, text in _skill_dirs(plugin).items()
                    if _model_invocable(text)}
        assert {s["id"] for s in seen["skills"]} == expected
        for skill in seen["skills"]:
            assert skill["content"].strip() and skill["description"].strip() not in ("", "|")


def test_disable_model_invocation_skill_not_model_registered():
    seen = _register("loom-code")
    assert "loom-code:expert-mode" not in {s["id"] for s in seen["skills"]}
    assert seen["commands"] == [{"name": "loom-code:expert-mode", "execute": "function"}]


def test_disable_model_invocation_read_case_insensitively_with_comment(tmp_path: Path):
    plugin = tmp_path / "demo"
    (plugin / "opencode").mkdir(parents=True)
    (plugin / "skills" / "x").mkdir(parents=True)
    (plugin / "package.json").write_text('{"name": "demo"}', encoding="utf-8")
    shutil.copy(REPO_ROOT / "loom-code" / "index.js", plugin / "index.js")
    shutil.copy(REPO_ROOT / "scripts" / "opencode" / "loader.js", plugin / "opencode" / "loader.js")
    (plugin / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndisable-model-invocation: True  # user-only\n---\nbody\n", encoding="utf-8")
    assert _node(str(plugin))["skills"] == []


def test_agents_registered_plugin_qualified():
    seen = _register("loom-code")
    expected = {f"loom-code:{p.stem}" for p in (REPO_ROOT / "loom-code" / "agents").glob("*.md")}
    assert {a["id"] for a in seen["agents"]} == expected
    for agent in seen["agents"]:
        assert agent["mode"] == "subagent" and agent["system"].strip()
        first = agent["system"].splitlines()[0]
        assert str(REPO_ROOT / "loom-code") in first and "<plugin>/" in first


def test_plugin_without_agents_registers_none():
    for plugin in ("loom-design", "loom-workflow"):
        seen = _register(plugin)
        assert seen["agents"] == [] and seen["commands"] == []


def test_shell_push_routed_to_push_hook(tmp_path: Path):
    event = {"tool": "shell", "sessionID": "root", "id": "c1", "input": {"command": "ls .git/loom"}}
    threw = _fire("loom-code", "execute.before", event, tmp_path)["threw"]
    # the checker's own refusal, not the loader's unreachable-handler fallback
    assert threw and threw.startswith("BLOCK selection.guard") and "checker failed" not in threw
    # `workdir` moves the call into the store: a plain redirect write is refused
    repo = tmp_path / "proj"
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".git" / "loom" / "selections").mkdir(parents=True)
    moved = {**event, "input": {"command": "printf x > rec", "workdir": ".git/loom/selections"}}
    env = {**os.environ, "STUB_SESSION_DIR": str(repo)}
    threw = _fire("loom-code", "execute.before", moved, tmp_path, env)["threw"]
    assert threw and threw.startswith("BLOCK selection.guard")


def test_subagent_prompt_entry_token_records_nothing(tmp_path: Path):
    bin_dir, log = tmp_path / "bin", tmp_path / "python3.log"
    bin_dir.mkdir()
    fake = bin_dir / "python3"
    fake.write_text(f'#!/bin/bash\necho "$*" >> "{log}"\ncat >/dev/null\n', encoding="utf-8")
    fake.chmod(0o755)
    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "TMPDIR": str(tmp_path)}
    for session in ("child-1", "root"):
        event = {"sessionID": session, "messageID": "m1",
                 "prompt": {"text": "/loom-code:expert-mode K7Q2"}}
        _fire("loom-code", "prompt", event, tmp_path, env)
        if session.startswith("child"):
            assert not log.exists()
            assert not (tmp_path / "loom-opencode" / f"{session}.jsonl").exists()
    assert "selection capture --hook" in log.read_text(encoding="utf-8")  # the root control


def test_nested_skill_folder_write_noted(tmp_path: Path):
    # OpenCode 2.0.18 sends `path` relative to the session's directory, which
    # differs from the loader process's cwd under the background service.
    project, elsewhere = tmp_path / "proj", tmp_path / "home"
    nested = project / "skills" / "demo" / "assets" / "sub" / "x.md"
    nested.parent.mkdir(parents=True)
    elsewhere.mkdir()
    (project / "skills" / "demo" / "SKILL.md").write_text("---\nname: demo\n---\n", encoding="utf-8")
    nested.write_text("x", encoding="utf-8")
    event = {"tool": "write", "sessionID": "root", "id": "c2", "status": "completed",
             "input": {"path": "skills/demo/assets/sub/x.md", "content": "x"},
             "result": {"output": "Wrote file", "content": [{"type": "text", "text": "Wrote file"}]}}
    env = {**os.environ, "STUB_SESSION_DIR": str(project)}
    result = _fire("loom-workflow", "execute.after", event, elsewhere, env)["event"]["result"]
    assert any("Skill folder structure violation" in part["text"] for part in result["content"])
    assert "Skill folder structure violation" in result["output"]  # the field OpenCode stores


def test_push_reminder_uses_session_directory(tmp_path: Path):
    repo, elsewhere = tmp_path / "proj", tmp_path / "home"
    repo.mkdir()
    elsewhere.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "feature/demo", str(repo)], check=True)
    call = {"tool": "shell", "sessionID": "root", "id": "c3", "status": "completed",
            "input": {"command": "git push --dry-run origin HEAD"},
            "result": {"output": "pushed", "content": [{"type": "text", "text": "pushed"}]}}
    fires = [{"hook": "execute.before", "event": call}, {"hook": "execute.after", "event": call}]
    env = {**os.environ, "STUB_SESSION_DIR": str(repo)}
    output = _node("loom-code", json.dumps(fires), cwd=elsewhere, env=env)["event"]["result"]["output"]
    assert "change not identified" in output and "not inside a git work tree" not in output
