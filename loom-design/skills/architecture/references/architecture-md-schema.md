# ARCHITECTURE.md schema

`ARCHITECTURE.md` lives at the repository root, one per repository. It holds
rules an agent can follow and a guard can check — nothing else. Overview or
background prose does not change what an agent does, so it has no place here.

## Shape

1. A title line: `# Architecture`.
2. Directly under the title, once the user has said yes to the restatement:
   `ratified-by: <name> <YYYY-MM-DD>`.
3. Exactly these four sections, in this order, and no other `## ` section:
   - `## Module boundaries` — which module may depend on which.
   - `## File placement` — where each kind of file goes.
   - `## File size` — the size limits files stay under.
   - `## CI stages` — what CI runs, and in what order.
4. Under each section, one line per rule:

   ```
   - <ID> — <rule> — check: <guard path>
   - <ID> — <rule> — check: review
   ```

   - `<ID>` is an uppercase prefix, a hyphen and a number (`MB-1`, `FP-2`);
     ids are unique across the file.
   - `<rule>` is one sentence stating what must hold.
   - `<guard path>` is the guard test's path relative to the repository
     root, and that file must exist. A rule that needs judgment and cannot
     be checked mechanically says `check: review` and has no guard; the
     closing review's `architecture-conformance` dimension reads it instead.

`scripts/architecture/validate_architecture_output.py` checks all of the
above (with `--draft` before the `ratified-by:` line is written).

## Guard failure message

A guard's failure message names, so the reader can act without opening
this file:

- the **rule id** and the rule text;
- the **offending path** (the file or import that broke it);
- both ways out: **conform** to the rule, or **change the rule and its guard**
  together in one commit and re-ratify.

For example:

```
MB-1 (ui/ never imports db/) broken by src/ui/list.py importing db.session.
Conform to the rule, or change the rule and its guard together in
ARCHITECTURE.md and re-ratify.
```

## Updating

A rule and its guard change in the same commit. Changing one without the
other leaves the document and the suite disagreeing, so the tool changes
both, runs the validator, and re-ratifies with a new `ratified-by:` line.

## Example

```
# Architecture
ratified-by: Alex Rivera 2026-09-25

## Module boundaries
- MB-1 — ui/ never imports db/ — check: tests/arch/test_boundaries.py

## File placement
- FP-1 — tests live under tests/, apart from the code they test — check: tests/arch/test_placement.py

## File size
- FS-1 — no source file over 400 lines — check: tests/arch/test_file_size.py

## CI stages
- CI-1 — lint runs before the test suite — check: review
```
