"""OpenCode v2 loader: each plugin's root index.js registers plugin-qualified
skills and agents on a stub plugin context.

The stub records what `setup(ctx)` hands to `ctx.skill.transform`,
`ctx.agent.transform` and `ctx.command.transform`. Node is required: a missing
node fails, it does not skip.
"""
from __future__ import annotations

import functools
import json
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

HARNESS = r"""
import { pathToFileURL } from "node:url";
const seen = { skills: [], agents: [], commands: [] };
const ctx = {
  skill: { transform: async (fn) => fn({ add: (s) => seen.skills.push(s) }) },
  agent: { transform: async (fn) => fn({ update: (id, f) => { const info = {}; f(info); seen.agents.push({ id, ...info }); } }) },
  command: { transform: async (fn) => fn({ add: (c) => seen.commands.push({ name: c.name, execute: typeof c.execute }) }) },
  session: { prompt: async () => {} },
};
const mod = (await import(pathToFileURL(process.argv[1]).href)).default;
await mod.setup(ctx);
console.log(JSON.stringify({ id: mod.id, ...seen }));
"""


@functools.lru_cache(maxsize=None)
def _register(plugin: str) -> dict:
    node = shutil.which("node")
    assert node, "node is required to exercise the OpenCode loader"
    proc = subprocess.run(
        [node, "--input-type=module", "-e", HARNESS, str(REPO_ROOT / plugin / "index.js")],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


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


def test_agents_registered_plugin_qualified():
    seen = _register("loom-code")
    expected = {f"loom-code:{p.stem}" for p in (REPO_ROOT / "loom-code" / "agents").glob("*.md")}
    assert {a["id"] for a in seen["agents"]} == expected
    for agent in seen["agents"]:
        assert agent["mode"] == "subagent" and agent["system"].strip()


def test_plugin_without_agents_registers_none():
    for plugin in ("loom-design", "loom-workflow"):
        seen = _register(plugin)
        assert seen["agents"] == [] and seen["commands"] == []
