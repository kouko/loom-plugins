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

## Re-run on 2026-11-11, at 75f9630f564b2aea29222ada7dbf59cbbcc83c50

Reviewed fix range `fa1055d1866c762b24c6d9181047a805bcb412fa..75f9630f564b2aea29222ada7dbf59cbbcc83c50`. Functional repair `22ff4ee5` replaces five Codex discriminator set-membership checks with tuple-membership checks, preventing array/object discriminator TypeError. Ingestion can affect all three rows, so none was carried over. The first-run evidence above remains intact.

Setup: fresh local clone at `/private/tmp/retro-acceptance-75f9630`, checkout of the full SHA above. Followed the same README setup, rerunning `uv run --offline --isolated --with-requirements requirements-package-tests.lock python loom-workflow/skills/skill-retro/scripts/main.py --help` successfully with authorized cache access. Final status was clean and rev-parse returned exactly the tested SHA. No real histories or product files were modified.

Reran `python3 /private/tmp/retro_acceptance_probe.py` after changing only its clean-clone target and adding the malformed-record smoke below. It created fresh temporary real repositories and a worktree, using the same synthetic data shapes and isolated-root CLI commands documented above. Exit 0:

- 1: re-tested — both adapters, repository/subdirectory/worktree grouped as one; distinct repositories counted as two; all known cases had empty unknown lists.
- 2: re-tested — both adapters, partial sessions retained one known project and disclosed all three affected sessions; all-unknown cases returned zero projects, cross_project_norm 0.0 and low confidence. Missing Git returned zero projects and three unknown sessions per target, exit 0.
- 3: re-tested — both adapters, equal-frequency/time/friction comparison returned cross_project_norm 1.0 versus 0.5 and high versus low confidence. Binding top-1 selected `loom-code:distinct`. All six invocation source locations per adapter (12 total) again matched their raw JSONL records and canonical project directories.

Captured summary:

```text
claude known: distinct=2/high/1.0; single=1/low/0.5; winner=loom-code:distinct; source_lines_checked=6; seconds=0.10
codex  known: distinct=2/high/1.0; single=1/low/0.5; winner=loom-code:distinct; source_lines_checked=6; seconds=0.06
claude partial: projects=1 confidence=low unknown=[partial-0,partial-1,partial-2]
codex  partial: projects=1 confidence=low unknown=[partial-0,partial-1,partial-2]
claude unknown: projects=0 confidence=low cross_project_norm=0.0 unknown_count=3
codex  unknown: projects=0 confidence=low cross_project_norm=0.0 unknown_count=3
claude empty: top_skills=[] subagent_payload=[]
codex  empty: top_skills=[] subagent_payload=[]
claude missing-git: projects=[0,0] unknown_counts=[3,3]
codex  missing-git: projects=[0,0] unknown_counts=[3,3]
```

Additional regression smoke: prefixed three Codex sessions with a top-level record whose type was respectively `[]`, `{}`, or `["session_meta"]`, then valid session_meta and Skill invocation from repository A. Actual CLI exit 0; three usable sessions, one known project, low confidence, no unknown sessions. Every emitted invocation source_line was 3, proving malformed records did not prevent later usable records or displace provenance.

Reran `python3 /private/tmp/retro_timeout_probe.py` against the new clone, using the same eight-second fake Git and three sessions sharing one cwd. Output:

```json
{"adapter":"claude","seconds":5.05,"projects":0,"unknown_count":3,"exit":0}
{"adapter":"codex","seconds":5.06,"projects":0,"unknown_count":3,"exit":0}
```

No findings from this re-run; no dismissed important findings were supplied. Full package tests remain delegated to finalize-review and were not run by this tester. Host installation/automatic routing, downstream model proposals, duplicate-session correctness and threshold overrides remain outside the verified boundary.

## Re-run on 2026-11-11, at 9013867c5d90d609c72bf5bf1091745d97945ca4

Independent integration re-test after merging main and resolving the shared README version table to retain loom-code 3.65.0 and loom-workflow 5.21.0. Inspected `5d7fb47e2692d69658fff7ee4a0fcb09f8d9be1c..9013867c5d90d609c72bf5bf1091745d97945ca4`: no loom-workflow changes; merged Stop-hook changes belong to loom-code. Requirements are unchanged. All three rows were nevertheless re-tested across both adapters, with no carried-over row and no production edits.

Setup: `git clone --quiet --no-hardlinks /Users/kouko/GitHub/loom-plugins /private/tmp/retro-acceptance-9013867`, then checkout of the full tested SHA. Read root README Development and skill-retro README Quick start. Following the documented Python CLI entry, `python3 loom-workflow/skills/skill-retro/scripts/main.py --help` exited 0 and advertised isolated transcript roots and top-N. Final `git status --short` was empty; `git rev-parse HEAD` returned the exact tested SHA.

Inspected and copied the earlier independent harness to `/private/tmp/retro_acceptance_integration_probe.py`, changing only its clean-clone target. Executed `python3 /private/tmp/retro_acceptance_integration_probe.py`; exit 0, captured output `/private/tmp/retro-acceptance-9013867-output.json`. All fixtures were fresh synthetic histories and real temporary Git repositories/worktrees; explicit roots excluded live histories.

- 1: re-tested — Claude and Codex each grouped repository A, its subdirectory and linked worktree into one project; A and B produced two projects. Known cases had no unknown sessions.
- 2: re-tested — both adapters returned one known project and three disclosed unknown sessions for partial attribution, then zero projects, low confidence and cross_project_norm 0.0 for wholly unknown attribution. Missing Git returned zero known projects and three unknown sessions for each target.
- 3: re-tested — equal frequency/time/friction cases produced cross_project_norm 1.0 versus 0.5 and high versus low confidence; binding top-1 selected `loom-code:distinct` on both adapters. Six invocation source locations per adapter (12 total) matched raw records and canonical project directories. Duplicate-session correctness remains unclaimed.

Captured summary:

```text
claude known: distinct=2/high/1.0; single=1/low/0.5; winner=loom-code:distinct; source_lines_checked=6; seconds=0.08
codex  known: distinct=2/high/1.0; single=1/low/0.5; winner=loom-code:distinct; source_lines_checked=6; seconds=0.08
claude partial: projects=1 confidence=low unknown=[partial-0,partial-1,partial-2]
codex  partial: projects=1 confidence=low unknown=[partial-0,partial-1,partial-2]
claude unknown: projects=0 confidence=low cross_project_norm=0.0 unknown_count=3
codex  unknown: projects=0 confidence=low cross_project_norm=0.0 unknown_count=3
claude empty: top_skills=[] subagent_payload=[]
codex  empty: top_skills=[] subagent_payload=[]
claude missing-git: projects=[0,0] unknown_counts=[3,3]
codex  missing-git: projects=[0,0] unknown_counts=[3,3]
codex malformed-discriminator: projects=1 confidence=low sessions=3 source_line=3 exit=0
```

Copied the inspected timeout harness to `/private/tmp/retro_timeout_integration_probe.py`, changing only its clean-clone target, and ran `python3 /private/tmp/retro_timeout_integration_probe.py`. Three sessions at the same location and the existing temporary eight-second fake Git produced:

```json
{"adapter":"claude","seconds":5.04,"projects":0,"unknown_count":3,"exit":0}
{"adapter":"codex","seconds":5.05,"projects":0,"unknown_count":3,"exit":0}
```

No findings; no dismissed important findings were supplied. No full package suite ran in this tester. The station will run the unchanged finalize-review suite command documented above; that future check is not a completed acceptance result. Host installation/automatic routing, downstream proposals, duplicate sessions and threshold overrides remain unverified. Previous evidence is retained above.

## Re-run on 2026-11-11, at 3a131c70020c6dccd211ef24f81acb106ae58f81

The owning station reported that its first integration package run found three failures caused by one additional stale README version string, then committed that correction. Inspected `9013867c..3a131c70`: only README.md changed, one insertion and one deletion. No skill-retro behavior changed. The preceding acceptance run remains evidence at its original SHA and is not represented as a full-suite pass.

Fetched the local source branch into the clean clone above and checked out the exact new SHA. Repeated the documented CLI `--help` load from that clone (exit 0), with output at `/private/tmp/retro-acceptance-3a131c70-help.txt`; its final status stayed clean. Re-executed both inspected temporary harnesses unchanged against the clone at this SHA. Both exited 0. Captured primary output: `/private/tmp/retro-acceptance-3a131c70-output.json`.

- 1: re-tested — both adapters still grouped repository/subdirectory/worktree as one and distinct repositories as two; unknown lists empty in known cases.
- 2: re-tested — both adapters retained one known project plus three unknown sessions in partial cases; all-unknown cases returned zero projects, low confidence and cross_project_norm 0.0. Missing Git returned zero projects and three unknown sessions for each target.
- 3: re-tested — both adapters returned two/high/1.0 versus one/low/0.5, selected `loom-code:distinct` under binding top-1, and matched all six raw source records per adapter. Known previews took 0.12s each.

Empty inputs again returned empty output lists on both adapters. Malformed Codex discriminators again preserved three valid later sessions, one project, low confidence and source line 3. Timeout output:

```json
{"adapter":"claude","seconds":5.05,"projects":0,"unknown_count":3,"exit":0}
{"adapter":"codex","seconds":5.06,"projects":0,"unknown_count":3,"exit":0}
```

All three rows are re-tested and work; no findings. The full suite is still delegated to the owning station and finalize-review, not claimed here. Existing host/model/deduplication limitations and absence of dismissed important findings remain unchanged.
