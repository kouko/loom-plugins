# Synthetic skill-review cases

These independent cases contain invented tools and project names. Review
each target against its supplied project contract and acceptance condition.
The reference manual excerpts are ground truth; no tool installation or
network access is needed. Record concrete findings, their target anchors,
and any required fix. Do not infer a contract from a target's location.

## external-clean

Project contract: This independent skill uses ordinary prose instructions.
Its project has no Loom gate-registration contract.

Acceptance: The skill tells an agent how to display the installed version.

Reference manual: `quill version` prints the installed version.

Target: `quill-guide/SKILL.md`

```markdown
# Quill version
When asked for the installed Quill version, run `quill version` and report
the command's output. Do not install or update Quill for this request.
```

## workflow-only-adoption

Project contract: This independent skill is being edited with the Loom
development workflow. Its project retains ordinary prose instructions and
has not adopted the Loom gate-registration contract for its artifacts.

Acceptance: The skill tells an agent how to display the installed version.

Reference manual: `quill version` prints the installed version.

Target: `quill-guide/SKILL.md`

```markdown
# Quill version
When asked for the installed Quill version, run `quill version` and report
the command's output. Do not install or update Quill for this request.
```

## governed-missing-marker

Project contract: This project, outside the Loom repository, explicitly
adopts Loom gate registration for its release skill's blocking rules.
Each such rule must carry its registered `<!-- gate: <id> -->` marker.
The registry includes `release.clean-tree`; the checker recomputes it by
requiring an empty `git status --porcelain` result before publication.

Acceptance: Publication is blocked when the working tree is dirty, with
the blocking rule marked according to the project contract.

Target: `release-helper/SKILL.md`

```markdown
# Release helper
Before publication, run `git status --porcelain` in the repository root.
If it returns any entries, stop publication until the working tree is clean.
```

## governed-marked

Project contract: This project, outside the Loom repository, explicitly
adopts Loom gate registration for its release skill's blocking rules.
Each such rule must carry its registered `<!-- gate: <id> -->` marker.
The registry includes `release.clean-tree`; the checker recomputes it by
requiring an empty `git status --porcelain` result before publication.

Acceptance: Publication is blocked when the working tree is dirty, with
the blocking rule marked according to the project contract.

Target: `release-helper/SKILL.md`

```markdown
# Release helper
<!-- gate: release.clean-tree -->
Before publication, run `git status --porcelain` in the repository root.
If it returns any entries, stop publication until the working tree is clean.
<!-- /gate -->
```

## real-command-error

Project contract: This independent skill uses ordinary prose instructions.
Its project has no Loom gate-registration contract.

Acceptance: The skill tells an agent how to display the installed version.

Reference manual: `quill version` prints the installed version.
`quill --version` is unsupported and exits with an unknown-option error.

Target: `quill-guide/SKILL.md`

```markdown
# Quill version
When asked for the installed Quill version, run `quill --version` and
report the command's output. Do not install or update Quill for this request.
```

## correct-command

Project contract: This independent skill uses ordinary prose instructions.
Its project has no Loom gate-registration contract.

Acceptance: The skill tells an agent how to display the installed version.

Reference manual: `quill version` prints the installed version.
`quill --version` is unsupported and exits with an unknown-option error.

Target: `quill-guide/SKILL.md`

```markdown
# Quill version
When asked for the installed Quill version, run `quill version` and report
the command's output. Do not install or update Quill for this request.
```
