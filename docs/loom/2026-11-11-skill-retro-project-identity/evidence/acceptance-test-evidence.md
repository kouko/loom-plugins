# Skill-retro project identity — acceptance test evidence

Tried on 2026-11-11, in a clean copy of the project at fa61939d1a414dd807758f80dc28cad50f372134.

## Setup and isolation

Fresh clone: `git clone --quiet --no-hardlinks . /private/tmp/retro-acceptance-fa61939`, followed by checkout of the full tested SHA. Final `git status --short` was empty; `git rev-parse HEAD` printed the tested SHA. Python was 3.12.11.

Read root README Development and skill-retro README Quick start. Loaded the actual entry point with `uv run --offline --isolated --with-requirements requirements-package-tests.lock python loom-workflow/skills/skill-retro/scripts/main.py --help`: exit 0, advertised both explicit transcript roots, facets root and top-N. The initial sandbox attempt could not acquire the uv cache lock; the authorized escalation succeeded. No installation or private transcript access was needed for the documented local preview.

The independent harness ran `python3 /private/tmp/retro_acceptance_probe.py` against the clean clone. It initialized two real empty Git repositories with fixture-only local author settings and added a detached linked worktree. All input JSONL was synthetic. Each invocation of main supplied either `--project-root <synthetic Claude directory>` or `--codex-root <synthetic Codex directory>`, plus `--facets-root <empty temporary directory>` and `--top-n 20` or `--top-n 1`. Thus unspecified live transcript roots were excluded. No model was dispatched.

Claude records were assistant messages with a `Skill` tool_use, sessionId, timestamp and cwd. Codex records were session_meta/turn_context with cwd followed by response_item/function_call named Skill with JSON arguments. Timestamp was fixed at `2026-11-11T00:00:00Z`. Three distinct sessions per target satisfied the unchanged default threshold. The first harness attempt incorrectly expected a top-level skill_name and stopped with KeyError; corrected only the temporary harness to read the CLI's aggregate_record wrapper, then reran successfully. No product edits occurred.

## 1. Same repository, subdirectories and worktrees count once; different repositories stay distinct

For each adapter, `loom-code:single` had three distinct sessions at repository A, its subdirectory, and its linked worktree. `loom-code:distinct` had three sessions at A, B and A's linked worktree. Both targets had one invocation per session and no friction signal.

Captured assertion summary, exit 0:

```text
adapter=claude projects={distinct:2,single:1} confidence={distinct:high,single:low}
adapter=codex  projects={distinct:2,single:1} confidence={distinct:high,single:low}
unknown_project_sessions=[] for both targets on both adapters
```

The returned project identities were the actual canonical A/.git and B/.git directories; A/sub and the linked worktree both returned A/.git. The CLI read real Git metadata rather than mocked identity results.

## 2. Missing and partial attribution do not create known projects or unsupported high confidence

For each adapter, three partial sessions invoked the same target first from A, A/sub or its linked worktree, then respectively with null cwd, relative cwd or a nonexistent absolute cwd. Codex used turn_context to replace the initial cwd; Claude carried the new cwd directly on each record. A second dataset contained three entirely unknown sessions with those invalid locations.

Captured assertion summary, exit 0:

```text
adapter=claude partial projects=1 confidence=low unknown=[partial-0,partial-1,partial-2]
adapter=codex  partial projects=1 confidence=low unknown=[partial-0,partial-1,partial-2]
adapter=claude all-unknown projects=0 confidence=low cross_project_norm=0.0 unknown_count=3
adapter=codex  all-unknown projects=0 confidence=low cross_project_norm=0.0 unknown_count=3
```

The partial sessions remained in the unknown list despite also having a known invocation. Invalid later context did not retain stale attribution.

## 3. Actual preview ranking, confidence and provenance reflect known projects

Used the paired, equal-frequency datasets from row 1. Full preview returned cross_project_norm 1.0 for the two-project target and 0.5 for the one-project target on each adapter. Reran with the binding `--top-n 1` cut: only `loom-code:distinct` remained, for both adapters. Frequency, timestamps and friction were equal, isolating the project contribution.

Checked all six emitted invocation events per adapter: opened each returned source_path at its one-based source_line and confirmed the original record type; checked cwd against the four supplied locations and project_path against A/.git or B/.git. Twelve source records matched. Both CLI calls exited 0. No duplicate-session behavior was tested or claimed fixed.

## Additional preview flows

Although the intent is engineering rather than product, all retained preview cases were exercised:

| Case | Actual result |
| --- | --- |
| Known data | Both adapters exit 0; two canonical identities versus one; unknown lists empty. |
| Incomplete data | Both adapters exit 0; affected sessions disclosed and no unsupported high confidence. |
| Empty | Both adapters exit 0 with top_skills=[] and subagent_payload=[]. |
| In progress | Ordinary paired previews completed in 0.07s Claude / 0.06s Codex; no new interaction. |
| Git unavailable | Executed main with an absolute Python path and PATH pointing to a nonexistent directory; both targets on both adapters returned zero projects, low confidence and three unknown sessions, exit 0. |
| Git timeout / repeated cwd | Supplied a temporary git executable that sleeps eight seconds. Three distinct sessions shared one existing cwd. Claude exited 0 in 5.05s and Codex in 5.06s, each with zero projects and three unknown sessions. One bounded lookup rather than three sequential waits demonstrates run-local cache reuse. |

Timeout command: `python3 /private/tmp/retro_timeout_probe.py`. Its subprocess command was the same preview with explicit isolated roots and PATH=/private/tmp/retro-timeout-bin. The fake executable contained only a shell shebang and `/bin/sleep 8`; no product files were replaced. Observed output:

```json
{"adapter":"claude","seconds":5.05,"projects":0,"unknown_count":3,"exit":0}
{"adapter":"codex","seconds":5.06,"projects":0,"unknown_count":3,"exit":0}
```

## Verification boundary and review handoff

No full package suite was run by this tester. The owning station states package-tests is not skipped and finalize-review will execute `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; this future check is not reported as a completed acceptance result. Report rows rely on the actual independent CLI runs above.

Host installation, automatic skill triggering, downstream analyst/model proposal generation, duplicate-session ranking and the separately retained threshold-override issue were not verified. No important-or-higher implementation finding was supplied as dismissed. All data fixtures were synthetic; no private session content or user data was read or changed.
