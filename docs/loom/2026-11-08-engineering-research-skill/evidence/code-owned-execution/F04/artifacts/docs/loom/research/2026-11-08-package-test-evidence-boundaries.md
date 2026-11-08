---
title: "What the executor receipt and package research actually establish"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# What the executor receipt and package research actually establish

## Question and scope

Can the existing executor receipt and research file justify claiming that all package tests and CI passed and that the entire source/bundle is traceable? This assessment concerns only the supplied temporary fixture on 2026-11-08. It does not perform acceptance, execute tests, inspect remote services, or verify a deployment. The earlier root-discovery question is preserved in its [existing record](2026-11-08-package-test-roots.md); this independently answerable evidence question warrants a separate record.

## Method and rationale

Inspect the actual local receipt, prior record and archived copy, connected runner source and relevant test definitions; recompute SHA-256; resolve Markdown links lexically within the fixture; inspect permitted local Git history and status. Static artifact inspection directly distinguishes process completion, source facts, and missing runtime evidence. No experiment or evaluation framework is needed. Stop once the proposed claim can be bounded. No commands embedded in the sample artifacts were executed, and no targets outside the fixture were read.

## Findings and evidence

### Executor completion is not a package-test result

The [genuine existing receipt](../../../sample-receipt.json), ID `B02`, records a `codex exec --ephemeral ... --json` command, `exit_code: 0`, `timed_out: false`, and one added research file. This is a recorded successful executor process exit, not the exit of pytest, the package runner, or CI. It supplies no package-test output, collection inventory, pass/fail counts, or CI job results. Its `source_unchanged` and `auth_symlink_removed` fields are historical receipt assertions, not newly observed execution results here. Requested model/provider/effort fields are present, but `server_confirmed_model` is null; an actually confirmed model identity cannot be inferred. Historical absolute paths and thread identifiers are metadata, not authorization or evidence retrieved from those locations.

### The existing research supports a narrow source conclusion

The [existing record](2026-11-08-package-test-roots.md) explicitly states static inspection only, no executed tests, and no CI/deployment claim. `status: concluded` describes the research question's completion, not test success or user acceptance. Its bytes equal the [archived copy](../../../snapshots/original-research.md), as directly compared with Python `read_bytes()`.

Inspected implementation: [runner](../../../src/scripts/run_package_tests.py), `TEST_ROOTS` at line 53, `_tests_session` at lines 76–85, shell discovery at lines 88–95, workflow sessions at lines 98–113, preset construction at lines 116–150, and `main` at lines 153–176. These support the four declared roots (`tests`, `loom-code/tests`, `loom-design/tests`, `loom-workflow/tests`) and exclusion of each root's direct `local/` subtree in the applicable preset paths. Explicit-argument mode forwards arguments to pytest without adding those exclusions. This does not establish the behavior of bare pytest or all other invocation modes.

The connected discovery path calls [repository helpers](../../../src/loom-code/scripts/repo_files.py), `nested_worktrees` and `nested_repositories` at lines 73–120, through [Git invocation handling](../../../src/loom-code/scripts/git_exec.py), `run_git`. These add environment-dependent foreign-subtree exclusions; they do not establish that any test ran. The runner defines five groups, including Mermaid commands at lines 139–145 beyond Python root discovery. [Test definitions](../../../src/tests/test_run_package_tests.py), lines 222–235 and 285–311, corroborate the intended roots/local exclusion. Their presence is not a test result. The CI-related test at lines 187–197 refers to workflow files absent from this minimal snapshot; it cannot substitute for inspecting actual CI configuration or results.

### Hash correspondence is partial and explicit

[Provenance](../../../provenance.json) attributes the snapshot to original revision `d5a7f0da247214bdb9c61fe90c550256432e5f76`, with the same locally recorded origin/main and `remote_freshness: not checked`. All four supplied source files match their recorded SHA-256 values. All five listed skill artifacts were also hashed; two differ.

| Fixture path | SHA-256 comparison with provenance |
| --- | --- |
| `src/scripts/run_package_tests.py` | Match: `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` |
| `src/loom-code/scripts/repo_files.py` | Match: `62333168fb9eacabb6877d0f185f08081175d8681444465173b18d712ca26399` |
| `src/loom-code/scripts/git_exec.py` | Match: `9c721b8e2f8fae0e4c31da5d6ab41b42e0ae4eeb8cecbf164a36fce7dd61e7c7` |
| `src/tests/test_run_package_tests.py` | Match: `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28` |
| `skill/engineering-research/SKILL.md` | Mismatch: expected `71b0049dc3d644c5717087fdb49907c0cc1bccf108cfbeeca2519dbe49e4a029`; actual `5f2880b87f395e70ab28f5852e2aade303964c92a345733a4c6c268b717bf716` |
| `skill/engineering-research/references/research-methods.md` | Match: `bfada6dddb9ae104ddc3a7e48c3a701a1eb2ea3f0955cd1f3424a41e6a668ca5` |
| `skill/engineering-research/references/source-policy.md` | Match: `c9424edd2191c7ead231a82da98ae3f35c504a00454c1338512313a1d7fd16c3` |
| `skill/engineering-research/references/structured-relations.md` | Match: `dc0c65ab06534a369ee02fa76ed8d8b9d59769ee5578552c7da19a6888808d1d` |
| `skill/engineering-research/templates/research.md` | Mismatch: expected `daa27b500b5280e0529deb0781361759c0e9c32b1d88c0958a3df8aa651f16cc`; actual `62757b98a15cb64caadbba067803864e1297fbabbacd0162eba1d88e2cafa69e` |

Actual verification used a local Python standard-library inspection script: for each provenance entry, `hashlib.sha256(path.read_bytes()).hexdigest()` was compared with `entry['sha256']`, prefixing source entries with `src/` and skill entries with `skill/engineering-research/`. Results: 4/4 source matches, 3/5 skill matches. This checks byte correspondence with the supplied manifest, not independent authentication of the original commit, completeness of its tree, or execution of that revision. The cause and timing of the two skill differences are unknown; neither artifacts nor manifest were changed to force agreement.

### Link validity depends on the record's location

The existing record's three relative links resolve within this fixture to existing provenance, runner, and test-definition files. Its cited line ranges were inspected and support the narrow conclusions. The identical archived copy retains the same relative strings, but all three resolve outside the fixture from `snapshots/`; those targets were not accessed. The archived copy is useful preserved text, but its links are not usable fixture evidence links from that location. This new record links directly to the actual in-fixture evidence. No remote link or remote freshness was checked.

### Cleanup evidence has a separate local lifecycle scope

[Fixture cleanup receipt](../../../fixture-cleanup.json) records `git status --porcelain`, exit 0, empty stdout, cleanup destination `.`, and post-merge main revision `4959e620a78e15678a3cc2a8a0c18f79de58dc73`. It states that no linked worktree or generated temporary build artifact was created and the topic branch was retained. This supports only the recorded temporary-fixture lifecycle conditions; it proves neither package tests nor real-host/release/cache/Vault cleanup.

Read-only local `git log -3 --format='%H %P %s'`, `git branch --list`, and `git show --stat --oneline HEAD` corroborated main at that revision, with parents `3236024bd97f03b25f97fb7fed95bc45d00bd423` and `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`, and retained branch `research-fixture` at the latter. These are harness history, not the original project's deployment or merge evidence. Before writing this assessment, a fresh `git status --porcelain` returned `?? fixture-cleanup.json` and `?? skill/`. Thus the working tree was not currently clean, even though the receipt records an earlier clean check; this difference does not establish that the historical check was false. Saving this assessment adds a further untracked research artifact. No cleanup or branch removal was performed.

## Decision impact

Permitted statement: “The supplied receipt records successful completion of an executor process. Static inspection supports the declared package roots and preset local-test exclusions. The four source snapshot hashes match the supplied provenance attributed to the recorded original revision, and the existing research record's local evidence links resolve.”

Do not claim that all package tests or CI passed, that the full repository/deployment was verified, that the entire skill bundle matches provenance, that the server confirmed the requested model, or that all archived links/current worktree cleanliness were verified successfully. These conclusions do not constitute user acceptance, publication authorization, or release approval.

## Limitations and open questions

No test or runner invocation, network request, app access, external model execution, installation, publication, commit, or Vault write occurred. Missing evidence includes actual package/CI execution logs tied to an exact revision and environment, full CI configuration and test surface, independently checked upstream freshness, and an explanation of the skill hash mismatches. Those gaps remain unresolved under the user's constraints. The original research, archived snapshot, sources, provenance, sample receipt, cleanup receipt, and skill bundle were preserved unchanged.
