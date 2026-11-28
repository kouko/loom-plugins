# Code-design standard

The rules code is designed to and judged against. The implementer reads
this file before writing code; write-plan reads it when choosing each
task's module boundary and entry; the closing-review code lens judges the
work against it. Each rule is stated here and nowhere else: the engineering
baseline, write-plan and the lens point to this file instead of restating
it. How the reviewer scores each dimension stays in the lens.

## 1. Names say what the thing is

Names say what the thing is; functions stay short — past 20 lines, and again
past 50, is a prompt to look, never itself a finding; a split finding names a
concrete problem, such as a function doing several unrelated things, and
length alone is never the finding.

## 2. An abstraction earns its place

Every new abstraction, flag, config or extension point justifies itself with
two concrete users now, an explicit request, or a visible motivation. A
finding must name the smaller shape that does the same job — no finding
without a concrete alternative.

## 3. A module that only forwards is a finding

A new module or function that only forwards — just a call elsewhere returning
its result, free of branching, transformation, validation, error handling,
resource-boundary handling and policy choice — is a finding. A module or
function hiding any of those is outside this rule, and so is a re-export that
declares the module's entry (a package `__init__`, a TS `index` barrel).

## 4. Extract on the Rule of Three

Remove duplication and smells; under the Rule of Three, three sites doing the same thing are
an extraction candidate, extracted only when the three change for the same
reason; a split or extraction defaults to a non-exported function inside the
module, and becomes its own module with an entry only when another module
needs to call it or its behaviour is unreachable from the existing entry —
wanting to test it alone is no reason for a new entry; a shared extraction
across modules stays acceptable as its own module whose entry its callers
import.

## 5. A module hides more than it shows

A module whose interface is nearly as complex as what it does gives its
callers little: they learn almost as much to call it as to do the work
themselves. Prefer a small interface that hides substantial behaviour.

To judge a module, imagine deleting it: if the complexity vanishes with it,
the module was a pass-through; if the complexity reappears across its
callers, the module earns its place. §3 is the plainest case of this test.

## 6. Code a test can drive

Accept a dependency from outside — as a parameter or a constructor argument —
rather than creating it inside, so a test can hand in its own. Where the
behaviour allows, return a result rather than producing a side effect, so a
test can check the value it gets back.

## 7. A deliberate shortcut names its ceiling

A shortcut taken on purpose is annotated with its ceiling and its upgrade
path; an annotation saying "later" or "someday" names no ceiling and is a
finding.
