---
title: "Can the extracted research note move without losing source traceability?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Research note migration traceability

## Question and scope

Can the supplied note at `docs/loom/research/2026-11-08-package-runner-exclusions.md` move unchanged to `docs/loom/example-change/research/2026-11-08-package-runner-exclusions.md` while retaining source traceability? These paths are relative to the supplied `samples/migration/` tree. The destination is hypothetical; there is no active change.

This assessment uses only supplied local evidence on 2026-11-08. The note is an extraction of metadata and verbatim evidence rows, not the complete original research. Neither the note nor any source, skill, sample or provenance file was changed, moved or copied. No repository initialization, test execution, network access, installation, external model, publication or delegation occurred.

## Method and rationale

Used document inspection, read-only Python path arithmetic, SHA256 comparison and source-line inspection. This directly answers whether the evidence edges survive a directory change; executing repository behavior would not resolve that question. Stopped after checking all seven supplied links, their line targets, the four source identities, metadata and the available provenance. No scratch experiment was needed.

## Findings

**An unchanged move fails in the supplied layout.** All seven outgoing links resolve at the old location. At the proposed location they would instead resolve below `samples/migration/docs/src/`, where none of the four target files exists. Adding one `../` to each source link restores the same target paths in this layout. Keep the filename for a minimal move; renaming to a sequence is a separate naming decision that would require additional incoming-link updates.

The following URLs are literal proposed edits, not links from this new report. All old URLs start with `../../../src/`; all corrected URLs start with `../../../../src/`.

| Evidence | Corrected URL from hypothetical destination | Inspected line target | Source length |
|---|---|---|---|
| E1 | `../../../../src/scripts/run_package_tests.py#L153` | `def main(argv: list[str]) -> int:` | 180 lines |
| E2 | `../../../../src/loom-code/scripts/repo_files.py#L97` | `def nested_repositories(root: Path \| str) -> list[Path]:` | 172 lines |
| E3 | `../../../../src/loom-code/scripts/repo_files.py#L73` | `def nested_worktrees(root: Path \| str) -> list[Path]:` | 172 lines |
| E4 | `../../../../src/loom-code/scripts/git_exec.py#L50` | `def run_git(` | 88 lines |
| E5 | `../../../../src/scripts/run_package_tests.py#L68` | `def _holds_tests(folder: Path, skip: tuple[Path, ...] = ()) -> bool:` | 180 lines |
| E6 | `../../../../src/tests/test_run_package_tests.py#L119` | `def test_targets_unchanged_without_nested_worktree(tmp_path: Path) -> None:` | 331 lines |
| E7 | `../../../../src/tests/test_run_package_tests.py#L22` | `def test_runner_exit_code_is_nonzero_when_a_later_group_fails(tmp_path: Path) -> None:` | 331 lines |

**Line references remain meaningful only for the identified bytes.** Every `#L<number>` is within the matching source file, and every prose line range in E1–E7 is within its file. Inspected source excerpts establish that the anchors identify the listed definitions. This is a source-location check, not a rerun or full revalidation of the earlier findings. These fragments describe source line positions, not Markdown heading IDs. GitHub-style line navigation is not guaranteed by a local Markdown link: actual GitHub/Obsidian/editor rendering and fragment navigation were not tested. There are no heading-fragment or internal section links in the supplied excerpt. The complete original may contain additional links or anchors.

**Provenance survives only if its mapping stays available and truthful.** Both manifests identify commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; their repository, HEAD, locally recorded origin/main, remote-freshness and source-file entries agree. Both say remote freshness was not checked. These are manifest assertions supported here by matching source hashes, not independently checked Git history or a fresh remote observation.

| Manifest-relative source path | SHA256; matches both supplied source copies |
|---|---|
| `scripts/run_package_tests.py` | `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` |
| `loom-code/scripts/repo_files.py` | `62333168fb9eacabb6877d0f185f08081175d8681444465173b18d712ca26399` |
| `loom-code/scripts/git_exec.py` | `9c721b8e2f8fae0e4c31da5d6ab41b42e0ae4eeb8cecbf164a36fce7dd61e7c7` |
| `tests/test_run_package_tests.py` | `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28` |

The project-root manifest additionally identifies the original full note's artifact path, SHA256 `dcbf5ea5573cd922f1f56b764d65ec10d481d54925f578cc195a575e10b9272b`, and extraction scope. The migration-local manifest omits that note-extraction entry. The supplied excerpt hashes to `f2392d0855416ff2e4979dec4d9f6b5f50dae7f01c2fa06df1b9e0ea0a79b256`; this is an extracted artifact, so its different hash does not establish corruption of the unavailable full note. The full note's recorded hash cannot be verified here. The excerpt itself has no explicit link to either manifest and no commit in its metadata.

The original repository's absolute location is provenance data only; it was not accessed. Manifest source paths omit the snapshot's `src/` prefix. Consequently, the corrected URLs above apply to the supplied migration layout, not automatically to a future real checkout. A real checkout must map each manifest-relative path to its actual location before accepting rewritten links.

## Evidence

- [Extracted original note](../../../samples/migration/docs/loom/research/2026-11-08-package-runner-exclusions.md): metadata lines 1–10 and evidence rows E1–E7. Flat metadata has the required fields, status `concluded`, dates `2026-11-08`, tag `loom/research`, and no `change`. These describe the earlier record, not migration acceptance.
- [Project provenance](../../../provenance.json) and [migration provenance](../../../samples/migration/provenance.json): read both manifests, compared common fields and all four source hashes. The former supplies the note-extraction provenance missing from the latter.
- Inspected source locations: [runner](../../../samples/migration/src/scripts/run_package_tests.py#L153), [repository inventory](../../../samples/migration/src/loom-code/scripts/repo_files.py#L97), [worktree inventory](../../../samples/migration/src/loom-code/scripts/repo_files.py#L73), [Git wrapper](../../../samples/migration/src/loom-code/scripts/git_exec.py#L50), [command discovery](../../../samples/migration/src/scripts/run_package_tests.py#L68), [test definitions](../../../samples/migration/src/tests/test_run_package_tests.py#L119), and [ordering test](../../../samples/migration/src/tests/test_run_package_tests.py#L22). Tests were read, never executed. All four files in project `src/` were also hashed and match their migration copies and manifest hashes.
- [Invoked skill](../../../skill/engineering-research/SKILL.md), [methods](../../../skill/engineering-research/references/research-methods.md), [source policy](../../../skill/engineering-research/references/source-policy.md), and [template](../../../skill/engineering-research/templates/research.md): read bundled instructions. The skill permits later changes to reference a general research record without copying it; it requires preserving earlier decisions and resolvable relative links.

Read-only command evidence: `python3 - <<'PY' ... PY` read both JSON manifests and extracted the seven Markdown URLs using `re.findall(r'\[([^\]]+)\]\(([^)]+)\)', note.read_text())`. For each URL it used `posixpath.normpath(str(base / path))` with old base `samples/migration/docs/loom/research` and new base `samples/migration/docs/loom/example-change/research`, then `posixpath.relpath(target, new_base)` to calculate the repair. Observed: 7/7 old targets exist, 0/7 unchanged new targets exist, and each repair normalizes to its original target. It used `hashlib.sha256(path.read_bytes()).hexdigest()` against each manifest entry: 8/8 source-copy comparisons matched. It read the actual anchor lines and source excerpts; this ran no repository imports or test commands.

The read-only command `rg -n --hidden '2026-11-08-package-runner-exclusions|docs/loom/research|example-change|#L[0-9]+' samples/migration skill provenance.json` found the seven outgoing links, the skill's generic directory rule, and the root manifest's historical original-note path. It found no incoming Markdown reference in that bounded set. This does not establish absence of backlinks in the unavailable complete repository. The provenance original path is a historical identifier, not a backlink to rewrite.

## Decision impact

The smallest option is to retain the general record and let a future change reference it with a relative Markdown link. That avoids a relocation and preserves existing readers' paths. If relocation is later required, perform the following only in an authorized future working copy; the supplied samples remain frozen.

1. Capture the actual full note's bytes/hash, metadata, old path, source commit and source hashes. Inventory all outgoing links (including reference-style links and attachments), incoming links, and any links to its headings across the real checkout. Do not treat this excerpt as the full inventory. Confirm destination availability and actual source layout; stop on a collision or unknown mapping.
2. Move the one record, keeping its filename and substantive conclusions. Rewrite the seven known source URLs by adding one parent traversal in the supplied layout; calculate rather than assume paths in a real checkout. Update real incoming references to the new location and preserve their fragments. Do not rewrite historical paths or hashes in provenance.
3. Preserve `created`, title, type, tags and the historical evidence/limitations. Record the actual relocation date in `updated` and a brief relocation annotation. Add `change` only if a real active change is established; the hypothetical directory name alone supplies none. If a future active-change naming convention requires a sequence, allocate it after inspecting that change's existing records and update the same link inventory for the chosen filename.
4. Keep provenance accessible. Add a short annotation linking to the preserved provenance record and recording the commit, source-path mapping, old/new note paths, original note hash and resulting relocated-note hash in a migration receipt. If adding an in-note receipt link, avoid a self-referential final hash: the receipt holds the final note hash. Carry the extraction entry as well as the source manifest when dealing with this excerpt; moving only the excerpt and migration-local manifest would omit its recorded origin. Keep original artifact hashes distinct from the edited note's new hash.
5. Accept only after reading back the actual moved note: every rewritten link resolves to the intended file, each fragment still identifies the intended source at the recorded commit/hash, metadata remains valid, all known incoming references resolve, and the receipt reconstructs old path → new path → evidence identity. Compare content with the captured original: only agreed relocation links, metadata and annotation may differ. Check actual target viewers' fragment behavior separately if clickable line navigation is required. This acceptance needs no pytest/npm execution and conveys no CI, deployment or runtime result.

## Rollback boundary

Before future acceptance, any missing target, source hash mismatch, unresolved incoming reference, ambiguous provenance or substantive content drift stops the move. Restore the captured original bytes at the old path, restore only references and metadata changed by this relocation, and remove only the destination/receipt created by it. A destination collision must be resolved without overwriting unrelated content. Do not alter source snapshots or historical provenance to make verification pass; retain any needed audit record of an attempted move separately.

After other work starts depending on the new location, rollback must also account for those consumers and any concurrent edits; do not blindly restore old bytes over later work. A relocation does not authorize implementation, a new active change, source modifications or publication. If the source commit or evidence conditions change, preserve the earlier decision and create a separately scoped revalidation instead of silently updating its historical basis. This investigation changed no original record, so no migration rollback is currently needed.

## Limitations and open questions

The full original note, complete checkout, history, backlinks and future destination are unavailable. Its original full-note hash and any omitted anchors/attachments remain unverified. GitHub/Obsidian rendering and line navigation are untested; no external permalink or upstream state was checked. Hash matches identify supplied bytes against supplied manifests, not independently authenticated upstream provenance. The source snapshot provides no test, CI or deployment outcome. The bounded conclusion is sufficient: a direct unchanged move breaks all seven supplied source links, while a carefully recorded move can preserve their identities after path repair and the stated future acceptance checks.
