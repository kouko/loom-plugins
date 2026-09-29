# OpenCode live checks — 2026-09-29-opencode-v2-compatibility (W3-01)

Binary: `/Users/kouko/.opencode/bin/opencode` v2.0.18. Plugins installed from the
local branch at commit `33ec1d9` with
`opencode plugin add 'git+file:///Users/kouko/GitHub/loom-plugins#engineering/2026-09-29-opencode-v2-compatibility::path:<plugin>'`.
Everything ran under an isolated `XDG_*` + `OPENCODE_CONFIG_DIR` tree (`<S>` below),
never the user's own OpenCode config. Project dir: a throwaway git repo `<S>/proj`
on branch `feature/demo` with a bare local `origin`. Model: `litellm/nvidia-only`
(the configured default `gemini-flash-lite-only` returned a 401 upstream). The
gateway key lived only in the server's environment and is not in any file here.

Two server shapes were used:
- **dedicated** — `opencode serve --port 4998` started with cwd = `<S>/proj`;
  prompts sent with `opencode run --server …`.
- **service** — the managed background service that `opencode` (TUI),
  `opencode run` and `opencode plugin list` use by default (port set to 4997
  in the isolated config). This is the shape a user gets.

## Results

| check | command/method | observed | verdict |
|---|---|---|---|
| none-installed-before-add | `plugin list` in a second fresh config with no `plugins` entry | `No plugins found`, exit 0 (twice) | works |
| git-file-install-lists-three-plugins | `plugin add 'git+file://…::path:<plugin>'` ×3, then `plugin list` | each add: `Plugin "…" installed and added to <S>/cfg/opencode.json`; list shows `loom-code`, `loom-design`, `loom-workflow` at `33ec1d9`; log has three `loading plugin` lines, no error | works |
| plugin list right after service cold start | `plugin list` as the first command | printed `No plugins found` once while plugins were still loading; the same command a few seconds later listed all three | works (race; retry) |
| TUI plugin dialog shows installs | tmux → `ctrl+p` → `Plugins` | dialog lists `loom-code`, `loom-design`, `loom-workflow` `33ec1d9` under `Server` | works |
| TUI "Install plugin" dialog | tmux → `Plugins` dialog → `shift+I` (binary's binding `dialog.plugins.install`); palette search `install`; `cli.json` rebinding to F6/F7 | `shift+I` typed `I` into the dialog search (also with tmux `extended-keys` csi-u); palette: `No results found`; rebinding had no effect | not-run (could not drive through tmux) |
| skills registered, plugin-qualified | `GET /api/skill` | 24 `loom-*:*` skills (6 loom-code, 6 loom-design, 12 loom-workflow), matching the repo's model-invocable SKILL.md count; no `expert-mode` skill | works |
| expert-mode as command | `GET /api/command` | `loom-code:expert-mode` listed as a command | works |
| skill load body + base dir | model called `skill` `{"id":"loom-code:write-plan"}` | result starts `<skill_content name="write-plan">`, then `Base directory for this skill: <S>/xdg/cache/opencode/npm/…/node_modules/loom-code/skills/write-plan`, then the SKILL.md body and a `<skill_files>` list | works |
| agents registered | `GET /api/agent` | `loom-code:reviewer`, `loom-code:implementer`, `loom-code:adversary`, `loom-code:acceptance-tester`, all `mode: subagent` | works |
| subagent dispatch | model called `subagent` `{"agent":"loom-code:reviewer",…}` | child session `parentID` = root session, `agent: loom-code:reviewer`, replied `NO-STATION / DONE` | works |
| 5a session-start context in root session | root prompt asked the model to quote the `Station order` line | quoted `Station order: capture-intent → write-spec → write-plan → build → closing-review → ship; maintain on alerts.` | works |
| 5b child session detected | `session.get` on child; child asked for the `Station order` line; transcript dir listing | child record carries `"parentID":"ses_…"`; child answered `NO-STATION`; no transcript file for the child id (prompt hook skipped it) | works |
| 5c `process.cwd()` = project dir | `lsof -d cwd` on server processes; push check through each shape | dedicated server: cwd `<S>/proj`. **Service: cwd `/Users/kouko` (home)**, not the project | **defect** (service shape) |
| 5d push hook reaches `git push --dry-run` | root prompt: `shell` `git push --dry-run origin HEAD` | dedicated: model saw `loom: change not identified (no intent for this branch); publishing anyway.` **Service: `loom: publication hook failed (/Users/kouko is not inside a git work tree.); allowing.`** | works on dedicated; **defect** on service (wrong cwd) |
| 5e folder-structure note on nested write | `skills/x/SKILL.md` present; model called `write` then `edit` on `skills/x/a/b/c.md` | no note on either result. Observed inputs: write `{"path":"skills/x/a/b/c.md","content":"hi"}`, edit `{"oldString":"hi","newString":"bye","path":"skills/x/a/b/c.md"}`: the key is `path` (relative), not `filePath` | **defect** |
| 5f execute-tool-hook-result-recorded | model listed its tools, then was asked to call `shell` inside `execute` | `execute` exists in 2.0.18 (tool list: `edit, glob, grep, question, read, shell, skill, subagent, webfetch, websearch, write, execute`). Inside `execute`, `tools` holds only the `browser` and `opencode` namespaces; `tools.shell(...)` → `Unknown tool 'shell'`, `tools.read(...)` → `Unknown tool 'read'` | works: the mapped tools (shell, write, edit, patch, skill) cannot be called from `execute`, so it cannot bypass them |
| 5g expert-mode-command-text-reaches-prompt-hook | `session.command` `{"name":"loom-code:expert-mode","text":"W3CMD …"}` | prompt-hook transcript line starts with `/loom-code:expert-mode W3CMD …` followed by the skill body (`Base directory for this skill: …/skills/expert-mode`); the model replied `ACK` | works |
| 5g via `opencode run "/loom-code:expert-mode …"` | `run` with the slash text as the message | the text reached the prompt hook raw, but the command callback did **not** run (user message was the literal text, no skill body attached) | `run` does not resolve slash commands; use the TUI or `session.command` |
| 5h language reminder | Traditional Chinese root prompt, then `skill` call | skill result ends with `對使用者的敘述一律使用會話語言（繁體中文）；機器面 artifact（brief/verdict/commit）維持原語言。` | works |

## Defects found (to fix as separate test-first tasks)

1. **Hooks see the wrong directory under the background service.** The loader
   uses `process.cwd()` for `cwd` in every payload and as the handlers' working
   directory. The managed service process runs from the user's home directory,
   so the push reminder fails (quoted above), and every `cwd`-based check
   (selection-guard Bash cwd, session-start, card, folder validator's repo
   check) runs against `$HOME`. The session record has the right value:
   ```
   {"data":{"id":"ses_f13414797ffe…","projectID":"ee387cd9…",…,
    "location":{"directory":"<S>/proj"}}}
   ```
   `ctx.session.get` already returns it, so the per-session directory is
   `(r.data ?? r).location.directory`.
2. **`write`/`edit` argument key is `path`, not `filePath`, and it is
   relative.** `TOOLS.write`/`TOOLS.edit` read `i.filePath`, which is
   `undefined` on 2.0.18, so the Claude payload has no `file_path`:
   the folder-structure validator exits 0, and the selection-record guard
   gets no file target for Write/Edit (inferred from the payload shape and the
   loader code; I did not write into the store). The validator also needs an
   absolute path (it greps `/skills/`), so the fix must resolve `path`
   against the session directory from defect 1. `patch` input shape was not
   observed.
3. **PreToolUse note not in the stored tool output.** For `shell`, the push
   note reached the model (it quoted it), but the event's `state.output` string
   does not contain it (the loader pushes it into `result.content`). The
   skill reminder does appear in `state.output`. TUI rendering was not checked.
   Minor; listed for W4-01 wording only.

## Not run

- **TUI "Install plugin" dialog**: could not be triggered through tmux (see the
  table). The dialog does list installed plugins. A human should try `shift+I`
  in the Plugins dialog in a real terminal before W4-01 describes it.
- **Real `github:` fetch**: out of scope until after publication.
- **5a–5b, 5e, 5g, 5h on the service shape**: these ran on the dedicated server
  only. 5c and 5d were repeated on the service.

## Log excerpts

Plugin load (dedicated server, trimmed):
```
level=INFO msg="loading plugin" id=git+file:///Users/kouko/GitHub/loom-plugins#engineering/2026-09-29-opencode-v2-compatibility::path:loom-code entrypoint=file://<S>/xdg/cache/opencode/npm/git-loom-plugins-61f9046f52ec/1790677355325/node_modules/loom-code/index.js
level=INFO msg="loading plugin" id=git+file:///…::path:loom-design entrypoint=file://<S>/xdg/cache/opencode/npm/git-loom-plugins-f0278914e631/…/node_modules/loom-design/index.js
level=INFO msg="loading plugin" id=git+file:///…::path:loom-workflow entrypoint=file://<S>/xdg/cache/opencode/npm/git-loom-plugins-9b5fb637fc7d/…/node_modules/loom-workflow/index.js
```

`plugin.list` API (non-builtin entries):
```
{"id":"loom-code","source":{"type":"package","target":"git+file:///Users/kouko/GitHub/loom-plugins#engineering/2026-09-29-opencode-v2-compatibility::path:loom-code","version":"33ec1d90e36aff6b7cc366ab0602fa3118ce3c5c"},"features":{"server":true},"state":{"status":"active"}}
```

Service port collision (first isolated `plugin list`, before the port was changed):
```
level=ERROR message="cli process failed" cause="… Managed service port 49374 on 127.0.0.1 is already in use by another process. Configure another port with `opencode service set port <port>` …"
```
A second OpenCode config on the same machine needs `opencode service set port <port>`;
without it `plugin list` hangs.

Process working directories:
```
opencode serve --hostname 127.0.0.1 --port 4998 …   cwd=<S>/proj
opencode serve --service  (isolated, port 4997)     cwd=/Users/kouko
```

Child session record (5b):
```
{"data":{"id":"ses_f13412b1effe…","parentID":"ses_f13414797ffe…","agent":"loom-code:reviewer",…,"title":"probe","location":{"directory":"<S>/proj"}}}
```

Inside `execute` (5f), model-written code and results:
```
return await tools.shell({ command: "git push --dry-run origin HEAD" });   -> Unknown tool 'shell'. Use search to find available tools.
return await tools.read({ path: "." });                                     -> Unknown tool 'read'. Did you mean tools.opencode.read_mcp_resource?
```

Other observation: the server also watches `/Users/kouko/.claude/skills` and
offers those skills (17 non-loom skills appeared, including OpenCode's
built-in `opencode` skill). This is OpenCode's own
Claude-compatibility behaviour, not something the loom plugins do.
