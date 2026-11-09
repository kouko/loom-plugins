# UNSAVED CANDIDATE – Vault preservation proposal (not written to any Vault)

## Source and provenance
- Project originals (stay in place):
  - [Test-roots research](../docs/loom/research/2026-11-08-package-test-roots.md)
  - [Merge/release status research](../docs/loom/research/2026-11-08-merge-release-status.md)
- Repository: temporary local fixture (no remote URL exists; none invented). Merged revision: `main` `4959e620a78e15678a3cc2a8a0c18f79de58dc73`.
- Source snapshot: upstream commit `d5a7f0da247214bdb9c61fe90c550256432e5f76` per [provenance](../provenance.json); remote freshness not checked.

## Proposed destination
Unresolved. Obsidian CLI is unavailable and no Vault path was supplied; none guessed. Please provide a Vault and folder (for example `<Vault>/Engineering/Research/`).

## Proposed content scope (one note only)
Title: "Package runner test roots and local-test exclusion"
Frontmatter: `type: loom-research`, `status: concluded`, `created/updated: 2026-11-08`, tags `loom/research`, plus `project-provenance` text.
Body, adapted from the test-roots record:
- Question and conditions (source snapshot at the commit above, not a full checkout).
- Findings: `TEST_ROOTS` lists `tests`, `loom-code/tests`, `loom-design/tests`, `loom-workflow/tests`; the `--loom-family` package preset excludes each root's `local/`; explicit-argument mode does not.
- Evidence limits: static source reading only, tests read not run, no CI/deployment/release claim.
- Decision impact: do not put ordinary-coverage tests in `tests/local/`; new test roots must be added to `TEST_ROOTS`.
- Provenance: the merge revision above; statement that merge is not release.
Links: source references would point to copied/pinned originals; I would re-resolve every link from the destination before saving. Because a Vault note outside the project cannot resolve the project's relative links, provide them as plain-text paths plus a copied evidence section, or place the note next to a copy of the sources, as you prefer.

Excluded: the merge-status record (fixture-specific, low enduring value), release-dependent claims (no release evidence), any other file.

## Decision requested
Approve or change: (1) destination Vault/folder, (2) this one-note scope, (3) behavior if a note of that name already exists (default: stop, no overwrite). Until then nothing is written.
