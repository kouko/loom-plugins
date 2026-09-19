# Blind-run report — reviewer-floor-and-process-notes

Run by a fresh-context agent that did not write this change. Branch
`chore/reviewer-floor-and-process-notes`, HEAD `9974316e`, in a clean copy of
the repo. Every line below was independently reconstructed — not read off
the diff or trusted from the plan's own claims — using the actual code, a
throwaway scratch git repo, and a full test run.

## Acceptance 1 — a `.json` file with only `version` changed is low-risk; anything else stays high-risk

**Held.** Built a scratch git repo and fed each scenario straight into
`reviewer_floor_for_paths` from `loom-code/scripts/loom_checker/reviewers.py`:

| Scenario | `manifest.json` before → after | Floor computed |
|---|---|---|
| Only `version` changes | `{"version":"1.0.0","name":"pkg"}` → `{"version":"1.0.1","name":"pkg"}` | **1** |
| `version` changes AND another field changes | `{"version":"1.0.1","name":"pkg"}` → `{"version":"1.0.1","name":"pkg2"}` | **2** |
| A brand-new `.json` file is added | (file didn't exist) → `{"version":"1.0.0"}` | **2** |
| The file becomes malformed JSON | valid JSON → `{version: 1.0.2, "name": "pkg2"` (unquoted key, unclosed) | **2** |

All four match the intent's Acceptance 1 wording exactly: version-only stays
floor 1, and any other field change, new file, or invalid JSON forces floor 2.

I also ran the project's own adversarial suite for this exact function
(`loom-code/scripts/test_adversarial_reviewer_floor_json.py`, 14 cases) rather
than trust that it exists — every case that should be blocked (int→bool,
int→float retype, duplicate JSON key, `version` retyped to an object, nested
`version` changes, array reordering/edits, mixed code+manifest changes,
rename+edit, top-level array JSON, protected-directory paths) computes floor
2. One case is a known, admitted blind spot — a `version` field that means a
schema/protocol version rather than a release number reads as low-risk when
it shouldn't — and that case is marked `xfail(strict=True)` (a test that is
*expected* to fail today); it did fail as expected, not silently pass.

## Acceptance 2 — write-plan requires naming existing test coverage before removing/rewriting a tested function

**Held.** `loom-code/skills/write-plan/SKILL.md` (Step 5, "Task size") reads:

> A task that removes or materially rewrites a function, module, recognizer,
> or rule that already has tests names the existing test file on its Risk
> line and states whether the change preserves, widens, or narrows what
> those tests cover — not just that "tests pass" once the change is made.

This is the "不變、擴大或縮小" (unchanged / widened / narrowed) requirement
from the intent, word for word in substance. It also carries its own escape
hatch for the case where this collides with the Risk line's 40-word cap,
pointing at the plan's existing "rationale exceeds its Risk line" spec-escape
rather than inventing a new one.

Checked, not assumed: `python3 loom-code/scripts/check-skill-crossrefs.py`
still returns `OK: all relative skill cross-references resolve.` after this
change (this script only walks `loom-code/skills/**`, which is where this
file lives — see the caveat under Acceptance 3 for its actual scope).
Word count of the file is 3,550 words, under its own soft cap.

## Acceptance 3 — git-memory warns that a memory entry must land before finalize-review generates the attestation

**Held.** `loom-workflow/skills/git-memory/SKILL.md`, "PR create" section,
reads:

> **For Loom, land a durable `docs/loom/memory/` entry before
> `closing-review`'s `finalize-review` generates the attestation, never
> after** — `loom-code:closing-review`'s own SKILL.md states why (a recorded
> lesson is functional content, so it must ride the fix round already in
> flight). The symptom if this is missed: the attestation's `content_digest`
> no longer matches the committed tree, and the next push fails on that
> mismatch, or the entry has to be reverted to recover the digest the
> reviewers actually read.

This matches the intent's requirement exactly ("must precede finalize-review,
cannot be added afterward") and even explains the concrete failure symptom.

**One caveat worth flagging, found by checking rather than trusting the
plan:** the plan's own boundary claim for this task says
"`check-skill-crossrefs.py` on loom-workflow still resolves." I read that
script directly (`loom-code/scripts/check-skill-crossrefs.py:50,218`) — its
scan root is hardcoded to `loom-code/skills`, and it ignores command-line
arguments entirely. It never actually inspects `loom-workflow/`, regardless
of what path you pass it, so this specific boundary check could not have
verified what it claims to. In practice this is harmless here: I grepped
`git-memory/SKILL.md` for markdown links (`](...)`) and found none, so there
is nothing in this file that could dangle. But the plan's stated verification
method for this task does not do what it says, and a future task relying on
it to catch a real dangling link in `loom-workflow` would get a false pass.

## Acceptance 4 — `heading_window.py` and `sibling_import.py` and their tests are removed, full suite passes

**Held**, with one number in the plan corrected. `git grep` across the whole
tracked tree for `heading_window` and `sibling_import` finds zero references
in live code, skills, or agent text — only historical mentions in
`loom-code/CHANGELOG.md`, `loom-design/CHANGELOG.md`, and two
`docs/loom/memory/` entries, which the intent explicitly says this removal
does not touch.

The plan's Risk line for this task says the boundary check is "collected
count matches pre-removal minus four." I checked this by building two
throwaway worktrees at the removal commit and its parent and running
`pytest --collect-only -q` on each:

- Parent of the removal commit (`d33ee9a3^`): **1984** tests collected.
- The removal commit itself (`d33ee9a3`): **1971** tests collected.

That's a drop of **13**, not 4. It matches exactly the sum of test functions
in the two deleted test files (`grep -c '^def test_' test_heading_window.py`
→ 10, `test_sibling_import.py` → 3, 10+3=13). "Four" only makes sense read as
"four files deleted" (two modules + two test files), not as a test-count
delta — the plan's own wording ("collected count") points at the wrong
number. This does not affect whether Acceptance 4 holds — the intent only
requires removal-with-passing-suite, not a specific count — but the plan's
boundary description for this task is factually wrong as literally read, and
I'm flagging it as a correction rather than silently letting it stand.

## Acceptance 5 — the full existing test suite passes

**Held.** Ran the whole package suite fresh, in parallel, on HEAD
(`9974316e`):

```
python3 -m pytest loom-code/scripts -q -n auto
...
1993 passed, 2 skipped, 1 xfailed in 66.24s (0:01:06)
```

Zero failures. The 1 xfailed is the same known/admitted blind-spot case
from Acceptance 1 (`test_semantic_version_field_is_not_a_low_risk_bump`),
which is supposed to fail — a `strict=True` xfail that started passing would
itself break the suite, so its presence here is a second confirmation the
gap is still open and honestly labeled, not silently fixed or silently
hidden.

## Summary

All 5 Acceptance lines hold. Two things worth the maintainer's attention
that don't block acceptance:

1. The W0-03 task's cited verification method (`check-skill-crossrefs.py`
   "on loom-workflow") doesn't actually check loom-workflow — the script's
   scan root is hardcoded to `loom-code/skills` and ignores its arguments.
   No live link is broken today only because `git-memory/SKILL.md` has no
   markdown links to break.
2. The W0-04 task's boundary claim ("minus four") undercounts the actual
   test-collection delta (13) by a factor of three; it was reading "four
   files removed," not "four fewer tests," and the wording invites the
   wrong reading.
