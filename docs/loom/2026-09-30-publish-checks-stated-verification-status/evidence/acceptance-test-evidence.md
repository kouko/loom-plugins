# Publish refuses a PR body that misstates its verification, and the OpenCode docs are tidied — acceptance test evidence

Tried on 2026-09-30, in a clean copy of the project at 2c6c419e.

## Setup

- Clean copy: `git worktree add --detach <scratch>/clean 2c6c419e` (fresh tree, no uncommitted files). A second clean copy at the branch base `adafa838` was made to compare "before" behaviour.
- The project's setup for this surface is the plugin's own checker script; it loads and runs from the clean copy: `/opt/homebrew/bin/python3 loom-code/scripts/loom_checker.py --list-rules` printed 26 rules, exit 0 (Python 3.14.7).
- Throwaway repositories: one per scenario, built by `scenarios.sh` in the scratch dir — `git init -b main`, an initial commit, branch `engineering/demo-change`, a committed intent `docs/loom/intent/demo-change.md` (`status: confirmed 2026-09-30`), one code file, and `origin = https://git.invalid/example/project.git`. `.invalid` is a reserved TLD that never resolves, so no call could reach any real host, least of all github.com. A local bare repo `<scenario>.bare.git` sits next to each.
- Driver `drive_publish.py` runs the checker's real `cmd_publish` handler (the same code `loom_checker.py publish` runs) with only its outward-call seam `run_publish_external` replaced: every outward argv is printed; `git ... origin ...` is re-pointed at the local bare repo and really run; `gh repo view` answers `main`; anything else (`gh api`, `gh pr create`) is stopped and never sent. Everything before that seam — change identification, body checks, attestation checks, status computation — runs unmodified.
- Every PR body carries Ship's nine headings in order; only the Verification section varies.
- Direct CLI runs (no driver) were also made for the refusal cases with the exact command `/opt/homebrew/bin/python3 <clean>/loom-code/scripts/loom_checker.py publish --confirm-authorized --title "feat: demo" --body-file <abs>`.

## 1. Publishing a change whose PR body states a verification status different from the one loom computes for that branch is refused before anything is pushed, and the refusal names the status the body must carry.

- How I tried it: five bodies against branches that compute `absent` (no attestation), plus one against a branch that computes `stale (...)`:
  - plain `Verification status: valid (skipped: reviewers)` (the exact misstatement from the 2026-09-29 OpenCode run)
  - `- Verification status: valid` (list item)
  - `**Verification status:** valid (skipped: reviewers)` (bold label)
  - `> Verification Status: valid` (quote + capitalised label)
  - stale branch (committed attestation with an incomplete schema), body `Verification status: valid`
- What came back (driver, HEAD 2c6c419e), each exit 1, `outward calls attempted: 0`, local bare origin empty:
  ```
  BLOCK push.contextual-body: PR body states 'Verification status: valid (skipped: reviewers)', but publish computes a different status; the body must carry exactly:
  Verification status: absent
  BLOCK push.contextual-body: PR body states '- Verification status: valid', but ... the body must carry exactly:
  Verification status: absent
  BLOCK push.contextual-body: PR body states '**Verification status:** valid (skipped: reviewers)', but ... must carry exactly:
  Verification status: absent
  BLOCK push.contextual-body: PR body states '> Verification Status: valid', but ... must carry exactly:
  Verification status: absent
  BLOCK push.contextual-body: PR body states 'Verification status: valid', but ... must carry exactly:
  Verification status: stale (attestation has an unknown or incomplete schema)
  ```
- Direct CLI (plain and bold cases): same BLOCK text, `exit=1`, bare origin refs `[]`.
- Before the change (base adafa838, same driver, same repos): all four `absent` misstatements were published — `Verification absent for <sha>`, then `gh repo view`, `ls-remote`, `push ... origin <sha>:refs/heads/engineering/demo-change`, and the bare origin then held `refs/heads/engineering/demo-change`.
- Evidence: captured output above; focused tests `test_stated_status_must_equal_the_computed_status`, `test_misstated_status_refused_before_network`, `test_publish_decoratedMisstatedStatus_refusedBeforePush[3 cases]` pass (`tests/test_loom_publish.py` + `tests/test_adversarial_decorated_status_line.py`: 90 passed). Code: `loom-code/scripts/loom_checker/rule_checks/publish.py` `validate_stated_status`; called at `command_handlers/publish.py:443`, before the first outward call at `:452`.

## 2. Publishing a change whose generated attestation exists in the working tree but is not committed is refused before anything is pushed, and the refusal says to commit it.

- How I tried it: (a) attestation file created but never added (`git status --porcelain` = `?? docs/loom/demo-change/`), body `Verification status: absent`; (b) attestation committed, then edited (`git status --porcelain` = ` M docs/loom/demo-change/attestation.json`).
- What came back (both cases, driver and direct CLI for (a)), exit 1, `outward calls attempted: 0`, bare origin empty:
  ```
  BLOCK publish.preconditions: docs/loom/demo-change/attestation.json is not committed — commit it, then publish again
  ```
- Following the remedy on (a): `git add docs && git commit` → publish again with body `absent` → refused naming `Verification status: stale (attestation has an unknown or incomplete schema)` (the committed demo attestation is not a real one) → corrected the line → publish proceeded to push (5 outward calls, bare origin holds the branch).
- Before the change (base): both (a) and (b) were published, with status `stale (attestation is not committed at HEAD)` / `stale (attestation has an unknown or incomplete schema)` and a push to the bare origin.
- Evidence: captured output above; focused test `test_uncommitted_attestation_refused_before_network` passes. Code: `command_handlers/publish.py:425-431`.

## 3. Publishing a change whose PR body states the computed status, with no uncommitted attestation, behaves as before, including when the status is `absent` or `stale`.

- How I tried it: same driver against HEAD and against base adafa838, for (a) truthful `Verification status: absent`, (b) no status line at all, (c) truthful `Verification status: stale (attestation has an unknown or incomplete schema)` with a committed attestation.
- What came back, identical at HEAD and at base for all three (only commit shas differ):
  ```
  Verification absent for <sha>            | Verification stale (attestation has an unknown or incomplete schema) for <sha>
  loom: verification absent (missing: plan, attestation); publishing anyway.   | ... stale (...) (missing: plan); publishing anyway.
  Publication target: git.invalid/example/project base main
  outward calls attempted: 5
      gh repo view git.invalid/example/project --json defaultBranchRef --jq .defaultBranchRef.name
      git -C <repo> ls-remote --heads origin refs/heads/engineering/demo-change
      git -C <repo> push --no-follow-tags --recurse-submodules=no -u --no-verify origin <sha>:refs/heads/engineering/demo-change
      git -C <repo> ls-remote --heads origin refs/heads/engineering/demo-change
      gh api --hostname git.invalid repos/example/project/pulls?state=open&head=...
  branches in local bare origin after publish: [refs/heads/engineering/demo-change]
  ```
  The run stops at `gh api` only because the driver refuses to send it (`BLOCK publish.preconditions: publication command failed: intercepted by acceptance tester: not sent`); the same stop happens at base.
- Not tried: a truthful `valid` status. Producing a real attestation needs a full closing review in the throwaway repo; the `valid` path is covered only by the existing publish tests (e.g. `test_confirmed_current_intent_publishes_without_ship_reask`), which pass.
- Evidence: captured output above; `test_good_body_without_attestation_publishes_with_reminder` and the whitespace case in `test_stated_status_must_equal_the_computed_status` pass.

## 4. The three OpenCode wording defects named in the Problem are fixed where they appear.

- How I tried it: read the ten READMEs (`README.md`, `loom-{code,design,workflow}/README{,.ja,.zh-TW}.md`), `docs/loom/2026-09-29-opencode-v2-compatibility/spec.md` REQ-1 and design decision, and that change's `acceptance-test-report.md`; `git diff adafa838..HEAD` on each; grep for `TUI`, `設定檔`, `沒講`, `does not name`.
- What came back:
  - Report: line 24 now reads 「說明已寫出設定檔在哪 … `~/.config/opencode/opencode.json`」; lines 34 and 49 corrected the same way; no remaining line says the install steps omit the settings file.
  - Spec REQ-1 (line 7): the WHEN clause and the carried quote still name "the TUI's plugin dialog", followed by the added note "(The TUI has no such dialog on 2.0.18–2.0.20; see Design decision — install is by the plugin command or `opencode.json`.)". Design decision line 24 agrees. The requirement no longer contradicts the decision silently, but it was annotated, not rewritten (plan W1-02 records this as agent-decided).
  - READMEs: all ten carry "The OpenCode TUI (2.0.18–2.0.20) has no plugin-install option" (or its ja/zh-TW equivalent), so the claim is bounded to verified versions; and `opencode.json` is now "the file `plugin add` writes in OpenCode's config folder `~/.config/opencode/`" — the folder is no longer called a file. Old text: "in OpenCode's config folder (`~/.config/opencode/`, the file `plugin add` writes)".
- Evidence: `tests/test_agy_install_docs.py` (14 passed) pins the bounded sentence and folder wording.

## 5. The repository's memory store holds the lesson that a host's interface or install claim is checked against the host's official documentation before it is written into install docs.

- How I tried it: read `docs/loom/memory/`; ran `/opt/homebrew/bin/python3 loom-workflow/skills/loom-memory/scripts/loom_memory.py validate docs/loom/memory`.
- What came back: new entry `docs/loom/memory/check-a-host-install-claim-against-its-official-docs-and-running-version.md` (type `gotcha`), indexed in `docs/loom/memory/index.md`. It says: before writing any host install or interface step, cite the official doc page and try it on the stated version; it cites the OpenCode docs URL and the removed shift+i TUI route of PR #70. Validator: `loom_memory validate: OK — OKF v0.2-compatible Loom memory profile holds.` exit 0.
- Evidence: the entry file and validator output.

## 6. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

- How I tried it: in the clean copy, `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; read every manifest's `version`, each CHANGELOG's top section and README version strings; `scripts/sync_codex_manifests.py --check --all`.
- What came back:
  - Suite: exit 0, `Summary: 11 PASS / 0 FAIL` (run requested explicitly by the closing-review station; the tail kept only the summary and the last shell-test lines, so per-test counts were not captured).
  - Plugins changed on the branch: loom-code, loom-design, loom-workflow (plus root README, docs, root tests).
  - loom-code 3.25.0 in `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`, CHANGELOG `## [3.25.0] — 2026-09-30`, all three READMEs, root README table and section.
  - loom-design 2.7.2 and loom-workflow 5.5.7: same set, all consistent. Root `.claude-plugin/marketplace.json` carries no version.
  - `sync_codex_manifests.py --check --all`: exit 0.
- Evidence: suite output above; `finalize-review` runs the same suite before the change is accepted and blocks on failure.

## Re-run on 2026-09-30, at cf17c38e

Fix range d867cf9c..cf17c38e (cf17c38e code: status-claim normalisation, refusal wording, rule texts, Ship prose; 924c5124 docs: README intro line, spec.md:24 version bound, dated notes in the old report). Fresh clean worktree at cf17c38e, fresh base worktree at adafa838, same `scenarios.sh` / `stale.sh` / `drive_publish.py` method (origin `https://git.invalid/...`, outward-call seam, local bare remote; nothing contacted any network host). Checker loads: `--list-rules` prints 26 rules.

- 1: re-tested — all earlier forms again plus three new ones, against `absent` branches, and `valid` against the `stale` branch. Every one exit 1, `outward calls attempted: 0`, bare origin `[]`, with the new wording:
  ```
  BLOCK push.contextual-body: PR body states 'Verification status: valid (skipped: reviewers)'; the body must carry exactly this bare line:
  Verification status: absent
  ... '- Verification status: valid' ...                       -> Verification status: absent
  ... '**Verification status:** valid (skipped: reviewers)' ... -> Verification status: absent
  ... '> Verification Status: valid' ...                       -> Verification status: absent
  ... '**Verification status**: valid' ...   (new)             -> Verification status: absent
  ... '### Verification status: valid' ...   (new)             -> Verification status: absent
  ... 'Verification status：valid' ...  (new, full-width colon) -> Verification status: absent
  ... 'Verification status: valid' (stale branch) -> Verification status: stale (attestation has an unknown or incomplete schema)
  ```
- 2: re-tested (the same scenario script covers it; the fix only moved comments around the check and extended the rule text) — untracked and modified attestation both: `BLOCK publish.preconditions: docs/loom/demo-change/attestation.json is not committed — commit it, then publish again`, exit 1, 0 outward calls, bare origin `[]`.
- 3: re-tested — truthful bare `absent`, no status line, prose line `Ship computes the verification status: see CI.`, and truthful bare `stale (attestation has an unknown or incomplete schema)`: each prints `Verification <status> for <sha>`, makes the same 5 outward calls as base (`gh repo view`, `ls-remote`, `push ... origin <sha>:refs/heads/engineering/demo-change`, `ls-remote`, stopped `gh api`) and the bare origin holds `refs/heads/engineering/demo-change`.
  New cases, truthful status in non-bare form, HEAD vs base:
  ```
  body line                            HEAD cf17c38e                                   base adafa838
  Verification status：absent          BLOCK push.contextual-body ... bare line; bare []   published, bare has branch
  **Verification status:** absent      BLOCK push.contextual-body ... bare line; bare []   published, bare has branch
  - Verification status: absent        BLOCK push.contextual-body ... bare line; bare []   published, bare has branch
  ```
  A body that states the computed status, only decorated, no longer behaves as before: it is refused, with the exact bare line as the remedy. The bullet case was already refused at 2c6c419e (the first run did not try it; `test_stated_status_must_equal_the_computed_status` pins `> **Verification status:** absent` as refused). This is a conflict with the intent's Constraint "only a body that misstates the status ... is refused" -> verdict partly.
- 4: re-tested over all three surfaces —
  - READMEs: the intro line in all ten now reads "OpenCode v2 (verified on 2.0.18; plugins installed from the CLI also load in the TUI) installs plugins from GitHub." (ja/zh-TW equivalents); `grep "CLI and TUI|CLI と TUI|CLI 與 TUI"` over the ten = 0 hits. The bounded "TUI (2.0.18–2.0.20) has no plugin-install option" sentence and the folder/file wording are unchanged from the first run.
  - spec.md: line 7 (REQ-1) unchanged, still annotated; line 24 design decision now says "no plugin-install option on 2.0.18–2.0.20".
  - Old report: line 24 restored to 「說明沒講設定檔在哪 … 沒說是哪個位置的設定檔」 plus 「（2026-09-30 更正：此次重跑時說明未寫出位置；61b46c87 之後已寫明 `~/.config/opencode/opencode.json`）」; line 34 now names the isolated config folder's `opencode.json`; line 49 restored with the same dated correction note. The report now records the run's observation and marks it superseded, so it no longer tells a reader the current install steps omit the settings file.
- 5: carried over — `git diff --stat d867cf9c..cf17c38e` touches no file under `docs/loom/memory/`.
- 6: re-tested — suite in the clean worktree at cf17c38e: exit 0, no failures (largest pytest run `2095 passed, 2 skipped`; every other pytest run and shell-test summary passed, e.g. `Summary: 9 PASS / 0 FAIL`). Focused: `loom-code/tests/test_loom_publish.py`, `loom-code/tests/test_adversarial_decorated_status_line.py`, `tests/test_agy_install_docs.py`: 106 passed. The fix range changes no manifest, CHANGELOG or README version string; versions stay loom-code 3.25.0 / loom-design 2.7.2 / loom-workflow 5.5.7, consistent as in the first run.

## Re-run on 2026-09-30, at df8feb8c

Fix range 7b548699..df8feb8c (df8feb8c: `validate_stated_status` compares only the value after the first `:`/`：`, stripped of whitespace and `*_`|`; `_status_claim` — which decides whether a line is a status claim at all — is unchanged). Fresh clean worktree at df8feb8c, same method as before (origin `https://git.invalid/...`, outward-call seam, local bare remote; no network host contacted). Checker loads (26 rules). Focused tests `test_loom_publish.py` + `test_adversarial_decorated_status_line.py`: 92 passed. Rows 2, 4, 6 keep their cf17c38e result and row 5 its 2c6c419e result (the range touches only the value comparison and its test).

- 1: re-tested — wrong value `valid` against `absent` branches, each exit 1, `outward calls attempted: 0`, bare origin `[]`, message `...; the body must carry exactly this bare line:` / `Verification status: absent`:
  `Verification status: valid (skipped: reviewers)`, `- Verification status: valid`, `**Verification status:** valid (skipped: reviewers)`, `> Verification Status: valid`, `**Verification status**: valid`, `### Verification status: valid`, `Verification status：valid`, `| Verification status: valid |`. Against the `stale` branch, `Verification status: valid` is refused naming `Verification status: stale (attestation has an unknown or incomplete schema)`.
  Not refused: a two-cell table row with no colon —
  ```
  | Check | Result |
  |---|---|
  | Verification status | valid |
  ```
  on an `absent` branch printed `Verification absent for <sha>`, made the 5 outward calls, and the bare origin holds `refs/heads/engineering/demo-change`. `_status_claim` matches only `verification status` followed by `:`, so this line is never judged (same at 2c6c419e and cf17c38e). Verdict partly.
- 3: re-tested — correct value `absent` in every form, each `Verification absent for <sha>`, 5 outward calls identical to base, bare origin holds the branch: bare `Verification status: absent`; no status line; prose `Ship computes the verification status: see CI.`; `Verification status：absent`; `**Verification status:** absent`; `- Verification status: absent`; `> Verification status: absent`; `| Verification status: absent |`; `### Verification status: absent`; `**Verification status**: absent`; `` `Verification status: absent` ``. Truthful bare `stale (attestation has an unknown or incomplete schema)` on the stale branch: same, published. The three forms refused at cf17c38e (full-width colon, bold, bullet) now publish as at base.
- Decision raised at cf17c38e (should a correct but decorated status be refused?): settled by the intent — Constraints: "only a body that misstates the status, or an attestation generated but left uncommitted, is refused", and Acceptance 3. Removed from the report's open questions.

## Re-run on 2026-09-30, at f93e1ea6

Fix range d5c8187a..f93e1ea6 (f93e1ea6: `|` now also separates label from value — `_status_claim` maps `|` to `:` before matching `^[: ]*(?:\d+ )?verification status ?:`, and the value is `status[\W_]*?[:：|](.*)` stripped of whitespace and `*_`|`). Fresh clean worktree at f93e1ea6, same method (origin `https://git.invalid/...`, outward-call seam, local bare remote; no network host contacted). Checker loads (26 rules). Focused tests `test_loom_publish.py` + `test_adversarial_decorated_status_line.py`: 92 passed. Rows 1 and 3 now carry f93e1ea6 results; rows 2, 4, 6 keep cf17c38e and row 5 keeps 2c6c419e (the range touches only the status-claim parser and its test).

Every branch below computes `absent` unless marked stale. "REFUSED" = exit 1, `BLOCK push.contextual-body: PR body states '<line>'; the body must carry exactly this bare line:` / `Verification status: absent`, 0 outward calls, bare origin empty. "published" = `Verification absent for <sha>`, the same 5 outward calls as base, bare origin holds `refs/heads/engineering/demo-change`.

- 1: re-tested — wrong value `valid`:

  | Body line(s) | Result |
  |---|---|
  | `Verification status: valid (skipped: reviewers)` | REFUSED |
  | `- Verification status: valid` | REFUSED |
  | `**Verification status:** valid (skipped: reviewers)` | REFUSED |
  | `> Verification Status: valid` | REFUSED |
  | `**Verification status**: valid` | REFUSED |
  | `### Verification status: valid` | REFUSED |
  | `Verification status：valid` | REFUSED |
  | `\| Verification status: valid \|` | REFUSED |
  | table header + `\| Verification status \| valid \|` (separate cells, the round-2 gap) | REFUSED |
  | `\|Verification status\|valid\|` | REFUSED |
  | table header + `\| **Verification status** \| `valid` \|` | REFUSED |
  | `Verification status \| valid` | REFUSED |
  | `\| Verification status \| valid \| from CI \|` | REFUSED |
  | `1. Verification status: valid` | REFUSED |
  | `  * Verification status: valid` | REFUSED |
  | `Verification status: valid` on the stale branch | REFUSED, names `Verification status: stale (attestation has an unknown or incomplete schema)` |
  | `- [x] Verification status: valid` (task list) | **published** |
  | table header + `\| Status line \| Verification status: valid \|` (claim in second cell) | **published** |
  | `Verification status - valid` (dash separator) | **published** |

  The task-list line normalises to `x verification status :`, which the `^[: ]*(?:\d+ )?` prefix does not allow; the second-cell and dash lines never reach the `verification status :` shape at line start. Verdict partly.
- 3: re-tested — correct value:

  | Body line(s) | Result |
  |---|---|
  | `Verification status: absent`; no status line; prose `Ship computes the verification status: see CI.` | published |
  | `Verification status：absent`, `**Verification status:** absent`, `- Verification status: absent`, `> Verification status: absent`, `\| Verification status: absent \|`, `### Verification status: absent`, `**Verification status**: absent`, `` `Verification status: absent` ``, `1. Verification status: absent` | published |
  | table header + `\| Verification status \| absent \|`; `\|Verification status\|absent\|`; `\| **Verification status** \| `absent` \|` | published |
  | table header + `\| Ship computes the verification status \| see CI \|` (mention only) | published (not judged) |
  | `Verification status: stale (attestation has an unknown or incomplete schema)` on the stale branch | published |
  | `\| Verification status \| absent \| from CI \|` (three cells) | **REFUSED** — value parsed as `absent \| from CI` |
  | `\| Verification status \| Reviewer \|` / `\|---\|---\|` / `\| absent \| CI \|` (header names the column, value in the next row) | **REFUSED** — header row judged, value parsed as `Reviewer` |

  At base adafa838 both refused tables would have published (base never judged the status line). A body stating the computed status is refused in these two table shapes, against the intent's Constraint. Verdict partly.

## Re-run on 2026-09-30, at 0efe4f93

Fix range 8be6765e..0efe4f93 (0efe4f93: claim prefix allows a task-list `x`; value is `[^|]*` after the separators, so it stops at the next cell border; an empty value is not judged). Fresh clean worktree at 0efe4f93, same method (origin `https://git.invalid/...`, outward-call seam, local bare remote; no network host contacted). Checker loads (26 rules). Focused tests: 92 passed. Rows 1 and 3 now carry 0efe4f93 results; rows 2, 4, 6 keep cf17c38e and row 5 keeps 2c6c419e (the range touches only the status-claim parser and its test). REFUSED / published as defined in the f93e1ea6 section.

- 1: re-tested — wrong value `valid`, all REFUSED naming `Verification status: absent` (0 outward calls, bare origin empty): every f93e1ea6 REFUSED form again (plain, bullet, bold, bold label, quote + caps, heading, full-width colon, `| … : valid |`, separate cells with header, tight cells, bold cell, no leading pipe, three cells, numbered, nested bullet), plus `- [x] Verification status: valid` (was published at f93e1ea6), `- [ ] Verification status: valid`, `* [X] **Verification status:** valid`, `| Verification status: valid | reviewers skipped |`. Stale branch, body `valid`: REFUSED naming `Verification status: stale (attestation has an unknown or incomplete schema)`.
  Still published, declared by the builder as known limitations for the PR: table header + `| Status line | Verification status: valid |` (claim in second cell); `Verification status - valid` (dash separator).
  Still published, NOT among the declared limitations: `| Verification status |` / `|---|` / `| valid |` — a one-column header names the status and the wrong value sits in the next row; the header has no value so it is not judged, and the value row carries no label. Verdict partly (same class as the second-cell limitation — value not on the label's line — but not declared).
- 3: re-tested — correct value, published (5 outward calls identical to base, bare origin holds the branch): every f93e1ea6 published form again, plus `| Verification status | absent | from CI |` (REFUSED at f93e1ea6), `| Verification status |` / `|---|` / `| absent |`, `- [x] Verification status: absent`, and a bare `Verification status:` with no value (not judged). Truthful `stale (...)` on the stale branch: published.
  Still REFUSED: `| Verification status | Reviewer |` / `|---|---|` / `| absent | CI |` — `BLOCK push.contextual-body: PR body states '| Verification status | Reviewer |'; the body must carry exactly this bare line:` / `Verification status: absent`. The two-column header's second cell `Reviewer` is read as the value. Base published it. Verdict partly.

## Re-run on 2026-09-30, at 5263a116

Fix range b9cc0f09..5263a116 (5263a116: only `:` / `：` separates label from value — `_status_claim` no longer maps `|` to `:`, claim regex `^(?:\d+ )?(?:x )?verification status ?:`, value `status[\W_]*?[:：][\s:：|*_`]*([^|]*)`). Fresh clean worktree at 5263a116, same method (origin `https://git.invalid/...`, outward-call seam, local bare remote; no network host contacted). Checker loads (26 rules). Focused tests: 92 passed. Rows 1 and 3 now carry 5263a116 results; rows 2, 4, 6 keep cf17c38e and row 5 keeps 2c6c419e (the range touches only the status-claim parser and its test). REFUSED / published as defined in the f93e1ea6 section.

- 1: re-tested — every colon-bearing wrong-value form REFUSED naming `Verification status: absent` (0 outward calls, bare origin empty): `Verification status: valid (skipped: reviewers)`, `- …: valid`, `**Verification status:** valid (skipped: reviewers)`, `> Verification Status: valid`, `**Verification status**: valid`, `### …: valid`, `Verification status：valid`, `| Verification status: valid |`, `| Verification status: valid | reviewers skipped |`, `1. …: valid`, `  * …: valid`, `- [x] …: valid`, `- [ ] …: valid`, `* [X] **Verification status:** valid`. Stale branch, body `Verification status: valid`: REFUSED naming `Verification status: stale (attestation has an unknown or incomplete schema)`.
  Published (builder-decided known limitations, to be stated in the PR):
  - separate cells, no colon: header + `| Verification status | valid |`, `|Verification status|valid|`, header + `| **Verification status** | `valid` |`, `Verification status | valid`, `| Verification status | valid | from CI |`, `| Verification status |` / `|---|` / `| valid |` (these were REFUSED at f93e1ea6 and 0efe4f93);
  - claim in second cell: header + `| Status line | Verification status: valid |`;
  - dash separator: `Verification status - valid`.
  Every form outside those three declared limitations holds. Verdict works.
- 3: re-tested — every correct-value form published (5 outward calls identical to base, bare origin holds the branch): bare `Verification status: absent`; no line; prose `Ship computes the verification status: see CI.`; `Verification status：absent`; `**Verification status:** absent`; `- …: absent`; `> …: absent`; `| Verification status: absent |`; `### …: absent`; `**Verification status**: absent`; `` `Verification status: absent` ``; `1. …: absent`; `- [x] …: absent`; bare `Verification status:` (no value); header + `| Verification status | absent |`; `|Verification status|absent|`; `| **Verification status** | `absent` |`; `| Verification status | absent | from CI |`; `| Verification status |` / `|---|` / `| absent |`; `| Verification status | Reviewer |` / `|---|---|` / `| absent | CI |` (REFUSED at 0efe4f93); mention row `| Ship computes the verification status | see CI |`. Stale branch, truthful `Verification status: stale (attestation has an unknown or incomplete schema)`: published. Verdict works.
- The two open questions raised at 0efe4f93 are closed: the one-column-header form is a builder-decided known limitation (separate cells, no colon), and the two-column-header form now publishes.
