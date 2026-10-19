# External CLI contract grounding — 2026-10-08

Scope: read-only documentation and local `--help` inspection. No model-backed
discovery, probe, or review was run for this evidence.

| Executor | Command surface grounded | What remains unproved |
|---|---|---|
| Antigravity | [Headless mode](https://antigravity.google/docs/cli/headless/) documents `agy -p <prompt>`, `agy models`, explicit `--model` and `--effort`, and nonzero rejection of an unknown model. Local `agy --help` lists `--add-dir` as adding a workspace directory, plus `--mode`, `--sandbox`, and `--disable-slash-commands`. The [CLI reference](https://www.antigravity.google/docs/cli/reference/) documents the interactive `/add-dir` workspace action. The repo's `loom-code/README.md` records that print mode needs an absolute `--add-dir` path; W5-02 passes the already validated absolute review root to each probe and review. | `--add-dir` and successful process exit do not prove filesystem confinement. The text response does not independently identify effective model or effort. The official headless page lists low/medium/high effort while current local help also lists xhigh/max; a bounded run must accept the requested pair before review. |
| Codex | [App-server guidance](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server) names `model/list` as a selector source, warns its catalog is not an entitlement check, and specifies `name`, `title`, and `version` in initialize `clientInfo`. The script supplies all three. Local `codex app-server --help` confirms stdio transport; local `codex exec --help` lists `--model`, `--sandbox`, `--ephemeral`, and `--skip-git-repo-check`. | A listed model is not account entitlement. The run's CLI stderr header is the observed model/effort evidence in this executor; this task did not perform a live run. |
| Claude Code | Local `claude --help` lists `--model`, `--effort`, `--permission-mode`, `--permission-prompts`, `--tools`, JSON output, and no-session-persistence flags used by the script. | A successful explicit invocation and `modelUsage` identify the accepted model family, not independently observed effective effort. This task did not perform a live run. |

The regression tests mock Antigravity probe and review and assert that each
command includes `--add-dir /repo`, keeps the prompt immediately after `-p`,
and leaves stdin empty. They reject a relative review root before any executor
call and check the Codex initialize `clientInfo` shape. `/repo` is a test value,
not a live path or sandbox claim.
