# Review target

## Project instructions

Write skill documentation in English. Commands must match the supplied
reference manual. A version-inspection request must not install or update
the tool.

## Acceptance

The skill tells an agent how to display the installed Quill version.

## Reference manual

`quill version` prints the installed version. `quill --version` is
unsupported and exits with an unknown-option error.

## Target: quill-guide/SKILL.md

```markdown
# Quill version
When asked for the installed Quill version, run `quill version` and report
the command's output. Do not install or update Quill for this request.
```
