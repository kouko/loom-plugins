# No intent yet: the short interview

Loaded by step 1 of `../SKILL.md` when no intent exists and `loom-design`
is not installed. Relative paths here are relative to this file's
directory; step numbers are that SKILL.md's.

Read `confirmation-template.md` before drafting or replying.
When you write the intent, use `../../../contract/templates/intent.md` for its
field boundaries. Missing required content stays in Open questions and blocks
confirmation; a yes cannot supply missing evidence. Stay in this interview until
the facts are settled; do not load the ready confirmation reader or layout yet.
Then return to step 2; step 3 loads `confirm-intent.md` only for ready confirmation.

- `loom-design` is not installed → hand the user the template path,
  `contract/templates/intent.md` inside the `loom-code` plugin, and stop
  there **unless** the user wants to describe the change now. If they do,
  run step 3's restate-and-confirm as a short interview instead: ask what
  the problem is, who it hurts, and what they will be able to do when it
  is done; write the file yourself from their answers. A feature or
  bug-fix request already describes the change: run the short interview
  and write the file; offer the template path only when the user asks for
  it. Keep it short — an
  engineering intent is normally three to five lines, and writing it by
  hand beats interviewing. The user never hand-writes the file. When you
  write it, `## Open questions` must be non-empty — the checker requires
  the section to have content, so with nothing open write exactly `- none`
  under the heading rather than leaving it blank.
