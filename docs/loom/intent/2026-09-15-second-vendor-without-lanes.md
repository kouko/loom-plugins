# Decide second-vendor suggestions without the removed lane setting
originator: kouko
kind: engineering
needs-design: no — this changes how an internal policy script and station instructions decide an existing notice; no command, output format, or interface surface a user types into changes
status: confirmed 2026-09-15
publication: automatic — authorized 2026-09-15 by kouko

## Problem
The lane setting was removed when expert-mode shipped, but the second-vendor
suggestion still depends on it: the policy script refuses to run without a
`small` or `full` lane, and the station instructions tell agents to pass one.
Nothing defines how to work out that value any more, so an agent has to guess.
The same change can therefore get a different result — whether the user may
opt in to a review by another model family — depending only on that guess.

## Proposed outcome
Whether a change is offered the second-vendor opt-in is decided the same way
every time, from information Loom already has, and no instruction or script
asks for a lane.

## Acceptance
1. For the same change and the same available reviewers, running the second-vendor suggestion step twice gives the same result, without the agent supplying any lane value.
2. No station instruction, reference, contract note, or policy script in `loom-code` or `loom-design` asks for, describes, or depends on a small or full lane.
3. Every change, including one Loom treats as narrow and low-risk, is offered the second-vendor opt-in the way a regular change is offered it today (user-decided 2026-09-15).
4. The repository's existing package test suite passes.

## Constraints
- The `second-vendor` repository default keeps its current values and meanings (`ask`, `suggest`, or a fixed tool).
- Expert-mode step selection and the reviewer count stay as they are.

## Out of scope
- Changing which reviewers run, or how many.
- Adding new second-vendor tools or hosts.

## Open questions
- none
