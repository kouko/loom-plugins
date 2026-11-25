# Agent hook blocks common spellings that commit, merge or push to main — acceptance test evidence

Tried on 2026-11-25, in a clean copy of the project at 6c2b92868.

## Setup

- Clean copy: `git worktree add --detach <scratch>/clean 6c2b92868` (never a tree anyone worked in). A second detached copy at the base `35c9efd15` served as the before-the-change baseline.
- Project setup: `XDG_CACHE_HOME=<scratch>/cache loom-code/scripts/loom-python --repair --help` provisioned the checker runtime from nothing (`python-3.11-pyyaml-6.0.2-v1`), exit 0. Every later run used that fresh cache and `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID`.
- Throwaway repos, rebuilt for every host run (`<R>` below):
  - `<R>/remote.git` bare remote, `<R>/main` checkout on `main` (one initial commit, pushed), `<R>/feature` linked worktree on branch `feature` with one extra commit, plus branch `other`.
  - Every file under `.git/hooks` (main) and `hooks/` (remote) deleted — not even samples; `git config --get core.hooksPath` is unset (global and system also unset). Driver prints `hooks-dir: [] core.hooksPath: (unset)`.
- Driver (scratch, not committed) sends each command the way each host does, with cwd = `<R>/feature` unless marked `cwd=main`:
  - Claude Code: runs the `PreToolUse`/`Bash` command string from `loom-code/hooks/hooks.json` via `sh -c`, `CLAUDE_PLUGIN_ROOT=<clean>/loom-code`, stdin `{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":…},"cwd":…}`. Exit 2 = refused.
  - Codex hook command: same, using `loom-code/hooks/hooks-codex.json` with `PLUGIN_ROOT`.
  - OpenCode: `node` imports `<clean>/loom-code/index.js` (which loads `opencode/loader.js`) on a stub plugin context, fires `execute.before` with `{"tool":"shell","input":{"command":…}}`, session directory = feature worktree. A thrown error = refused.
  - Antigravity: `python3 <clean>/loom-code/hooks/agy_adapter.py push-gate` with a `run_command` payload (`workspacePaths=[<R>/feature]`, `Cwd: "."`), cwd = plugin root. `decision` read from stdout JSON.
  - When a hook allows, the driver then actually runs the command, so a slip would show as a moved `main`. Local and remote `main` SHAs are recorded before/after every command.
- Commands (`{main}` = `<R>/main`):

| id | command | cwd |
|---|---|---|
| 1a | `cd {main} && git commit --allow-empty -m x` | feature |
| 1b | `cd {main} && git merge feature` | feature |
| 2a | `git -C {main} commit --allow-empty -m x` | feature |
| 2b | `git -C {main} merge feature` | feature |
| 3a | `git push origin HEAD:main` | feature |
| 3b | `git push origin HEAD:master` | feature |
| 3c | `git push origin feature:refs/heads/main` | feature |
| 4a-old | `git commit --allow-empty -m x` | main |
| 4b-old | `git merge feature` | main |
| 4c-old | `git push origin main` | main |
| 4d-pass | `git commit --allow-empty -m more` | feature |
| 4e-pass | `git merge other` | feature |
| 4f-pass | `git push origin feature` | feature |
| 4g-pass | `git push origin HEAD:feature2` | feature |

Refusal message seen on every refusal, every host:
`loom: direct git merge, commit, or push on main/master is blocked. Next: preserve your work on a feature branch or worktree and open its PR.`

## 1. An agent command `cd <main checkout> && git commit …` (and the same with `git merge`) is refused with the existing "direct git merge, commit, or push on main/master is blocked" message, and nothing is committed.
- How I tried it: cases 1a, 1b through the Claude Code hook command; same cases against the base `35c9efd15`.
- What came back (6c2b92868):
  ```
  [1a] hook exit=2 -> refused; msg='loom: direct git merge, commit, or push on main/master is blocked. …'
      local main 3d38941->3d38941; remote main 3d38941->3d38941
  [1b] hook exit=2 -> refused; msg=<same>
      local main 3d38941->3d38941; remote main 3d38941->3d38941
  ```
  Baseline (35c9efd15): `[1a] hook exit=0`, `[1b] hook exit=0` — the command then ran.
- Evidence: captured driver output above; HEAD of `main` unchanged. Criterion tests: `python3 -m pytest -q -p no:cacheprovider loom-code/tests/test_main_branch_hook.py loom-code/tests/test_agy_adapter.py loom-code/tests/test_opencode_loader.py` → `110 passed in 16.50s` (run in the clean copy). Full suite left to finalize-review: `python3 scripts/run_package_tests.py --loom-family`.

## 2. An agent command `git -C <main checkout> commit …` or `git -C <main checkout> merge …` is refused the same way.
- How I tried it: cases 2a, 2b, Claude Code hook command; baseline at 35c9efd15.
- What came back: `[2a] hook exit=2 -> refused`, `[2b] hook exit=2 -> refused`, same message; `local main 3d38941->3d38941`. Baseline: `[2a] hook exit=0`, `[2b] hook exit=0`.
- Evidence: driver output; same criterion test run (110 passed).

## 3. An agent command run on a feature branch that pushes to `main` or `master` on a remote (for example `git push origin HEAD:main`) is refused the same way.
- How I tried it: cases 3a, 3b, 3c from the feature worktree, Claude Code hook command; baseline at 35c9efd15.
- What came back: `[3a] hook exit=2`, `[3b] hook exit=2`, `[3c] hook exit=2`, same message; `remote main 3d38941->3d38941`. Baseline: all three `hook exit=0`.
- Evidence: driver output; same criterion test run (110 passed).

## 4. The commands refused today are still refused, and these still pass: commit, merge and push on a feature branch; a push from a feature branch to a feature branch; any command in a repository with `loom.protectMain` set to `false`.
- How I tried it: cases 4a–4g with the Claude Code hook command; then the full case list (1a–4g) in a fresh repo set with `git config loom.protectMain false` on `<R>/main`.
- What came back (protection on):
  ```
  [4a-old] hook exit=2 -> refused   [4b-old] hook exit=2 -> refused   [4c-old] hook exit=2 -> refused
  [4d-pass] hook exit=0 -> allowed  [4e-pass] hook exit=0 -> allowed
  [4f-pass] hook exit=0 -> allowed; msg='loom: change not identified (no intent for this branch); proceeding.' (push reminder, allow)
  [4g-pass] hook exit=0 -> allowed; same reminder
  ```
  Opt-out (`loom.protectMain false`): every case 1a–4g `hook exit=0 -> allowed`, and the commands ran: `[1a] local main 711f5cf->e4123eb`, `[1b] e4123eb->b72817a`, `[2a] b72817a->da34751`, `[3a] remote main 711f5cf->37ecebb`, `[4a-old] da34751->77aba98`, `[4c-old] remote main 37ecebb->77aba98`.
- Evidence: driver output; same criterion test run (110 passed).

## 5. All of the above hold in a repository with no native git hooks installed.
- How I tried it: every run above used repos whose hook directories were emptied and with `core.hooksPath` unset everywhere.
- What came back: driver header `hooks-dir: [] core.hooksPath: (unset)` on every run; results of 1–4 as above.
- Evidence: driver header line; `git config --global --get core.hooksPath` and `--system` both returned nothing.

## 6. The three commands from items 1–3, sent through the OpenCode hook loader and through the Antigravity hook adapter, are refused there too. Codex is reported as not verified when its CLI is unavailable in the test environment.
- How I tried it: the full case list through the OpenCode loader (node, stub context) and the Antigravity adapter (`push-gate`); also through the Codex hook command string.
- What came back:
  - OpenCode: 1a, 1b, 2a, 2b, 3a, 3b, 3c, 4a–4c `refused` with the message; 4d–4g `allowed`; `local main 63bc73d->63bc73d` throughout.
  - Antigravity: 1a–3c and 4a–4c `decision=deny`, reason = the message; 4d–4g `decision=allow` (4f/4g carry the push reminder); `local main ef2a299->ef2a299` throughout.
  - Codex hook command: 1a–3c and 4a–4c `hook exit=2` with the message; 4d–4g `hook exit=0`.
  - Codex live: `codex-cli 0.172.0` is installed, but no Codex session was run with the plugin installed, so the in-Codex path is not verified (installing would change the user's Codex configuration).
- Evidence: driver output; criterion tests `test_agy_adapter.py::test_main_spellings_from_feature_branch` and `test_opencode_loader.py::test_main_spellings_refused_from_feature_session` within the 110 passed.
