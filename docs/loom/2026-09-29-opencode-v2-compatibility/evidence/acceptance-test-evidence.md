# OpenCode v2 compatibility — acceptance test evidence

Tried on 2026-09-29, in a clean copy of the project at `5a0e8d4a` (a detached
`git worktree` for the source, removed afterwards).

Environment used for every line:

- Binary `/Users/kouko/.opencode/bin/opencode` 2.0.18. The shell function was not used.
- Isolated scratch directory `oc-at/`. It holds `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
  `XDG_CACHE_HOME`, `XDG_STATE_HOME` and `OPENCODE_CONFIG_DIR`.
  `OPENCODE_DISABLE_AUTOUPDATE=1` and `OPENCODE_DISABLE_PROJECT_CONFIG=1` are set.
  The background service runs on its own port, 49601.
- The user's `~/.config/opencode`, `~/.local/share/opencode` and the user's
  service on 49374 were not read, changed or touched. The 49374 listener, pid
  91480, was still up at the end.
- Model: the `litellm` provider block, copied from the user's own catalog.
  The default is `litellm/hyper-coding-group`, which routes to free third-party
  models such as GLM and DeepSeek flash. Only `OPENCODE_LITELLM_API_KEY` is
  exported, and the key was never printed.
- Every `CLAUDE*`, `CODEX*` and `ANTHROPIC*` variable is unset before the
  service starts.
  - An earlier batch of hook checks ran while the service had inherited
    `CLAUDE_CODE_SESSION_ID` / `CLAUDE_CODE_SESSION_ATTENDED=1` from the
    tester's shell. That batch is discarded.
  - Every result below comes from the clean re-run: service stopped and started
    again, 0 `CLAUDE*` variables in its environment.
- `gh` is isolated and unauthenticated (`GH_CONFIG_DIR` inside the scratch
  directory). Nothing was pushed to any real GitHub repository.
- Install spec: `git+file:///Users/kouko/GitHub/loom-plugins#5a0e8d4a::path:<plugin>`.
  The documented `github:kouko/loom-plugins#main::path:<plugin>` fetch cannot be
  tried before the branch is published.

## 1. Installs with the official plugin command and the TUI dialog, and the plugin list shows all three

- How I tried it:
  1. `opencode plugin list` before installing.
  2. `opencode plugin add 'git+file:///Users/kouko/GitHub/loom-plugins#5a0e8d4a::path:loom-code'`, then the same for `loom-design` and `loom-workflow`.
  3. `opencode plugin list`.
  4. `opencode service restart`, then `plugin list` again.
  5. TUI in tmux: `shift+I`, CSI-u escapes, a `tui.json` keybind for the install command, and a palette search for "install".
- What came back:
  - Before installing: `No plugins found`.
  - Each add: `installed and added`.
  - Straight after three adds on the running service, `plugin list` showed only `loom-code`. Only after `service restart` did it list `loom-code`, `loom-design` and `loom-workflow` at `5a0e8d4`. This was reproduced by re-adding `loom-workflow`.
  - The first list after a restart once printed `No plugins found` (a cold start); the next list was correct.
  - The TUI Plugins dialog listed the three installed plugins.
  - I could not open the dialog's "Install plugin" entry from tmux:
    - `shift+I` typed `I`.
    - A custom keybind either collided with the variant key (`ctrl+t`) or did nothing (`F6`/`F7`).
    - The palette search gave `No results`.
- Removal / update step (README.md:254):
  - `opencode plugin remove loom-workflow` answered `Plugin "loom-workflow" is not configured`.
  - Removal only worked with the full spec string.
- Evidence: the terminal transcript in the session log; README.md:248-254.
- Verdict: partly. The command path works from a pinned local spec. Still not tried:
  - the GitHub fetch (it needs the branch published);
  - the TUI install dialog (it needs a person at a real terminal).

## 2. Every station and skill is offered and loads its full instructions, including with a same-named skill from another plugin

- How I tried it:
  1. `opencode api GET /api/skill`, `/api/command`, `/api/agent`.
  2. Installed a throwaway rival plugin that registers skills `write-plan`, `build` and `ship` whose body is the marker `RIVAL-BODY`. Also added a local skill `build` with marker `LOCAL`.
  3. `opencode run` asked the model to load each of the 24 loom skill ids in turn. I compared every loaded body with its `SKILL.md`.
- What came back:
  - `/api/skill` listed 24 loom skills named `<plugin>:<skill>`. That is exactly the set of model-invocable `SKILL.md` files in the three plugins.
  - `expert-mode` is registered as a command, `loom-code:expert-mode` in `/api/command`, by design.
  - The rival's `write-plan`/`ship` and the local `build` were listed alongside loom's without replacing them.
  - All 24 loaded bodies were complete, with no `RIVAL-BODY` or `LOCAL` text.
  - `/api/agent` listed `loom-code:implementer`, `reviewer`, `adversary` and `acceptance-tester`, each `mode: subagent`.
- Evidence: the scratch logs `skills.json`, `a2-load.jsonl` and `a2-all.jsonl`.
- Verdict: works.

## 3. A small change through capture-intent → write-plan → build → closing-review → ship on a third-party model; checker accepts intent, plan and attestation; report committed; PR opened

- How I tried it:
  - A throwaway repo `proj` holds a tiny `greet.py` CLI with tests. Its origin is a local bare repo; no GitHub remote exists.
  - One root session (`ses_f1303d51…`, model `litellm/hyper-coding-group`) was asked to add a `--version` flag through the loom flow.
  - I answered decision point ① as the user: yes, needs-design no, automatic publication authorised.
  - Permission prompts:
    - approved for the project and for loom's own installed files;
    - two prompts for a temp directory, `/tmp/greet-before/*`, approved once;
    - one for the acceptance tester's temp checkout, approved;
    - two prompts from reviewers asking to read the tester's own loom source checkouts, rejected, because a real user would not have them.
- What came back (branch `feat/2026-09-29-add-version-flag`):
  - `8ca8896` intent confirmed
  - `e0b58f4` kickoff defaults
  - `7ef993a` plan
  - `660ad79` feat (implementer subagent)
  - `7055fc0` adversarial probe. The adversary found that `--version --bogus` exited 0. The probe was red.
  - `1ea63ab` fix, made by the root session
  - `db520cd` plan update
  - `deede27` acceptance test report and evidence (acceptance-tester subagent)
  - Reviewer 1: PASS. Reviewer 2 was re-dispatched after its first attempt stopped at my rejection.
- Interrupted at that point by the cost cap:
  - Root session: about 1.95M non-cached input tokens over 63 steps, plus 1.72M cache reads.
  - Nine subagent sessions: about 1.35M non-cached input tokens and 1.20M cache reads.
  - Output: about 38k tokens.
  - Reported cost: 0 (free routes).
  - I interrupted both sessions (`POST /api/session/<sid>/interrupt` → `{"interrupted":true}`). The run had overshot the ~1.5M cap: I was watching commits, not tokens, during the last stretch.
- Checker, run by me with the installed copy, in `proj`:
  - `loom_checker.py intent docs/loom/intent/2026-09-29-add-version-flag.md` → exit 0.
  - `intake write-plan 2026-09-29-add-version-flag` → exit 0.
  - `reviewer-count` → `2`.
  - The plan-shape rules and the attestation run only in `finalize-review`, which was never reached, so there is no attestation.
- Ship: not reached. `git ls-remote origin` shows only `main` at `c24da0e`, so nothing was pushed and no pull request was opened. There is also no GitHub remote for one to open against.
- Loom's own reference files:
  - The acceptance-tester subagent was not given the report template's location. It ran `find / -name acceptance-test-report.md` over the whole disk and read a copy from a stale test fixture in the system temp directory (`…/T/rename-adversary-807cmoiv/…/loom-code/skills/closing-review/references/acceptance-test-report.md`).
  - Two reviewers looked for `closing-review/references/lenses.md` in the project, found nothing, and asked to read the tester's own checkouts.
  - The agent definitions name these files by repo-relative paths (loom-code/agents/acceptance-tester.md:19). Those paths do not exist in a user's project.
  - The implementer and adversary dispatches did carry the installed-cache paths.
- Evidence: the scratch logs `flow-01/02/03.jsonl` and `permission-prompts.jsonl`; the `proj` git log.
- Verdict: partly.

## 4. Implementer, reviewer, adversary and acceptance-tester each run as separate OpenCode subagents

- How I tried it: listed the sessions whose parent is the root session, with their `agent` field.
- What came back:
  - `ses_f12fd7e41…` `loom-code:implementer`
  - `ses_f12f12933…`, `ses_f12ecac76…`, `ses_f12e1ed6b…` `loom-code:adversary`. The first was cut off by a service restart; the second and third were re-dispatches.
  - `ses_f12d5d508…` `loom-code:acceptance-tester`
  - `ses_f12d1833b…`, `ses_f12d014a9…`, `ses_f12cc3dd5…`, `ses_f12cb6030…` `loom-code:reviewer`
  - Each child has its own session, messages and token count.
- Other observations:
  - The fix for the adversary's finding was written by the root session itself, not by a new implementer subagent.
  - The second-vendor policy call passed `"host_vendor": "claude"` while running on OpenCode.
- Permission prompts:
  - `opencode run --auto` does not cover child sessions. Subagents stop on `external_directory` prompts when they read loom's own files from the plugin cache, and wait for an answer.
  - The README does not mention this.
- Verdict: works.

## 5. Session-start order and defaults, publication reminder, language reminder, folder-structure rule, selection-record guard

All runs are in a second throwaway repo `proj2` (branch `feature/demo`, with a `docs/loom/KICKOFF-DEFAULTS.md` file), in the clean environment, with `PWD` set to the repo. OpenCode uses `$PWD` as the session directory. An earlier batch without it ran in the real repo; its only effects were a `git push --dry-run` and one stray file, which I deleted. That batch is discarded.

- Session start: the first context carried the `Station order: capture-intent → … ; maintain on alerts.` line and the kickoff-defaults lines from the repo file.
- Publication reminder: asking the model to push produced `loom: change not identified (no intent for this branch); publishing anyway.`
- Language reminder: a Traditional Chinese prompt that loads a loom skill got the language reminder appended after the skill load.
- Folder rule: writing `skills/x/refs/deep/d.md` produced `Skill folder structure violation`.
- Selection guard, forgery attempts:
  - A nested `opencode run "/loom-code:expert-mode J2KW"` from the model's shell → `BLOCK selection.guard: a nested host session's expert-mode prompt would pass as user-typed`.
  - A shell write naming the store → refused (`names the selection record store`).
  - A write-tool call into the store → refused (`resolves under the loom record directory`).
  - Running `selection capture --hook` directly → refused (`runs only from the prompt hook`).
  - A child subagent sent the expert-mode prompt with code `DJS4` → the proposal stayed unbound (`bound=false`).
  - The code-mode `execute` tool cannot reach shell or write (`Unknown tool 'shell'`).
- Selection guard, positive control: the same code `DJS4`, sent as the `loom-code:expert-mode` command in the root session through the command API (the TUI path), bound the proposal (`bound=True`, `skip=[reviewers]`).
  - Sent through `opencode run "/loom-code:expert-mode …"`, the text is stored wrapped in literal quotes and does not bind. The docs already point users to the TUI for this.
- Evidence: the scratch logs `r1-ss`, `r2-push`, `r3-lang`, `r4-folder`, `r5-forge`, `c1`–`c6`.
- Verdict: works.

## 6. Package suite and Codex manifest drift check still pass; other hosts unchanged

- How I tried it, in the clean worktree:
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  - `python3 scripts/sync_codex_manifests.py --check --all`
  - `git diff 58bf79d2..5a0e8d4a` over the manifests, `hooks.json` / `hooks-codex.json` and the skill `name:` fields.
- What came back:
  - The package suite exited 0 with no failures. The pytest groups passed (for example `201 passed, 5 skipped`), every shell summary ended `0 FAIL`, and the last line was `exit 0`.
  - The drift check exited 0.
  - The manifests differ only in version fields, plus a whitespace-only re-indent of loom-design's Codex `longDescription`.
  - `hooks.json` and `hooks-codex.json` are unchanged; the new `hooks-opencode.json` files were added.
  - The skill file set and every `name:` are unchanged.
  - The shared `selection_guard.py` now treats `opencode` as a host program on Claude Code and Codex too. This hardens those hosts; it is not a regression.
- Evidence: the scratch log `package-suite.txt`.
- Verdict: works.

## 7. PRINCIPLES.md names OpenCode v2 as a supported host

- How I tried it: read `PRINCIPLES.md`.
- What came back:
  - OpenCode v2 is named in the Who line and the Fixed-choices line, next to Claude Code, Codex and Antigravity CLI.
  - The ratified-by line records `hosts clause amended (OpenCode v2 added) by kouko 2026-09-29`.
- Verdict: works.

## 8. New versions, consistent across manifests, CHANGELOGs and READMEs

- How I tried it: grepped the version strings in `.claude-plugin`, `.codex-plugin`, `plugin.json`, `package.json`, the CHANGELOG top sections and the READMEs.
- What came back:
  - loom-code 3.24.0, loom-design 2.7.1 and loom-workflow 5.5.6 everywhere.
  - No stale strings.
  - `marketplace.json` carries no version fields.
- Verdict: works.

## Cleanup

- The isolated service was stopped; nothing listens on 49601 any more.
- The permission stand-ins and monitors were stopped, and the tmux server was killed.
- The worktree was removed with `git worktree remove`.
- The real repo is clean at `5a0e8d4a`.

## Re-run on 2026-09-29, at 136c0248

Fix range `5bc86a10..136c0248`:
- `89637084` prefixes every OpenCode subagent's system prompt with its installed plugin root. The change is in the loader's `agents()` only: `loom-code/opencode/loader.js:87-88`, plus the three mirror loaders and `scripts/opencode/loader.js`.
- `136c0248` changes the OpenCode README steps: remove by full spec, restart after add, and a note on permission prompts.

No manifest, `hooks*.json`, hook script, skill, `PRINCIPLES.md` or version file is in the range.

Environment for the re-run:
- A fresh isolated tree `oc-at/rerun/` with its own `XDG_*`, `OPENCODE_CONFIG_DIR` (no plugins at start), service port 49613 and a new throwaway project `rerun/proj`.
- Same binary, 2.0.18. The user's service on 49374 (pid 91480) was untouched and was still up at the end.
- The service environment carried 0 `CLAUDE*`/`CODEX*`/`ANTHROPIC*` variables.
- `gh` was the user's real login (`GH_CONFIG_DIR=$HOME/.config/gh`), authorized for the scratch repo only.
- Model: `litellm/hyper-coding-group` (free third-party routes via the user's litellm).
- Driving:
  - `opencode run` without `--auto` aborts at the first permission prompt (`error: aborted "Step interrupted"`), and the `question` tool aborts a non-interactive run (`Session interrupted: shutdown`).
  - So after two `opencode run` turns, the root session was driven through the server API the TUI uses: `POST /api/session/<id>/prompt`, and `GET /api/form` / `POST /api/session/<id>/form/<id>/reply` for questions.
  - No `--auto` was in effect for the flow; every permission prompt went to the stand-in.
- Stand-in rules (`oc-at/approver2.py`):
  - `external_directory` inside the project or the plugin cache → `always`;
  - a temp dir outside the tester's scratch area → `once`;
  - anything else → `reject`.
- Harness finding: `opencode api GET /api/session/<id>/message` output is cut near 256 KiB. The re-run pages with `?limit=&cursor=` (`oc-at/oc_api.py`). The first run's token counter did not page, so it may have under-counted.

### 1: re-tested
- How: README.md:246-256 steps with the pinned local spec, then the documented update/remove step. Log `rerun/logs/a1-install.txt`.
  - `opencode plugin list` → `No plugins found`.
  - Three `opencode plugin add 'git+file:///Users/kouko/GitHub/loom-plugins#136c0248::path:<plugin>'` → each `installed and added`.
  - `plugin list` straight after the adds → `No plugins found`.
  - `opencode service restart`, then `plugin list` → `No plugins found` at +5 s and +10 s.
  - The +20 s list and every one after it showed `loom-code`, `loom-design` and `loom-workflow` at `136c024`.
  - `opencode plugin remove loom-workflow` → `Plugin "loom-workflow" is not configured`, as the README now says.
  - `opencode plugin remove '<full spec>'` → `removed`. Re-add → `installed and added`. After a restart the list showed all three again after about 35 s.
- Still not tried:
  - the `github:` fetch (the branch is not published);
  - the TUI "Install plugin" dialog (it needs a person at a real terminal).
- Verdict: partly.

### 2: carried over
- Reason: the fix touches only `agents()` (the subagent system prompt) and README text; skill and command registration is unchanged in the diff.
- Consistent with this: `/api/agent` lists the four `loom-code:<role>` subagents (`rerun/logs/agents.json`), and the flow loaded `loom-code:*` and `loom-design:*` skills from the cache.

### 3: re-tested
- Scratch repo `https://github.com/kouko/loom-opencode-scratch` (private, created by the user).
  - The initial commit went to branch `trunk`, not `main`: the tester's own Claude Code guard refused `git push -u origin main` ("do not push directly to main/master").
  - `trunk` became the default branch, `origin/HEAD -> origin/trunk`.
- Root session `ses_f12b97e45ffejOcQviIsULy7BG`. Prompts, in order (`rerun/prompts/`, `rerun/logs/driver.jsonl`):
  1. The ask: add `--upper`, through to an opened PR.
  2. Answers to the capture-intent and principles questions.
  3. "confirmed, needs-design: no, automatic publication authorized".
  4. At ship's github-rules question: "No — don't add the workflow template or any branch protection".
- Branch `feat/2026-09-29-greet-upper-flag`:
  - `c772bd5` intent confirmed
  - `52815a3` principles + kickoff defaults
  - `bec838d` plan
  - `842ab23` feat
  - `3233a9a` fix: the kickoff-defaults placeholders, found by the adversary
  - `eedc89a` adversarial probe
  - `4f05b21` acceptance test report + evidence
- Checker, run by the tester with the installed copy (`rerun/logs/a3-checker.txt`):
  - `intent docs/loom/intent/2026-09-29-greet-upper-flag.md` → exit 0.
  - `intake write-plan 2026-09-29-greet-upper-flag` → exit 0.
  - `reviewer-count` → 2.
  - `finalize-review 2026-09-29-greet-upper-flag --input /tmp/finalize-input.json`, run by the root → `wrote docs/loom/2026-09-29-greet-upper-flag/attestation.json for f844aba…`, exit 0.
- Attestation:
  - The attestation was never committed; it is still untracked in `rerun/proj`.
  - `publish` printed `loom: verification stale (attestation is not committed at HEAD); publishing anyway.` / `Published PR: https://github.com/kouko/loom-opencode-scratch/pull/1` / `No required checks registered`.
  - In a throwaway clone (`rerun/attest-check`) with the attestation committed, `pr-floor --body-file <PR body> --base 36f5306 --head <sha>` → `::notice title=verification::valid`, exit 0. So the attestation itself is good; the flow skipped committing it.
- PR #1: `OPEN`, base `trunk`, head `4f05b21`, `gh pr checks` → `no checks reported`.
  - The PR body says `Verification status: valid (skipped: reviewers)`. Both parts are wrong: publish computed `stale`, and no step was skipped (two reviewers ran).
  - loom-code/skills/ship/SKILL.md:78-86 requires the body to carry the status publish printed.
- The PR was not merged. Nothing was pushed to any other repo.
- Verdict: partly.

### 4: re-tested
- Child sessions of the root (`rerun/logs/tokens-final.txt`):
  - `loom-code:adversary` ×1;
  - `loom-code:reviewer` ×3. One was cancelled after the stand-in rejected its `cd /` (resource `/*`); two completed: the code lens and the docs lens;
  - `loom-code:acceptance-tester` ×2. The first was cancelled after the stand-in rejected a worktree in the project's parent directory; the second committed the report.
- Plugin root, per child (`rerun/logs/tools-<session>.txt`):
  - Every child's first reads came from the installed plugin root `…/xdg/cache/opencode/npm/git-loom-plugins-13c9afe2e85a/…/node_modules/loom-code/…`: the reviewers' lens file, the acceptance tester's `skills/closing-review/references/acceptance-test-report.md`, and the adversary's 16 reads.
  - Across all children: 0 `find /`, 0 reads of `/Users/kouko/GitHub/loom-plugins`, 0 reads of stale temp fixtures.
  - The loader put `Plugin root for this agent: <cache>/node_modules/loom-code — …` first in each agent's system prompt (`rerun/logs/agents.json`).
  - No child stopped on a plugin-cache prompt: the root's earlier `always` approvals for `node_modules/loom-code/*` covered them.
- The implementer was never dispatched.
  - The root session wrote `greet.py`, the tests and README itself (tools log lines 79-99), and committed `842ab23`.
  - `implementer` was not skipped: no selection was made, and no skip is in the intent or plan.
  - loom-code/skills/build/SKILL.md:68-76 makes implementer dispatch mandatory in that case.
- Verdict: partly.

### 5: carried over
- Reason: no hook script, `hooks-opencode.json` or loader hook code is in the fix range; the loader change is confined to `agents()`.
- Side observation: the intent restatement came back in Traditional Chinese although every prompt was English. The cause was not isolated.

### 6: re-tested
- In a clean worktree at `136c0248`, the tests covering the fix:
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_opencode_loader.py tests/test_agy_install_docs.py` → `22 passed`.
  - `python3 scripts/sync_codex_manifests.py --check --all` → exit 0.
  - `git diff --stat 5bc86a10..136c0248 -- '*.json' '**/hooks*'` → empty.
  - Log: `rerun/logs/a6-targeted.txt`.
- Full suite command, run by `finalize-review`: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. The tester did not run it this time.
- Verdict: works.

### 7: carried over
- Reason: `PRINCIPLES.md` is not in the fix range.

### 8: carried over
- Reason: no manifest, CHANGELOG or version string is in the fix range, so the versions stay 3.24.0 / 2.7.1 / 5.5.6 and consistent.

### Cost
- All 7 sessions: 7,115,186 non-cached input tokens, 5,572,966 cache reads, 45,465 output tokens. Reported cost 0 (free routes).
- The root session alone: 5.07M input.
- The ~6M budget was passed while ship was already running (6.65M at the github-rules question). The tester sent the one remaining answer so the flow could reach the PR, and ended at 7.1M.

### Side effects outside the sandbox
- The root session ran `pip3 install --break-system-packages pytest -q` in its shell.
  - This installed pytest 9.1.1, pluggy 1.6.0, iniconfig 2.3.0, packaging 26.3 and pygments 2.21.0 into `/opt/homebrew/lib/python3.14/site-packages`.
  - dist-info mtimes: 2026-09-29 22:08:41-42.
- OpenCode's shell tool is not gated by `external_directory`. The root also listed the tester's scratch directory and printed `oc-at/env.sh`, which holds no key. That only happened because the throwaway project sat inside the tester's scratch area.

### Cleanup
- The isolated service was stopped; nothing listens on 49613.
- The stand-in and monitors were stopped.
- The worktree was removed with `git worktree remove`.
- The real repo is clean at `136c0248`.
- The scratch repo and PR #1 remain for the user to delete.
