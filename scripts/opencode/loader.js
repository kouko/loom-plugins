// OpenCode v2 loader shared by the Loom plugins.
// Canonical copy: scripts/opencode/loader.js. scripts/sync_codex_manifests.py
// copies it byte-identical to <plugin>/opencode/loader.js; edit this file, then
// run `python3 scripts/sync_codex_manifests.py --all`.
//
// It carries no plugin id: each plugin's root index.js exports
// `default { id: "<plugin>", setup }`, because duplicate plugin ids fail to load.
// The plugin root is the parent of this file's opencode/ directory.
//   <root>/skills/<name>/SKILL.md -> skill "<plugin>:<name>"
//     (disable-model-invocation: true -> user command "/<plugin>:<name>" instead)
//   <root>/agents/<name>.md       -> subagent "<plugin>:<name>"
//   <root>/hooks/hooks-opencode.json -> v2 tool and session hooks (registerHooks)
import { spawn } from "node:child_process";
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const plugin = JSON.parse(readFileSync(join(root, "package.json"), "utf8")).name;

function unquote(value) {
  if (value.length > 1 && value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1).replace(/''/g, "'");
  }
  if (value.length > 1 && value.startsWith('"') && value.endsWith('"')) {
    return JSON.parse(value);
  }
  return value;
}

// Frontmatter reader for the shapes Loom uses: `key: value`, quoted scalars,
// and `key: |` / `key: >` block scalars with indented continuation lines.
function parse(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return { data: {}, body: raw };
  const data = {};
  const lines = match[1].split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z_-]+):\s*(.*)$/);
    if (!kv) continue;
    const [, key, value] = kv;
    if (/^[|>][+-]?$/.test(value)) {
      const block = [];
      while (i + 1 < lines.length && (/^\s/.test(lines[i + 1]) || lines[i + 1] === "")) {
        block.push(lines[++i].trim());
      }
      data[key] = block.join(value.startsWith("|") ? "\n" : " ").trim();
    } else {
      data[key] = unquote(value.trim());
    }
  }
  return { data, body: raw.slice(match[0].length) };
}

function skills() {
  const dir = join(root, "skills");
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && existsSync(join(dir, e.name, "SKILL.md")))
    .map((e) => {
      const path = join(dir, e.name, "SKILL.md");
      const { data, body } = parse(readFileSync(path, "utf8"));
      return {
        id: `${plugin}:${e.name}`,
        name: data.name || e.name,
        description: data.description || "",
        path,
        content: `Base directory for this skill: ${dirname(path)}\n\n${body}`,
        userOnly: data["disable-model-invocation"] === "true",
      };
    });
}

function agents() {
  const dir = join(root, "agents");
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .map((f) => {
      const { data, body } = parse(readFileSync(join(dir, f), "utf8"));
      return { id: `${plugin}:${basename(f, ".md")}`, data, system: body.trim() };
    });
}

async function registerSkills(ctx, found) {
  const model = found.filter((s) => !s.userOnly);
  await ctx.skill.transform((draft) => {
    for (const { userOnly, ...skill } of model) draft.add(skill);
  });
}

// A user-only skill becomes a command whose prompt starts with the typed
// `/<plugin>:<name> <args>` text, so the prompt hook sees what the user typed.
async function registerCommands(ctx, found) {
  const commands = found.filter((s) => s.userOnly);
  if (commands.length === 0) return;
  await ctx.command.transform((draft) => {
    for (const skill of commands) {
      draft.add({
        name: skill.id,
        description: skill.description,
        execute: (input) => {
          const typed = `/${skill.id} ${input?.prompt?.text ?? ""}`.trim();
          return ctx.session.prompt({
            ...input.prompt,
            sessionID: input.sessionID,
            text: `${typed}\n\n${skill.content}`,
            delivery: input.delivery,
          });
        },
      });
    }
  });
}

async function registerAgents(ctx, found) {
  if (found.length === 0) return;
  await ctx.agent.transform((draft) => {
    for (const agent of found) {
      draft.update(agent.id, (info) => {
        info.name = agent.id;
        if (agent.data.description) info.description = agent.data.description;
        info.mode = "subagent";
        info.system = agent.system;
        // Only a "provider/model" value names an OpenCode model; else inherit.
        const model = agent.data.model;
        if (model && model.includes("/")) {
          const [providerID, ...rest] = model.split("/");
          info.model = { providerID, id: rest.join("/") };
        }
      });
    }
  });
}

// Each capability registers in its own step, so a later one (hooks) is one
// more function and one more line here.
export async function setup(ctx) {
  const found = skills();
  await registerSkills(ctx, found);
  await registerCommands(ctx, found);
  await registerAgents(ctx, agents());
  await registerHooks(ctx);
}

// hooks/hooks-opencode.json has the Claude hooks.json schema, event names and
// tool-name matchers. Each command runs through `bash -c` with PLUGIN_ROOT set
// and cwd = the project, fed the Claude Code payload built from the OpenCode
// call, so the handlers are the ones every other host runs.
const TOOLS = {
  shell: (i) => ["Bash", { command: i.command }],
  write: (i) => ["Write", { file_path: i.filePath, content: i.content }],
  edit: (i) => ["Edit", { file_path: i.filePath, old_string: i.oldString, new_string: i.newString }],
  patch: (i) => ["apply_patch", { ...i }],
  apply_patch: (i) => ["apply_patch", { ...i }],
  skill: (i) => ["Skill", { skill: i.id }],
};

// selection.guard's store patterns, applied only when the checker cannot be
// reached: a failed handler never loosens the guard.
const STORE = [/loom\/selections\//, /\.git\/loom/];
const STORE_TEXT = [...STORE, /(?<![\w.-])selections\//, /git-common-dir|--git-dir|\bGIT_DIR\b/];
const PATCH_TARGET = /^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+?)\s*$/gm;

function namesStore(name, input, cwd) {
  const hit = (patterns, text) => patterns.some((p) => p.test(text));
  if (name === "Bash") return hit(STORE, `${resolve(cwd)}/`) || hit(STORE_TEXT, input.command ?? "");
  const targets = [input.file_path, ...Object.values(input)
    .filter((v) => typeof v === "string")
    .flatMap((v) => [...v.matchAll(PATCH_TARGET)].map((m) => m[1]))];
  return targets.some((t) => typeof t === "string" && hit(STORE, `${resolve(cwd, t)}/`));
}

function hookTable() {
  const path = join(root, "hooks", "hooks-opencode.json");
  return existsSync(path) ? JSON.parse(readFileSync(path, "utf8")).hooks ?? {} : {};
}

// SessionStart ignores its matcher: OpenCode reports no startup source.
function commands(table, event, tool) {
  return (table[event] ?? [])
    .filter((e) => tool === undefined || !e.matcher || e.matcher.split("|").includes(tool))
    .flatMap((e) => e.hooks ?? []);
}

function run(hook, payload, env) {
  return new Promise((done) => {
    let stdout = "";
    let stderr = "";
    const child = spawn("bash", ["-c", hook.command], {
      cwd: process.cwd(),
      env: { ...process.env, PLUGIN_ROOT: root, ...env },
      timeout: (hook.timeout ?? 30) * 1000,
    });
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("error", (error) => done({ status: null, stdout, stderr: String(error) }));
    child.on("close", (status) => done({ status, stdout, stderr }));
    child.stdin.on("error", () => {});
    child.stdin.end(JSON.stringify(payload));
  });
}

function output(result) {
  try {
    const data = JSON.parse(result.stdout);
    return {
      context: data.hookSpecificOutput?.additionalContext || data.additionalContext || "",
      message: data.systemMessage || "",
    };
  } catch {
    return { context: "", message: "" };
  }
}

function note(result, text) {
  if (Array.isArray(result?.content)) result.content.push({ type: "text", text });
  else if (typeof result?.output === "string") result.output += `\n\n${text}`;
}

// The per-session user-prompt file lang_detect reads as a Claude transcript.
function transcript(sessionID) {
  const name = String(sessionID).replace(/[^A-Za-z0-9_.-]/g, "_");
  return join(tmpdir(), "loom-opencode", `${name}.jsonl`);
}

async function registerHooks(ctx) {
  const table = hookTable();
  const payload = (sessionID, event, extra) =>
    ({ hook_event_name: event, session_id: sessionID, cwd: process.cwd(), ...extra });

  // A session with a parent, or one whose parent cannot be read, is a child:
  // it gets no context, records no prompt, and its handlers run unattended.
  const parents = new Map();
  const isChild = (sessionID) => {
    if (!sessionID) return Promise.resolve(true);
    if (!parents.has(sessionID)) {
      parents.set(sessionID, Promise.resolve()
        .then(() => ctx.session.get({ sessionID }))
        .then((r) => Boolean((r?.data ?? r)?.parentID), () => true));
    }
    return parents.get(sessionID);
  };
  const envFor = async (sessionID) =>
    ((await isChild(sessionID)) ? { CLAUDE_CODE_SESSION_ATTENDED: "0" } : {});

  const started = new Map(); // session id -> SessionStart context, run once
  const turn = new Map(); // session id -> the latest prompt's added context
  if (table.SessionStart || table.UserPromptSubmit) {
    await ctx.session.hook("context", async (ev) => {
      const id = ev.sessionID;
      if (!id || (await isChild(id))) return;
      if (!started.has(id)) {
        started.set(id, (async () => {
          const texts = [];
          for (const hook of commands(table, "SessionStart")) {
            texts.push(output(await run(hook, payload(id, "SessionStart", { source: "startup" }))).context);
          }
          return texts.filter(Boolean).join("\n\n");
        })());
      }
      for (const text of [await started.get(id), turn.get(id)]) {
        if (text) ev.system.push({ type: "text", text });
      }
    });
  }

  if (table.UserPromptSubmit) {
    const keepsTranscript = commands(table, "PostToolUse", "Skill").length > 0;
    await ctx.session.hook("prompt", async (ev) => {
      const id = ev.sessionID;
      const text = ev.prompt?.text;
      if (typeof text !== "string" || (await isChild(id))) return;
      const file = transcript(id);
      if (keepsTranscript) {
        try {
          mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
          appendFileSync(file, `${JSON.stringify({ type: "user", message: { role: "user", content: text } })}\n`);
        } catch {} // no transcript only costs the language reminder
      }
      const added = [];
      for (const hook of commands(table, "UserPromptSubmit")) {
        const result = output(await run(hook, payload(id, "UserPromptSubmit",
          { prompt: text, prompt_id: ev.messageID, transcript_path: file })));
        added.push(result.context, result.message);
      }
      turn.set(id, added.filter(Boolean).join("\n\n"));
    });
  }

  if (!table.PreToolUse && !table.PostToolUse) return;
  const notes = new Map(); // tool call id -> PreToolUse systemMessage lines
  await ctx.tool.hook("execute.before", async (ev) => {
    const mapped = TOOLS[ev.tool]?.(ev.input ?? {});
    if (!mapped) return;
    const [name, input] = mapped;
    const env = await envFor(ev.sessionID);
    const body = payload(ev.sessionID, "PreToolUse", { tool_name: name, tool_input: input });
    for (const hook of commands(table, "PreToolUse", name)) {
      const result = await run(hook, body, env);
      if (result.status === 2) throw new Error(result.stderr.trim() || `loom: a PreToolUse hook refused ${name}`);
      if (result.status !== 0 && namesStore(name, input, process.cwd())) {
        const why = result.stderr.trim() || `exit ${result.status}`;
        throw new Error(`BLOCK selection.guard: names the selection record store and the checker failed (${why})`);
      }
      const { message } = output(result);
      if (message) notes.set(ev.id, [...(notes.get(ev.id) ?? []), message]);
    }
  });
  await ctx.tool.hook("execute.after", async (ev) => {
    const held = notes.get(ev.id) ?? [];
    notes.delete(ev.id);
    const mapped = TOOLS[ev.tool]?.(ev.input ?? {});
    if (mapped && ev.status !== "error") {
      const [name, input] = mapped;
      const env = await envFor(ev.sessionID);
      const body = payload(ev.sessionID, "PostToolUse",
        { tool_name: name, tool_input: input, transcript_path: transcript(ev.sessionID) });
      for (const hook of commands(table, "PostToolUse", name)) {
        const result = await run(hook, body, env);
        held.push(result.status === 2 ? result.stderr.trim() : output(result).context);
      }
    }
    for (const text of held.filter(Boolean)) note(ev.result, text);
  });
}
