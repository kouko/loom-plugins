# Tests standard

The rules a test is written to and judged against. The implementer reads
this file before writing a test; the closing-review `tests` lens judges the
work against it. Each rule is stated here and nowhere else: the engineering
baseline and the lens point to this file instead of restating it. How the
reviewer runs and scores tests stays in the lens.

## 1. A test can fail for the behaviour it names

**Tests verify intent.** A test that cannot fail for the behaviour
it names is a finding — one restating a constant or the implementation,
one reading source text to assert code structure (prose-pin tests that meet §5 of this file excepted),
or a mock or stub replacing the very seam it claims to cover.

Whoever forces a RED by deliberately mutating code, a fixture or text must
confirm, before counting it as evidence, that the mutation landed — a
non-empty diff against the pristine copy, or the edit anchor matched exactly
once — and that the unmutated version passes. An unconfirmed RED is not
evidence.

## 2. Expected values come from an independent source

A tautological assertion is a finding: its expected value is computed the
same way the code computes it, so it passes by construction. Expected values
must come from an independent source: a known-good literal, a worked example
done by hand, or the spec.

## 3. Tests go through the public interface

A test coupled to the implementation is a finding: one mocking an internal
collaborator, one testing a private method, or one verifying through a side
channel instead of the public interface. The tell: a behaviour-preserving
refactor breaks the test.

## 4. Module entry versus internal functions

A module's entry is what other modules call, never whatever its tests call;
a task adding or changing a function's behaviour whose plan Files line marks
no entry is a finding; a new or changed test that calls an internal
(non-entry) function is a finding when that behaviour is reachable from the
module's entry, whether or not entry tests already cover it, and the fix
moves the test to the entry, or deletes it when an entry test already covers
that behaviour; a test through the entry is never asked to add internal
tests, and logic the entry cannot reach that became its own module with its
own entry, tested at that entry, is not a finding.

## 5. Prose-pin tests are affirmative

A test that pins a sentence of prose requires an affirmative verb before the
pinned literal, rejects any negation token in that same sentence, and
carries synthetic self-tests validating one affirmative example and one
rejected negated example.

## 6. A new test earns its place against existing cases

Compare tests for touched behaviour with existing cases: what distinct
defect, input, state, environment or oracle is new? Ordinary consolidation
or deletion requires evidence the retained case detects the old defect, not
shared lines, text similarity or counts. Preserve distinct boundary,
integration and environment coverage. Unnecessary helpers and harnesses are
findings. A test of a test is a finding, except the synthetic self-tests §5
requires. The fix for any finding adds at most one test,
extending an existing test first.
