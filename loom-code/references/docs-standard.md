# Docs standard

The rules docs and skill text are written to and judged against: docs,
`SKILL.md` files, agent contracts, references and rule text. The implementer
reads this file before writing any of them; the closing-review docs and
skill lenses judge the work against it. Each rule is stated here and nowhere
else: the engineering baseline and the lenses point to this file instead of
restating it. How the reviewer scores each dimension stays in the lens.

## 1. Nothing the reader needs is missing

An obligation or referent the text needs and lacks is a finding: a step the
reader cannot execute, a term used but never defined, a promised section
absent, a required diagram or comparison table missing (or declared
not-applicable for a reason the text's own content contradicts).

## 2. One live reading

An absolute — "only", "never", "zero" — with no support is a finding, and so
is a sentence with two live readings that fork what the executor does.

## 3. Passages agree

Two passages contradicting is a finding, including changed against
unchanged: the delta says X and an untouched paragraph still says not-X.

## 4. Facts match their source

A citation that does not support its claim is a finding, and so is a stated
number or path that is wrong against the artifact it describes.

## 5. A number names its population

A measured number with no denominator or scope is a finding: "0% false
positives" without saying over what.

## 6. Polarity against the base

This sharpens §3 for changed against base. When a change deletes or rewrites
a sentence carrying a polarity word, read the base version with
`git show <base>:<path>` and compare each such sentence with its new form.
Polarity words are never, must not, only, always, 不得 and their kin (no, do
not, may not, forbid, 禁止, 絕不). A reversed direction, or a polarity clause
dropped with nothing else in the delta or the unchanged tree carrying it, is
an `inconsistency` finding. A reversed direction is must ↔ may, never ↔
always, forbid ↔ allow; a rewording that keeps the direction is not a
finding.

## 7. Deletion-first for docs and skill

A new paragraph, mechanism, reserved task or fallback path in station text
or a contract shows in the delta what it replaced, or names the
already-observed failure it prevents by citing a concrete failure or a
`docs/loom/memory` entry — otherwise it is a finding, and the finding names
the smaller shape that does the same job. This is the rule
[`code-design-standard.md`](code-design-standard.md) §2–3 states for code,
applied to station text and agent contracts. A `*_CAP` constant raised in
the same file across two consecutive changes is a design smell: the
`deletion-first` dimension always names at least one deletion candidate for
that file, standing until it is rebutted with evidence.
