---
title: "Can the existing research note move without losing source traceability?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Can the existing research note move without losing source traceability?

## Question and scope

Assess a future move of `docs/loom/research/2026-11-08-package-runner-exclusions.md` to `docs/loom/example-change/research/` within the same repository layout. This is an assessment only: there is no active change. The provided specimen remains at its original relative location inside `samples/migration/`. No original note was moved, edited or copied.

Evidence is limited to supplied files. The source snapshots represent recorded commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`, not a full checkout, deployed system or CI result. Original repository paths in provenance are identifiers only; they were not accessed. No network, apps, external models, agents, installations, repository initialization, commits, pytest or npm execution were used.

## Method and rationale

Use staged migration analysis with read-only old/new path comparison and artifact inspection, following the invoked [engineering-research skill](../../../skill/engineering-research/SKILL.md), its [evaluation guidance](../../../skill/engineering-research/references/evaluation-selection.md), [methods](../../../skill/engineering-research/references/research-methods.md) and [source policy](../../../skill/engineering-research/references/source-policy.md). The mandatory invariants are identical evidence targets and bytes, meaningful anchors, preserved historical metadata/provenance, and no broken consumers after a future cutover. Path arithmetic and hashes settle the supplied links; a runtime experiment is unnecessary. Stop at a bounded recommendation because the complete note and its consumers are unavailable.

## Findings

**An unchanged move cannot preserve these links.** All seven supplied relative links resolve today to `samples/migration/src/…`. At the proposed destination, the unchanged `../../../src/…` resolves instead to `samples/migration/docs/src/…`, which does not exist. Adding one parent traversal, producing `../../../../src/…`, restores the exact original target for every link. This result also applies to the equivalent layout without the `samples/migration/` prefix, provided the repository tree otherwise stays fixed.

| Row / link | Source suffix under `src/` | Fragment | Inspected target line | Required destination URL |
| --- | --- | --- | --- | --- |
| E1 runner | `scripts/run_package_tests.py` | `#L153` | `def main(argv: list[str]) -> int:` | `../../../../src/scripts/run_package_tests.py#L153` |
| E2 repo_files | `loom-code/scripts/repo_files.py` | `#L97` | `def nested_repositories(root: Path \| str) -> list[Path]:` | `../../../../src/loom-code/scripts/repo_files.py#L97` |
| E3 nested_worktrees | `loom-code/scripts/repo_files.py` | `#L73` | `def nested_worktrees(root: Path \| str) -> list[Path]:` | `../../../../src/loom-code/scripts/repo_files.py#L73` |
| E4 git_exec | `loom-code/scripts/git_exec.py` | `#L50` | `def run_git(` | `../../../../src/loom-code/scripts/git_exec.py#L50` |
| E5 command construction | `scripts/run_package_tests.py` | `#L68` | `def _holds_tests(folder: Path, skip: tuple[Path, ...] = ()) -> bool:` | `../../../../src/scripts/run_package_tests.py#L68` |
| E6 test definitions | `tests/test_run_package_tests.py` | `#L119` | `def test_targets_unchanged_without_nested_worktree(tmp_path: Path) -> None:` | `../../../../src/tests/test_run_package_tests.py#L119` |
| E7 ordering-related tests | `tests/test_run_package_tests.py` | `#L22` | `def test_runner_exit_code_is_nonzero_when_a_later_group_fails(tmp_path: Path) -> None:` | `../../../../src/tests/test_run_package_tests.py#L22` |

The anchor lines exist and match the named evidence entry points. E5 begins at a helper within the broader command-construction range; E6 begins at the baseline test within the broader test range. These are existing citation scopes, not reasons to rewrite the research conclusions during a move. The cited ranges also fit the file lengths: runner 180 lines, repo_files 172, git_exec 88, tests 331. A `#L…` fragment is a line-number convention, not a Python-defined anchor. File existence and correct line numbers do not establish that every Markdown renderer implements navigation to that fragment. No renderer was run.

**Source provenance survives only if retained explicitly.** Both manifests record the same repository identity, HEAD, locally recorded origin/main and four source hashes. Remote freshness is explicitly “not checked.” All eight file/hash comparisons passed (four in each snapshot). This supports byte identity against the supplied manifest; it does not independently authenticate the manifest or the original Git history.

The [root manifest](../../../provenance.json) additionally describes extraction of the original full note: frontmatter/title lines 1–10 and verbatim evidence-link rows, without its original findings/conclusions. It records original-note SHA256 `dcbf5ea5573cd922f1f56b764d65ec10d481d54925f578cc195a575e10b9272b`. The [migration manifest](../../../samples/migration/provenance.json) lacks that note-extraction entry, so the two manifests are not byte-identical. The supplied excerpt hashes to `f2392d0855416ff2e4979dec4d9f6b5f50dae7f01c2fa06df1b9e0ea0a79b256`; it must not be represented as the complete original note or expected to match its historical full-note digest. A future link edit likewise changes a note's digest without changing source provenance; retain historical digests and label new digests separately.

## Evidence

The directly inspected [note excerpt](../../../samples/migration/docs/loom/research/2026-11-08-package-runner-exclusions.md) supplies seven Markdown URLs and concluded metadata (`created` and `updated`: 2026-11-08; no `change`). Anchor contents were read in the [runner](../../../samples/migration/src/scripts/run_package_tests.py#L153), [repository helper](../../../samples/migration/src/loom-code/scripts/repo_files.py#L97), [Git helper](../../../samples/migration/src/loom-code/scripts/git_exec.py#L50) and [test definitions](../../../samples/migration/src/tests/test_run_package_tests.py#L119). These are source observations, not executed behavior. This investigation does not revalidate the original package-runner research conclusions.

| Manifest source path (relative to each `src/`) | Expected and observed SHA256 in both snapshots |
| --- | --- |
| `scripts/run_package_tests.py` | `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` |
| `loom-code/scripts/repo_files.py` | `62333168fb9eacabb6877d0f185f08081175d8681444465173b18d712ca26399` |
| `loom-code/scripts/git_exec.py` | `9c721b8e2f8fae0e4c31da5d6ab41b42e0ae4eeb8cecbf164a36fce7dd61e7c7` |
| `tests/test_run_package_tests.py` | `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28` |

Read-only commands used: `cat` for skill/resources/manifests/excerpt; `nl -ba … | sed -n …` for target lines; `rg --files` for the supplied inventory; and `rg -n '2026-11-08-package-runner-exclusions|example-change|#L(153|97|73|50|68|119|22)' samples/migration skill provenance.json src` for bounded references. The latter found the seven excerpt links and the root manifest's historical original-path field, with no additional consumer in those searched artifacts. That historical field is provenance, not a link to rewrite. An initial inventory reported that `docs/` did not yet exist; this record creates the general research directory.

An inline, read-only `python3 - <<'PY'` calculation used `re.findall(r'\[([^\]]+)\]\(([^)]+)\)', note.read_text())`, split URLs at `#`, and computed `posixpath.normpath(str(parent / target))` from old and hypothetical new parents. For each row it checked `is_file()`, recomputed using `'../' + target`, and inspected `read_text().splitlines()[int(fragment[1:])-1]`. Actual result: 7/7 old targets existed, 0/7 unchanged new targets existed, 7/7 corrected paths equaled their original targets, and 7/7 anchors were in range. `hashlib.sha256(path.read_bytes()).hexdigest()` was compared with each manifest's `files[].sha256`: 8/8 matched. The same calculation produced the excerpt digest and confirmed unequal manifest bytes. No repository modules were imported or executed; these were permitted path/hash checks, not a scratch behavior experiment.

## Decision impact

Keeping the note at its current general-research location and linking to it from a later change is the smallest option, explicitly supported by the skill. A future physical move is feasible for the supplied links with the following bounded procedure, but is not authorized or performed by this assessment:

1. Before any move, obtain the complete note and applicable repository layout. Confirm the destination is unused, capture the original bytes/hash and metadata, inventory every outbound Markdown/reference/image/HTML link and fragment, and find inbound references in specs, plans, indexes and other available consumers. Record the source revision and source hashes. If the proposed destination or naming policy changes, recompute paths rather than reuse this table blindly.
2. In one reviewable future change, relocate the one note without duplicating its evidence. Rebase the seven known URLs as listed above and calculate all other relative URLs from their actual target paths. Preserve fragments and historical findings, `created`, type and tags. Preserve `status: concluded` unless the research itself changes; record the actual edit date in `updated` according to the future task's metadata policy. Add `change` only if an actual active change is then established. Retain repository identity, revision, original-path/extraction history and labeled hashes in accessible provenance; do not rewrite historical fields to pretend the note always lived at its new location.
3. Update every known inbound link, resolving it from each consumer's own directory and preserving its note-heading fragment. Preserve heading text and explicit anchor IDs. If compatibility with unavailable consumers is mandatory, defer the move until a separately authorized compatibility approach is agreed; do not silently leave a duplicate research record or assume redirects exist.
4. Accept only after reading the actual saved note and checking that each rebased outbound URL reaches the same normalized source path and SHA256, every line anchor/range still identifies the intended evidence, metadata/history are preserved, and all inventoried inbound links reach the new note and intended heading. Search available consumers for stale live references to the old location, excluding intentionally retained provenance/history fields. Review the diff for a single relocation plus necessary link/metadata/provenance edits, with no source changes or conclusion rewrite. Check navigation in required renderers when available; otherwise retain that limitation. No pytest/npm run is needed for this document move.

### Stop and recovery boundaries

Before future cutover, stop if a source hash differs, an anchor points at different content, a destination collision exists, the complete note cannot be inventoried, required consumers cannot be accounted for, or provenance cannot be retained. A source mismatch requires separate revalidation; a path rewrite cannot settle it.

For a future local, unpublished move, the recovery boundary is the recorded original state: restore the note at its original path and bytes, undo only this migration's inbound-link/metadata/provenance edits, and remove the new location after confirming no independent edits would be lost. Verify original links and hashes again. Do not overwrite intervening work or rewrite historical provenance. If a future move has already been shared/published or acquired new consumers or edits, restoring a local path alone cannot undo those effects; coordinate a forward repair or separately authorized compatibility step. This assessment creates no such cutover and needs no rollback of the specimen.

## Limitations and open questions

The excerpt omits the full note's body, headings, possible attachments and additional links. The minimum snapshot cannot establish complete inbound-link coverage or rendering behavior in Obsidian/GitHub/other editors. No immutable remote permalink was verified, and no remote URL should be invented from the local repository path. Supplied hashes and recorded commit provide bounded local traceability only. Future source changes, a different destination depth, different repository layout, unavailable consumers or a new naming policy require revalidation. The decision against an unchanged move is settled for all seven supplied links; full-migration acceptance remains conditional on the missing complete-note and consumer evidence.
