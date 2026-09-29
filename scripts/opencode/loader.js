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
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
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
}
