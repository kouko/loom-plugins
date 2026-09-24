# Acceptance test report — the template

Independent acceptance testing produces `docs/loom/<change-id>/acceptance-test-report.md`. This is
the document the user reads at decision point ③ to say "yes, that is what I
wanted". They never read the diff, so anything not in here is invisible to
them. It should read in about a minute.

Write it in the user's own language and in their words: what they asked
for, what happened when it was tried, what it cost them. Technical terms
stay in English. No file paths, no function names, no loom vocabulary —
the one path allowed is the line pointing to the evidence file. Every
section below is required; a section with nothing to say says so in one
line rather than disappearing.

How each line was tried, the commands, their output and any `file:line`
go to a second file, `docs/loom/<change-id>/evidence/acceptance-test-evidence.md`,
shaped as the next section shows. The report carries the verdicts; the
evidence file carries what backs them.

---

```markdown
# <change title> — what I tried and what happened

Tried on <date>, in a clean copy of the project at <short sha>. How I tried
each line and what came back: `docs/loom/<change-id>/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | <the intent's first Acceptance line, verbatim> | works | <one plain sentence> | re-tested |
| 2 | <the second Acceptance line> | partly | <one plain sentence> | carried over — <one-line reason> |

<Verdict is one of works / partly / not verified / fails. One row per
Acceptance line; for a product change, one further row per UI flow in the
spec. On a first run the Re-run cell is "—". On a re-run after a fix it
is "re-tested" for a line tried again, or "carried over — <one-line
reason>" for a line kept from the earlier run. A re-tested row carries no
reason.>

## 對你既有的資料做了什麼 (what this did to data you already had)

<One paragraph, always present. If the change reads and writes nothing the
user already owned, the line is: "Nothing — it only touched files this
change created." If it did touch existing data, say exactly what changed,
whether the old form can still be read, and where the backup is.>

## I decided for you

<Every fork the agent resolved without asking, and every finding of
severity important or worse that the main agent dismissed. One bullet each:>

- **<the choice>** — I picked <option> because <reason>. Changing it later
  means <cost>.
- **<the dismissed finding>** — <who> raised <finding>; dismissed
  because <reason>. If that reason is wrong, this is where it shows.

<If there were none: "Nothing — every choice was either yours or forced.">

## Things I am not sure you want

<Open questions, in the user's terms, each answerable with a sentence. If
none: "Nothing.">
```

---

## The evidence file

`docs/loom/<change-id>/evidence/acceptance-test-evidence.md` is plain
markdown, never executable and never starting with `#!`. It holds one
section per row of the report, under the same number, and a dated section
for each re-run.

```markdown
# <change title> — acceptance test evidence

Tried on <date>, in a clean copy of the project at <short sha>.

## 1. <the intent's first Acceptance line, verbatim>
- How I tried it: <the commands typed or the buttons pressed>
- What came back: <the output, trimmed to what backs the verdict>
- Evidence: <captured output / screenshot / file:line / named test>

## 2. <the second Acceptance line>
…

## Re-run on <date>, at <short sha>
- 1: re-tested — <how, over every surface the line names, and what came back>
- 2: carried over — <the reason, checked against the fix>
```

---

## Gate-only's replacement material

Gate-only presents the one-page probe-and-package-test result at decision
point ③ instead of an acceptance test report, shaped by this same
`references/acceptance-test-report.md` structure — every adversarial probe
named, what ran and what it proved, plus the package-test command's own
recorded result.

## What makes a report unusable

- An Acceptance line reported as "works" with no evidence anyone can look
  at. Evidence is a screenshot, a captured output, or a named test in the
  evidence file — not the runner's word.
- Evidence pasted into the report. Commands, output and `file:line` belong
  in the evidence file; the row keeps its verdict and one plain sentence.
- A carried-over verdict with no reason, or a re-tested row that still
  carries one.
- The data paragraph missing. It is fixed because acceptance testing happens in
  a clean environment and structurally cannot hit the user's real data:
  that harm is only ever caught by saying out loud what would happen.
- Decisions folded into prose instead of listed. If the user has to hunt
  for what was decided for them, it was not disclosed.
