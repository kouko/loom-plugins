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
