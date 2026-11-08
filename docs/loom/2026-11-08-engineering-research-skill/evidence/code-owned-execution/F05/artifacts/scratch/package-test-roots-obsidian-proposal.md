---
title: "Package runner test roots and local-test exclusion"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
  - engineering/testing
  - loom/package-runner
---

# Package runner test roots and local-test exclusion

Reviewable candidate only: this file is in project scratch; no Obsidian/Vault copy has been saved or approved. Proposed destination: `<user-selected fixtureVault path>/Engineering/package-test-roots-and-local-exclusion.md`. The exact fixtureVault path is unresolved. Approval would cover this single note's content only, with no installation, publishing, synchronization or other Vault changes.

## Question and applicable conditions

Where should tests be placed to participate in this Loom package runner's ordinary suite? Findings apply to the minimal source snapshot attributed to original repository `loom-plugins` (recorded worktree identity `loom-research-skill-discut`), source commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`. The original filesystem location is provenance only and was not accessed. This is not a complete checkout or deployed version.

## Findings and decision

The runner's `TEST_ROOTS` is exactly `tests`, `loom-code/tests`, `loom-design/tests`, and `loom-workflow/tests` (runner lines 51–55). The `--loom-family` preset excludes each applicable root's direct `local/` subtree from Python or shell discovery (lines 76–114, 124–137). The explicit-argument mode forwards groups to pytest without adding that local exclusion (lines 168–175); bare pytest and explicitly targeted local tests are outside this conclusion.

Place tests intended for ordinary package coverage under a listed root outside its direct `local/` subtree. A new standalone plugin root must be added to `TEST_ROOTS` to participate, subject to ordinary discovery rules. Revalidate this advice against the runner revision used by the target project.

## Evidence and provenance

Static source inspection and matching provenance hashes support these findings. Test definitions corroborate intent but were not run. No CI, runtime, installation or release verification is claimed.

The temporary fixture merged the prior research at main revision `4959e620a78e15678a3cc2a8a0c18f79de58dc73` from topic `00fa7642dd5ba69eb7b37fa19dfc0b15d4f3537a`. This harness history is distinct from the original source commit. No local tags or remote were present during inspection; upstream release remains unverified. Prior isolated executor success does not prove installed-host behavior or server-confirmed model identity.

The following ordinary Markdown links use absolute fixture-local paths so moving this note into a fixtureVault will not reinterpret project-relative links. The evidence copies were extracted from the exact merge revision via `git show`; project originals remain in place. No upstream remote URL is available to form published commit permalinks.

- [Pinned original research at fixture merge 4959e620](/private/tmp/code-owned-engineering-research-execution-20261108/F05/project/scratch/preservation/4959e620a78e15678a3cc2a8a0c18f79de58dc73/research-original.md)
- [Pinned runner source at fixture merge 4959e620](/private/tmp/code-owned-engineering-research-execution-20261108/F05/project/scratch/preservation/4959e620a78e15678a3cc2a8a0c18f79de58dc73/run_package_tests.py)
- [Pinned test definitions at fixture merge 4959e620](/private/tmp/code-owned-engineering-research-execution-20261108/F05/project/scratch/preservation/4959e620a78e15678a3cc2a8a0c18f79de58dc73/test_run_package_tests.py)
- [Project research original](/private/tmp/code-owned-engineering-research-execution-20261108/F05/project/docs/loom/research/2026-11-08-package-test-roots.md)
- [Source provenance](/private/tmp/code-owned-engineering-research-execution-20261108/F05/project/provenance.json)
- [Lifecycle closeout](/private/tmp/code-owned-engineering-research-execution-20261108/F05/project/docs/loom/research/2026-11-08-package-test-roots-closeout.md)

## Preservation limits

The pinned research copy retains its historical text, including project-relative links; use the destination-adapted source links above when reading this candidate. All evidence paths depend on this temporary fixture remaining available. They are suitable for reviewing this isolated proposal, not a promise of permanent access. A durable evidence destination or genuine upstream permalinks remains unresolved. No release-dependent claim, full receipt, credential, session archive or environment configuration is proposed for copying into Obsidian.
