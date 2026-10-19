# Fold workaround lessons into loom — acceptance test evidence

## Re-run after fix (2026-10-03, HEAD 87f73a96, fix range 162e9638..87f73a96)

Clean copy: `git worktree add --detach <scratch>/at-wt2 87f73a96`.
Setup check: criterion tests import and run in the clean copy, and
`/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`
exits 0, so the change loads and is usable there.

Fix diff touches: `loom-code/scripts/loom_checker/probes.py`,
`loom-code/tests/test_loom_attestation.py`, `loom-code/skills/closing-review/references/adversarial.md`,
`loom-code/agents/adversary.md`, `loom-code/CHANGELOG.md`, the plan.
Re-tested in full: 1, 2, 4, 8. Carried over: 3 (no change to
`command_handlers/publish.py` or `test_loom_publish.py`), 5 (no change to
`agents/implementer.md`), 6 (no change to `AGENTS.md`), 7 (no change to
`loom-design/skills/capture-intent/SKILL.md`) — checked against
`git diff --stat 162e9638..87f73a96`.

### R1 (line 1)
- How: `scratchpad/line1b.py <clean copy>` calls `command_names_artifact` and
  `command_executes_artifact` (the pair `finalize-review` and the attestation
  check apply) for 38 commands, artifact A = `docs/loom/c/probes/test_x_state_expected.py`.
- What came back at 87f73a96:
  - ACCEPT: `pytest A`, `-q A`, `-q -p no:cacheprovider A`, `--tb=short -x A`,
    `-k smoke A`, `uv run --isolated --with pytest python -m pytest -q A`,
    `/opt/homebrew/bin/python3 -m pytest -v -W error A`, `python3 A`,
    `-pno:cacheprovider A`, `-rA A`, `-vx A`, `--strict-markers --no-header A`,
    `A -q --tb=short`.
  - REFUSE (does not run A): `tests/other.py A`, `--deselect A tests/other.py`,
    `--ignore A tests/other.py`, `-q` (no file), `python3 -c A`, `bash A`,
    `node A`, `A; touch x`, `--unknown-opt value A`, `uv run pytest A`,
    `-q A --deselect` (value option with no value).
  - REFUSE (runs no tests; earlier nit): `--co A`, `--collect-only A`,
    `A --collect-only`, `A --co`, `A -q --co`, `--help A`, `-h A`,
    `--version A`, `-V A`, `--setup-only A`, `--setup-plan A`, `--fixtures A`,
    `--markers A`.
  - REFUSE (unlisted but ordinary; fail-closed): `--junitxml out.xml A`, `-n 4 A`.
- Extra probe with real pytest on a red test file (`scratchpad/oprobe/test_red.py`):
  `-o addopts=--collect-only` is accepted by the checker but pytest still runs
  the test (exit 1), so it is no bypass; `-k nomatch` is accepted and exits 5
  (no test run, non-zero, so not a false pass).
- Criterion tests (pass, clean copy):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project --python /opt/homebrew/bin/python3 --with pytest python -m pytest -q -p no:cacheprovider loom-code/tests/test_loom_attestation.py::test_pytest_runner_directly_executes_named_artifact loom-code/tests/test_adversarial_pytest_option_order.py loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`
  -> `5 passed`.
- Earlier nit (collect-only accepted before the file): resolved.

### R2 (line 2)
- How: read the shipped text in the clean copy.
- What came back: `adversarial.md:39-46` — the first part "writes no new
  program: besides its report, it may only add a `concern:` line to an existing
  test it names as its program"; `adversarial.md:70-76` unchanged (no attack
  earned a program -> name one existing covering test with its `concern:`
  line); reuse rule `adversarial.md:78-92`. `adversary.md:42-49` — same, plus
  "when none exists, say so in your report, so Build can ask the user, in plain
  words, whether to skip `adversarial`." Build's plain-words skip handling:
  `loom-code/skills/build/SKILL.md:127-130`.

### R4 (line 4)
- How: read the shipped text.
- What came back: `adversarial.md:158-164` — "A finding that only a loom agent
  or user deliberately defeating one of loom's own internal rules (a budget, a
  cap, a check) could trigger is rated `nit` and so recorded as a known
  limitation; a finding reachable by untrusted input, including a deliberate
  attacker, or without that intent keeps its severity. Build fixes every fatal
  or important finding before hand-off" (Build's rule unchanged).
- Note: narrower than the intent's literal wording ("someone deliberately
  defeating a rule"); recorded in the report as decided on the user's behalf.

### R8 (line 8)
- How (clean copy): manifest check above; `"version"` grep across
  `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
  `package.json`; top CHANGELOG heading; README grep; release-metadata test (R1 run).
- What came back: loom-code 3.29.0 x4, CHANGELOG `## [3.29.0] — 2026-10-03`,
  3.29.0 in README / README.ja / README.zh-TW; loom-design 2.11.0 x4,
  CHANGELOG `## [2.11.0] — 2026-10-03`; loom-workflow 5.6.2 unchanged,
  `git diff --stat fa7d0dee..HEAD -- loom-workflow` empty.
- Full suite: not run by me this round (step 6). It is executed by
  `finalize-review`, which refuses the attestation on failure:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
  The orchestrator reports this command exited 0 on 87f73a96 (not my result).

---

## First run

Tried on 2026-10-03, in a clean copy of the project at 18ce2b02
(`git worktree add --detach <scratch>/at-wt HEAD`). For comparison a second
clean copy at the base commit fa7d0dee was made (`<scratch>/base-wt`).

Setup: the repository's documented way to verify a build is the package
suite plus the Codex manifest check (AGENTS.md, Test Location). Both ran in
the clean copy (see 8) and passed, so the change loads and is usable there.
The plugins were not installed into a live Claude Code host from the
marketplace; the guidance-text lines (2, 4, 5, 6, 7) were checked by reading
the shipped text a fresh agent reads.

## 1. Closing review accepts an adversarial program command whose test-runner options come before the test file, and still refuses a command that does not run the declared program.
- How I tried it: a script (`scratchpad/line1.py`) imported the checker in each
  clean copy and called the two checks that both `finalize-review`
  (`loom-code/scripts/loom_checker/command_handlers/finalize.py:111-114`) and
  the attestation check (`loom-code/scripts/loom_checker/attestation.py:84-87`)
  apply to every adversarial command: `command_names_artifact` and
  `command_executes_artifact`. Artifact `docs/loom/c/probes/test_x_state_expected.py`.
- What came back (HEAD vs base):

| Command (artifact = A) | HEAD | base |
|---|---|---|
| `python3 -m pytest A` | ACCEPT | ACCEPT |
| `python3 -m pytest -q A` | ACCEPT | REFUSE |
| `python3 -m pytest -q -p no:cacheprovider A` | ACCEPT | REFUSE |
| `python3 -m pytest --tb=short -x A` | ACCEPT | REFUSE |
| `python3 -m pytest -k smoke A` | ACCEPT | REFUSE |
| `uv run --isolated --with pytest python -m pytest -q A` | ACCEPT | REFUSE |
| `/opt/homebrew/bin/python3 -m pytest -v -W error A` | ACCEPT | REFUSE |
| `python3 A` | ACCEPT | ACCEPT |
| `python3 -m pytest tests/other.py A` | REFUSE | REFUSE |
| `python3 -m pytest --deselect A tests/other.py` | REFUSE | REFUSE |
| `python3 -m pytest --ignore A tests/other.py` | REFUSE | REFUSE |
| `python3 -m pytest -q` | REFUSE | REFUSE |
| `python3 -c A` | REFUSE | REFUSE |
| `bash A` / `node A` | REFUSE | REFUSE |
| `python3 -m pytest A; touch x` | REFUSE (shell metacharacters) | REFUSE |
| `python3 -m pytest --unknown-opt value A` | REFUSE (fail-closed) | REFUSE |
| `uv run pytest A` | REFUSE | REFUSE |
| `python3 -m pytest --co A` | ACCEPT | REFUSE |

- Criterion tests run (pass): `loom-code/tests/test_loom_attestation.py::test_pytest_runner_directly_executes_named_artifact`,
  `loom-code/tests/test_adversarial_pytest_option_order.py` (3 cases).
- Observation (nit): `--co` / `--collect-only` before the file is now accepted;
  it collects but runs no test. The same option after the file
  (`python3 -m pytest t/p.py --collect-only`) was already accepted at base
  (checked: base True/False, HEAD True/True for after/before), so this is a
  new spelling of an existing gap, not a new one.
- Evidence: table above, captured from the script output.

## 2. The adversary guidance tells an attack that found nothing on a change that needs an executed program to reuse an existing repository test instead of reporting a bare attempt.
- How I tried it: read the shipped text in the clean copy.
- What came back: `loom-code/skills/closing-review/references/adversarial.md:69-73`
  — "when no attack earned a new program, the adversary names one existing
  repository test that covers the change as this change's program, adding the
  `concern:` line the reuse rule below describes, when such a test exists";
  `adversarial.md:43-44` (the part-one ending names that test);
  `loom-code/agents/adversary.md:44-47` repeats it in the adversary's own run
  order and points at the reuse rule (`adversarial.md:79-88`). The adversary
  is told to read `adversarial.md` first (`adversary.md:30`).
- Note: the text applies to every attack that found nothing, not only to a
  change that needs an executed program; that is broader than the line, not
  narrower.
- Evidence: the quoted lines.

## 3. When publishing is refused because the pull request does not yet show the pushed commit, the refusal tells the user to retry once right after a push and to stop if it is refused again; publishing still refuses and never retries on its own.
- How I tried it: read the refusal branch and ran the test that drives the real
  publish command against a fake `gh` returning a mismatching PR identity.
- What came back: `loom-code/scripts/loom_checker/command_handlers/publish.py:510-515`
  refuses with "existing pull request identity does not match origin, HEAD,
  and base; right after a push GitHub may not yet show the new commit, so
  retry once, and stop if it is refused again". No loop around the PR listing.
  `loom-code/tests/test_loom_publish.py::test_publish_rejects_cross_repository_pr_match`
  passed: exit 1, the hint present in stderr, exactly one `/pulls?` call
  (no automatic retry), and no `create` call.
- Evidence: the named test (passed, run in the clean copy) and the quoted message.

## 4. The adversary guidance rates a finding that only someone deliberately defeating a rule could trigger as a nit, so it is recorded as a known limitation rather than fixed, while findings that can happen without such intent keep their severity.
- How I tried it: read the shipped text.
- What came back: `adversarial.md:156-161` — "A finding that only someone
  deliberately defeating a rule could trigger, such as a deliberate bypass of
  an internal budget, is rated `nit` and so recorded as a known limitation; a
  finding that can happen without that intent keeps its severity. Build fixes
  every fatal or important finding before hand-off" (Build's rule unchanged).
- Evidence: the quoted lines.

## 5. The implementer guidance says that removing a behaviour removes the tests that only check it, and that this is not deleting a test to reach green.
- How I tried it: read the shipped text.
- What came back: `loom-code/agents/implementer.md:40-43` — "Never delete, skip
  or weaken a test to reach green; it erases the evidence. When a task removes
  a behaviour, the tests that only check that behaviour are deleted with it;
  that is not deleting a test to reach green."
- Evidence: the quoted lines.

## 6. This repository's contributor guide says to bump versions in the last fix round before the review evidence is generated.
- How I tried it: read the shipped text.
- What came back: `AGENTS.md:116` — "版號在最後一輪 fix 就 bump，要在 closing-review 的
  finalize-review 產生 attestation 之前；在它之後才 bump 會讓 attestation 失效（stale）".
- Evidence: the quoted line.

## 7. capture-intent's description no longer claims a request made inside an active change.
- How I tried it: read the shipped description.
- What came back: `loom-design/skills/capture-intent/SKILL.md:4` now ends
  "skip non-software work, and skip a request inside an active change (its
  station continues it)." Contract test
  `loom-design/tests/spec/test_capture_intent_contract.py` passed (clean copy).
- Evidence: the quoted line and the named test.

## 8. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.
- How I tried it (clean copy):
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  - `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`
  - grep of `"version"` in each plugin's `plugin.json`, `.claude-plugin/plugin.json`,
    `.codex-plugin/plugin.json`, `package.json`; top CHANGELOG heading; the three READMEs.
- What came back:
  - Suite: exit 0 in 1:58; 13 pytest groups, 3043 passed, 0 failed (skips only in
    `tests/local`-style groups); shell checks all PASS.
  - Manifest check: exit 0.
  - loom-code: 3.29.0 in all four manifests, CHANGELOG `## [3.29.0] — 2026-10-03`,
    README / README.ja / README.zh-TW 3.29.0; root README row 3.28.0 -> 3.29.0.
  - loom-design: 2.11.0 in all four manifests, CHANGELOG `## [2.11.0] — 2026-10-03`,
    the three READMEs 2.11.0; root README row 2.10.0 -> 2.11.0.
  - loom-workflow: no file changed (`git diff --stat fa7d0dee..HEAD -- loom-workflow` empty), no bump needed.
  - `test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` passed.
- Evidence: the captured suite log summary and the version greps above.
