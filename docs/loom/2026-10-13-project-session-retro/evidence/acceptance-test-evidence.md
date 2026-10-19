# Project session retro — acceptance test evidence

Tried on 2026-10-13 in a fresh local clone at `d2c9c893984191a0029d4ad4a112e39046ca5bf0`. The original change worktree was clean before this report was written. No implementation files were edited in either copy.

## Clean setup

- Attempt: `git worktree add --detach /private/tmp/loom-retro-acceptance-20261013 d2c9c893984191a0029d4ad4a112e39046ca5bf0`
- Result: `fatal: could not create directory of '/Users/kouko/GitHub/loom-plugins/.git/worktrees/loom-retro-acceptance-20261013': Operation not permitted`. The source repository's Git metadata is outside writable roots.
- Alternative: `git clone --no-local --no-checkout /private/tmp/loom-retro-20261013 /private/tmp/loom-retro-acceptance-20261013`, then `git checkout --detach d2c9c893984191a0029d4ad4a112e39046ca5bf0`.
- Result: clone and checkout succeeded; `git status --short --branch` printed `## HEAD (no branch)` with no changed files; `git rev-parse HEAD` printed the expected SHA.
- README setup check: `agy plugin validate ./loom-workflow` returned `[ok]`, `skills: 13 processed`, `hooks: 1 processed`.
- Isolated installation: with `HOME=/private/tmp/loom-retro-acceptance-home` and `XDG_CONFIG_HOME=/private/tmp/loom-retro-acceptance-config`, `agy plugin install ./loom-workflow` returned `[ok]`, `skills: 13 processed`, `hooks: 1 processed`; `agy plugin list` returned `loom-workflow`, source `antigravity`, components `skills` and `hooks`.
- `cmp` confirmed the installed `retro`, `distill-sessions`, and `using-loom-workflow` SKILL.md files exactly matched the clean clone. `git status --short` in the clone remained empty.

## 1. Current or specified session yields ranked, source-backed advice

- How I tried it: validated and installed the plugin from the clean clone; inspected the installed `retro` skill; ran its focused contract tests together with packaging and catalog tests. Then tried one live `agy --add-dir /private/tmp/loom-retro-acceptance-20261013 -p 'For one coding session retrospective, which loom-workflow skill should I use? Answer only the skill name.'` with isolated configuration.
- Bounded second host command: `gtimeout 45s claude --plugin-dir /private/tmp/loom-retro-acceptance-20261013/loom-workflow --permission-mode plan --permission-prompts none -p '/loom-workflow:retro Review this one fictional coding-session record as a bounded format trial. Event 1: the user asked for lint guidance. Event 2: the assistant ran pnpm lint and got command not found. Event 3: the project README says use uv run ruff check . Event 4: the assistant then ran uv run ruff check . and it passed. Do not read other files or use tools. Produce any supported project recommendation and separate skill candidates with source pointers to event numbers; do not edit files.'`.
- What came back: the first live attempt failed under the sandbox with `Failed to start: listen tcp 127.0.0.1:0: bind: operation not permitted`. An elevated retry started but requested Google authentication and waited for a code; I interrupted it, yielding `authentication failed or timed out`. A separate, bounded Claude CLI attempt loaded the clean plugin with `--plugin-dir`, `--permission-mode plan`, and a fictional four-event session in the prompt, but returned `Not logged in · Please run /login` and an unrecognized-model error. No model answer or retrospective was produced. No private session transcript was sent.
- Evidence: installed `retro/SKILL.md` says to use the current or specified single session, rank recommendations by impact, and include a traceable event pointer. `test_user_invoked_current_or_specified_session`, `test_ranked_recommendations_link_to_observed_source`, and `test_missing_source_limits_claims` passed. These are contract checks, not a captured recommendation.

## 2. Separate project recommendations and skill candidates, without writes

- How I tried it: inspected the installed `retro` skill, ran `test_project_advice_is_separate_from_skill_candidates_and_read_only`, and checked the clean clone's status after validation and installation.
- What came back: the focused test passed; the installed instructions contain separate `Project recommendations` and `Skill candidates` sections and prohibit writes or promotion of a one-session candidate. `git status --short` remained empty in the clean clone. Both live hosts stopped at authentication, so there is no generated output or execution of the read-only workflow to inspect.
- Evidence: `loom-workflow/skills/retro/SKILL.md:9-12,39-59`; `loom-workflow/tests/retro/test_skill_contract.py::test_project_advice_is_separate_from_skill_candidates_and_read_only`.

## 3. Preserve distill-sessions and route each request

- How I tried it: compared the installed router and both skill files with the clean clone; ran routing, catalog, manifest, loader, release, and install-document tests; ran the existing distill-sessions test directory separately.
- What came back: installed copies matched. The targeted test command returned `80 passed in 5.90s`; the distill-sessions command returned `121 passed in 0.48s`. The router has distinct entries for one-session project retro and past-session skill mining. The live routing prompt did not complete because the isolated host required login; the later Claude CLI attempt also lacked login.
- Evidence: `loom-workflow/skills/using-loom-workflow/SKILL.md:13,21`; `loom-workflow/skills/distill-sessions/SKILL.md:2-10`; `loom-code/contract/manifest.yaml:29,36`; installed paths under the isolated HOME. Named routing tests: `test_single_session_retro_and_cross_session_skill_mining_have_distinct_routes`, `test_distill_sessions_contract_still_targets_recurring_skill_issues`.

## Focused test commands and later gate

```sh
PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/retro/test_skill_contract.py loom-workflow/tests/retro/test_routing.py loom-workflow/tests/scripts/test_skill_count.py loom-workflow/tests/scripts/test_release_metadata.py loom-code/tests/test_contract_manifest.py tests/test_loom_skill_description_catalog.py tests/test_agy_install_docs.py loom-code/tests/test_opencode_loader.py -q
# 80 passed in 5.90s

PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/distill-sessions -q
# 121 passed in 0.48s
```

The full package suite was not run here. The planned `finalize-review` gate will run `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` and block its attestation if that suite fails. Its result is not claimed in this report.

## Re-run on 2026-10-13, at `f4fc4d34`

The fix range was `8b858bae..f4fc4d34`. It removed `disable-model-invocation: true` from retro, retained read-only local inspection, added an OpenCode discoverability test, and synchronized release metadata. Because the skill contract and routing surface changed, all three Acceptance lines were re-tested in full.

### Clean setup and focused checks

- `git clone --no-local --no-checkout /private/tmp/loom-retro-20261013 /private/tmp/loom-retro-acceptance-rerun-20261013`, then `git checkout --detach f4fc4d34129a851813e78a9e1a56e0e76a83a649`: succeeded; `git status --short --branch` printed only `## HEAD (no branch)`.
- `agy plugin validate ./loom-workflow`: `[ok]`, `skills: 13 processed`, `hooks: 1 processed`.
- With fresh isolated `HOME=/private/tmp/loom-retro-rerun-home` and `XDG_CONFIG_HOME=/private/tmp/loom-retro-rerun-config`, `agy plugin install ./loom-workflow` returned `[ok]` and `agy plugin list` named `loom-workflow` with `skills` and `hooks`. `cmp` confirmed the installed retro skill exactly matched the fresh clone.
- Focused command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/retro/test_skill_contract.py loom-workflow/tests/retro/test_routing.py loom-workflow/tests/scripts/test_skill_count.py loom-workflow/tests/scripts/test_release_metadata.py loom-code/tests/test_contract_manifest.py tests/test_loom_skill_description_catalog.py tests/test_agy_install_docs.py loom-code/tests/test_opencode_loader.py loom-code/tests/test_write_plan_station_text.py -q` → `118 passed in 9.05s`.
- Existing tool command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/distill-sessions -q` → `121 passed in 1.14s`.
- The full package suite remains the later `finalize-review` check and was not run by this tester.

### 1. Current and specified single sessions

- I made a fictional local fixture with `README.md` and `session.md`. Its seven numbered events show a failed guessed lint command, a successful documented lint command, a failed guessed test path, and a successful corrected test path. The README documents lint and the test directory but omits the test command. The fixture contains no private transcript or credential.
- Explicit Codex trial: `gtimeout 75s /Users/kouko/.local/bin/codex exec --sandbox read-only --ephemeral --ignore-user-config --skip-git-repo-check -C /private/tmp/retro-acceptance-fixture 'Read /private/tmp/loom-retro-acceptance-rerun-20261013/loom-workflow/skills/retro/SKILL.md and follow it exactly. The user explicitly asks for retro of the one fictional coding session in session.md. Read only session.md and README.md from this fixture as needed. Give the retro result in Traditional Chinese. Cite E-number events as source pointers. Do not edit any file. This is synthetic test data only.'`. The default outer sandbox blocked Codex's in-process app-server initialization with `Operation not permitted`; an elevated retry of the same bounded, inner read-only command completed in 26.6 seconds. Codex reported `sandbox: read-only` and read the skill, fixture README, and session with `cat`.
- Captured specified-session answer: `1. **在 README.md 補上明確的測試指令。**` It cited `E3、E5、E6`, explained the failed guess and corrected result, and gave medium confidence because the directory was already documented. It did not propose a duplicate check because existing lint and tests succeeded. This is one ranked recommendation; behavior with multiple ranks was not exercised.
- Current-session trial: `gtimeout 60s /Users/kouko/.local/bin/codex exec --sandbox read-only --ephemeral --ignore-user-config --skip-git-repo-check -C /private/tmp/retro-acceptance-fixture 'Read /private/tmp/loom-retro-acceptance-rerun-20261013/loom-workflow/skills/retro/SKILL.md and follow it exactly. Review only this current conversation as a coding session. Do not read session.md or infer earlier events. This current conversation contains only this request and your subsequent tool calls. Give the result in Traditional Chinese. Do not edit files.'` completed in 57.7 seconds. The answer said `沒有足夠證據支持任何專案改善建議` because only the request and skill read existed. It did not borrow the specified fixture's earlier events.
- Both trials explicitly named the fresh-clone skill file. They prove behavior after explicit loading, not automatic skill selection by the host.

### 2. Separate sections and no writes

- The specified-session answer had `### 專案建議` and `### 技能候選`. The candidate cited `E2、E3、E5`, explicitly said the record did not identify a skill or prove a recurring defect, and did not promote it to a skill edit. The current-session answer had both sections and said neither had supporting evidence.
- Both Codex runs reported `sandbox: read-only`; their visible tool calls were `cat` reads. After the trials, the fresh clone still reported `## HEAD (no branch)` with no changed files. `rg --files --hidden /private/tmp/retro-acceptance-fixture` found only the original `README.md` and `session.md`; their SHA-256 values were `19122c2c3c584099a3c2c5e80ea9d188683ab20833c801302813f60db0ffe9b3` and `4d2428ecb4ba323af302b1c762a41f60eab6be51dab72195d76aeb6f305d5414` respectively.

### 3. Existing distill-sessions and routing

- The installed plugin retained both `retro` and `distill-sessions`. The focused route tests and the OpenCode loader test passed; `test_retro_is_discoverable_as_an_opencode_model_skill` found `loom-workflow:retro` in registered skills. The `121` existing distill-sessions tests passed. The full package suite will run later at `finalize-review` and is not claimed here.
- The live Codex trials loaded retro by an explicit absolute path. They did not exercise automatic host selection for an unnamed one-session request or for a cross-session skill-mining request. Therefore this line remains `partly`.

## Re-run on 2026-10-13, at `b27320f5`

The authorized review-fix range was `6ee7806d..b27320f5`. It changed retro's discovery description, Japanese `振り返り` routing, and its privacy wording about local tool output entering model context. It also changed plugin metadata and focused tests. All three Acceptance lines were affected and re-tested in full. The earlier A1 `works` row had only one recommendation and did not establish impact ordering; this rerun used two supported candidates.

### Clean setup and focused checks

- `git clone --no-local --no-checkout /private/tmp/loom-retro-20261013 /private/tmp/loom-retro-acceptance-pr90-20261013`, then `git checkout --detach b27320f5692a87faf7fc5d79ac6f82cf9e06a908`: succeeded; `git status --short --branch` printed `## HEAD (no branch)` and no changed files.
- `agy plugin validate ./loom-workflow`: `[ok]`, `skills: 13 processed`, `hooks: 1 processed`.
- In fresh isolated `HOME=/private/tmp/loom-retro-pr90-home` and `XDG_CONFIG_HOME=/private/tmp/loom-retro-pr90-config`, `agy plugin install ./loom-workflow` returned `[ok]`; `agy plugin list` showed `loom-workflow` with `skills` and `hooks`; `cmp` confirmed the installed retro file matched the clean clone.
- Focused test command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/retro/test_skill_contract.py loom-workflow/tests/retro/test_routing.py loom-workflow/tests/scripts/test_skill_count.py loom-workflow/tests/scripts/test_release_metadata.py loom-code/tests/test_contract_manifest.py tests/test_loom_skill_description_catalog.py tests/test_agy_install_docs.py loom-code/tests/test_opencode_loader.py -q` → `85 passed in 8.90s`.
- Existing tool command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/distill-sessions -q` → `121 passed in 1.54s`.
- This tester did not run the full package suite. `finalize-review` owns `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, the automated test suite that runs before acceptance and blocks attestation on failure.

### 1. Two ranked improvements from one specified session, plus current-session limit

- Fictional fixture: `README.md` documented `python tools/release.py --dry-run` without its required `RELEASE_CHANNEL`, documented the lint command, and named `checks/` without the test command. `ci-release.md` supplied `RELEASE_CHANNEL=staging`. The one `session.md` had E1–E7: the documented release command failed for missing configuration (E2), then succeeded with the CI setting (E3); a guessed `pytest tests/` failed (E5), then `pytest checks/` passed (E6). The fixture contained no private transcript or credentials.
- Specified-session command: `gtimeout 90s /Users/kouko/.local/bin/codex exec --sandbox read-only --ephemeral --ignore-user-config --skip-git-repo-check -C /private/tmp/retro-pr90-fixture 'Read /private/tmp/loom-retro-acceptance-pr90-20261013/loom-workflow/skills/retro/SKILL.md and follow it exactly. The user explicitly requests a retrospective of the one fictional coding session in session.md. Inspect README.md and ci-release.md as project context. Produce only recommendations supported by this session, rank project recommendations by likely impact, cite E-number source events, separately list skill candidates, and do not edit files. All fixture contents are fictional and contain no private transcript or credentials. Answer in Traditional Chinese.'` → exit 0. Codex reported `sandbox: read-only` and read the skill and three fixture files with `cat`, `rg`, and `nl`; it did not run mutating commands.
- Captured result, in order: `1. **補齊 README 的發版試跑指令，明示必要環境變數。**` with E2/E3, followed by `2. **在 README 補上 pytest checks/。**` with E5/E6. Both included source links, effect, confidence, and limits. The first recommendation addressed a documented release procedure that failed; the second addressed a missing test command while noting the assistant also ignored a documented directory. The ordering is plausible for this fixture, but this one trial is not a general ranking benchmark.
- Current-session command: `gtimeout 75s /Users/kouko/.local/bin/codex exec --sandbox read-only --ephemeral --ignore-user-config --skip-git-repo-check -C /private/tmp/retro-pr90-fixture 'Read /private/tmp/loom-retro-acceptance-pr90-20261013/loom-workflow/skills/retro/SKILL.md and follow it exactly. Review only this current conversation as a coding session. Do not inspect the fixture session.md or assume any earlier coding events. If this conversation has too little development evidence, say so. Answer in Traditional Chinese. Do not edit files.'` → exit 0. It read only the skill and said `目前對話的開發證據不足`; it did not borrow E events from the specified fixture.
- Both trials explicitly named the skill path. This proves behavior after explicit loading, not automatic host discovery for an unnamed request.

### 2. Separate candidates, read-only result, and model-context privacy wording

- The specified-session answer had separate `## 專案建議` and `## 技能候選` sections. The skill candidate cited E2/E5/E6 and said the record did not name the skill in use, so one failure does not establish a recurring skill defect or authorize a skill edit. The current-session answer also kept both sections with no unsupported claim.
- `git status --short --branch` in the clean clone still printed only `## HEAD (no branch)`. `rg --files --hidden /private/tmp/retro-pr90-fixture` found only the three initial fixture files. Their SHA-256 values after trial were `c8c70fdecff5b80a1038ee3d1216d189c1304bdf1955567daa0aa3fd9a89f7f9` (README), `c02426ee3998e28ab18b9f5b101509a639496799975ae58e3ecd4075da2603f5` (CI note), and `170b51115009ba193b61197bf34e0920cb926acaa583c709d163e7635302cbfa` (session). Visible Codex commands only read files, and its inner sandbox was read-only.
- The revised `loom-workflow/skills/retro/SKILL.md:27-33` says local transcript tool output enters model context and may be processed by the host service; it asks for local redaction before tool output where feasible and a redacted excerpt or stated limit otherwise. `test_sensitive_transcript_handling_names_model_context_boundary` passed. This is a contract check; no real secret or sensitive session was used, so actual redaction behavior was not tested.

### 3. Distill-sessions and request routing

- The installed plugin retained `retro` and `distill-sessions`; the latter's skill file had no changes in `6ee7806d..b27320f5`. Its `121` focused tests passed. The router now distinguishes Japanese `振り返り` used for a progress recap from `振り返り` requesting project-development improvements. `test_single_session_retro_and_cross_session_skill_mining_have_distinct_routes` and `test_japanese_furikaeri_routes_by_requested_outcome` passed within the `85` focused tests.
- `test_retro_is_discoverable_as_an_opencode_model_skill` also passed. The live Codex trials still loaded retro by explicit path. Automatic host selection for unnamed one-session and cross-session requests was not observed, so A3 remains `partly`.
