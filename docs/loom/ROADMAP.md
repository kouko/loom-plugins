# Roadmap

Cross-session planning summary for loom-plugins. Detail lives in each change's
intent, spec, plan and PR; this file only says what is next and why.

## Loom-code fixes from dogfooding in a dbt repo (started 2026-11-20)

**Goal:** remove the loom-code traps a maintainer hit while running loom end to
end in a downstream dbt repository, so the same flow works without
workarounds in any repository. **Done when** every open item below is fixed
or explicitly dropped with a reason.

### Done

| Item | Outcome | Evidence |
|---|---|---|
| Keep the worktree when landing | `land --accepted-by <name> --keep-worktree` merges with the same gates and keeps the worktree and both branches | PR #173, loom-code 3.88.0 |
| Record kept worktrees | the keep is recorded in git config; `land --sweep` lists kept changes on a `kept` line it never removes; ship asks before cleaning earlier work | PR #177, loom-code 3.89.0 |

### Next

**Acceptance report commit line gets translated (do next).** The acceptance
report template and `loom-code/agents/acceptance-tester.md` tell the tester to
write in the user's language, but `finalize-review` only accepts the English
`Tried on <date>, in a clean copy of the project at <sha>.` line, so a
translated line blocks with `intake.commit-identity` (raised at
`loom-code/scripts/loom_checker/command_handlers/finalize.py` ~446-448 through
`report_tested_commit` in `loom-code/scripts/loom_checker/rule_checks/commit_identity.py`).
Affects every non-English user. Current workaround: tell the tester to keep
that one line in English. Ride these small fixes on the same branch:

- `docs/loom/memory/a-graduated-probe-keeps-its-concern-line.md`: the "Why"
  paragraph credits graduation discovery; the refusal actually comes from the
  file being declared as an adversarial artifact (`check_adversarial_proportionate`
  in `loom-code/scripts/loom_checker/probes.py`).
- `docs/loom/2026-11-23-record-kept-worktrees/spec.md` Design decision 2 does
  not describe the rule that a candidate whose PR head is the tip of a recorded
  local branch is also kept.
- The keep-record read in `land --sweep` (`git config --get-regexp`) fails open
  on a timeout or OS error; consider blocking instead.

### Later (unordered)

| Item | Problem | Known workaround |
|---|---|---|
| Suite timeout in finalize-review | the complete suite runs under a 600 s default (`PROBE_RUN_TIMEOUT` in `loom-code/scripts/loom_checker/probes.py`); the only override is the undocumented `LOOM_PROBE_RUN_TIMEOUT`, with no KICKOFF-DEFAULTS key and no hint in the timeout error | set `LOOM_PROBE_RUN_TIMEOUT=1500` |
| Adversary programs that need external infra | `loom-code/agents/adversary.md` offers the no-program record only when every attack held; it says nothing about probes that need a database or network | tell the adversary to record no program with the reason |
| Package suite needs PyYAML in uv's base interpreter | launcher tests symlink their fake runtime to the base interpreter, so the documented `package-tests` command fails locally when that base lacks PyYAML (CI is unaffected); see `docs/loom/memory/the-package-suite-needs-pyyaml-in-uvs-base-interpreter.md` | set `UV_PYTHON` to an interpreter whose base has PyYAML |
| Flaky timing tests | two 5 s timeout tests in `loom-code/tests/test_external_review.py` failed once inside finalize-review under heavy machine load | re-run finalize-review |
| Renamed kept branch | after a local `git branch -m`, sweep shows the kept change as "no worktree" and `land --cleanup <old>` removes only the old-name remote; loom cannot fully remove it (nothing is deleted wrongly) | remove the worktree and branch with git |
| Root-only PRs can never merge | main's branch protection requires the `pytest + knowledge-drift + codex-manifest-drift` check, but `.github/workflows/loom-code-ci.yml` only runs on listed paths (`loom-code/**`, `docs/loom/**`, `scripts/**`, plugin manifests, …), so a PR touching only root files never reports that check and stays BLOCKED (found on PR #179) | place the file under a triggering path (this roadmap moved to `docs/loom/` for that reason), or merge with admin rights |

### Open questions

- None. Each item still needs its own intent confirmation before work starts.
