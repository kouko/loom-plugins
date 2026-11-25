# Agent hook blocks common spellings that commit, merge or push to main — acceptance test evidence

Tried on 2026-11-25, in a clean copy of the project at 5ece56d25 (first run at 6c2b92868; sections 1–6 below record that first run, the re-run section at the end records 5ece56d25).

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

## Re-run on 2026-11-25, at 5ece56d25

Fix range `1f932a0a0..5ece56d25` (8e132ffa9 heredoc bodies / `$( )` / backtick text not judged, redirect tokens dropped; e6775e3bb refspecs read after `git push --repo`; 5ece56d25 comments + CHANGELOG). It changes `loom-code/scripts/loom_checker/command_handlers/push.py`, the guard every host and every row goes through, so all six rows were re-tested in full; none carried over.

Fresh clean copy `git worktree add --detach <scratch>/clean 5ece56d25`, same fresh runtime cache, fresh throwaway repos per host run (header `hooks-dir: [] core.hooksPath: (unset)` on all five runs). Case list = the first-run list plus:

| id | command | cwd | expect |
|---|---|---|---|
| 1c | `cd {main} && git commit --allow-empty -m "$(cat <<'EOF'⏎x⏎EOF⏎)"` | feature | refuse |
| 3d | `git push --repo origin main` | feature | refuse |
| 3e | `git push --repo=origin HEAD:main` | feature | refuse |
| 4h-pass | `git commit --allow-empty -m "$(cat <<'EOF'⏎fix: guard⏎⏎git push origin HEAD:main⏎EOF⏎)"` | feature | pass, and commit lands on feature |
| 4i-pass | `gh pr create --title t --body "$(cat <<'EOF'⏎## Test⏎git push origin HEAD:main⏎cd ../main && git commit -m x⏎EOF⏎)"` | feature | pass (hook decision only; not executed — outward-facing) |
| 4j-pass | `git push origin HEAD:feature3 2>&1` | feature | pass |

(⏎ = a real newline in the command text.)

Per-host verdicts (x2 = exit 2 refused, x0 = exit 0 allowed):
```
claude:    1a 1b 1c 2a 2b 3a 3b 3c 3d 3e 4a-old 4b-old 4c-old = x2 ; 4d 4e 4f 4g 4h 4i 4j = x0
optout:    every case x0; local main moved on 1a,1b,1c,2a,4a-old; remote main 28ae259->4126405 on 3a
opencode:  1a..3e, 4a-old..4c-old = refused (message as above); 4d..4j = allowed
agy:       1a..3e, 4a-old..4c-old = deny (reason = message); 4d..4j = allow
codex-cmd: 1a..3e, 4a-old..4c-old = x2; 4d..4j = x0
```
Every refusal on every host carried `loom: direct git merge, commit, or push on main/master is blocked. Next: preserve your work on a feature branch or worktree and open its PR.` With protection on, local and remote `main` never moved on any host. Sample lines (Claude Code):
```
[1c] hook exit=2 -> refused   local main ae8ff30->ae8ff30
[3d] hook exit=2 -> refused   remote main ae8ff30->ae8ff30
[4h-pass] hook exit=0 -> allowed   local main ae8ff30->ae8ff30; feature 35c5541->41055a7 (commit landed on feature)
[4i-pass] hook exit=0 -> allowed; msg='loom: change not identified (no intent for this branch); proceeding.'
```

- 1: re-tested — 1a, 1b, 1c on Claude Code (and every other host); all refused, `main` unchanged.
- 2: re-tested — 2a, 2b on every host; all refused, `main` unchanged.
- 3: re-tested — 3a–3e on every host; all refused, remote `main` unchanged.
- 4: re-tested — 4a–4c refused; 4d–4j allowed (4h committed on feature; 4i hook decision only); opt-out repo allowed and ran every case.
- 5: re-tested — every repo of every run had empty hook folders and no `core.hooksPath`.
- 6: re-tested — OpenCode loader and Antigravity adapter gave the same verdicts as Claude Code on the full list; Codex hook command matched; live Codex session still not run (not verified).
- Criterion tests at 5ece56d25: `python3 -m pytest -q -p no:cacheprovider loom-code/tests/test_main_branch_hook.py loom-code/tests/test_agy_adapter.py loom-code/tests/test_opencode_loader.py` → `118 passed in 18.54s`. Full suite left to finalize-review: `python3 scripts/run_package_tests.py --loom-family`.
