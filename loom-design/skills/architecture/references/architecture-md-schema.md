# ARCHITECTURE.md schema

`ARCHITECTURE.md` lives at the repository root, one per repository. It holds
the design decisions the user picked, with their reasons, and rules an agent
can follow and a guard can check — nothing else. Overview or background
prose does not change what an agent does, so it has no place here. Data
models and API interfaces have no place here either: they belong to each
change's spec.

## Shape

1. A title line: `# Architecture`.
2. Directly under the title, once the user has said yes to the restatement:
   `ratified-by: <name> <YYYY-MM-DD>`.
3. A required `## Decisions` section, before the rule sections: one entry
   per design choice, naming the choice, the options considered and the
   reason:

   ```
   - D-<n> — <choice> — options: <option>, <option> — reason: <why>
   ```

4. Exactly these four rule sections, in this order, and no `## ` section
   other than these and `## Decisions`:
   - `## Module boundaries` — which module may depend on which.
   - `## File placement` — where each kind of file goes.
   - `## File size` — the size limits files stay under.
   - `## CI stages` — what CI runs, and in what order.
5. Under each rule section, one line per rule:

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

`scripts/architecture/validate_architecture_output.py` checks:

- exactly one well-formed `ratified-by:` line (with `--draft`, zero or one);
- nothing above the first `## ` section but the title and that line;
- `## Decisions` and the four rule sections, each once, in this order, and
  no other `## ` section;
- `## Decisions` is not empty — it does not check what each entry says;
- every line under a rule section follows the rule grammar, ids are unique,
  and each guard path is inside the repository and exists.

It does not check that a guard tests its rule or that the suite runs it.

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

## Example

```
# Architecture
ratified-by: Alex Rivera 2026-09-25

## Decisions
- D-1 — layer-first folders (ui/, core/, db/) — options: layer-first, feature-first — reason: one small app; split by feature when a layer grows too big

## Module boundaries
- MB-1 — ui/ never imports db/ — check: tests/arch/test_boundaries.py

## File placement
- FP-1 — tests live under tests/, apart from the code they test — check: tests/arch/test_placement.py

## File size
- FS-1 — no source file over 400 lines — check: tests/arch/test_file_size.py

## CI stages
- CI-1 — lint runs before the test suite — check: review
```
