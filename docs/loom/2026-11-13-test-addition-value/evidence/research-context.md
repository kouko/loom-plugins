# Scoped research context

## Question and conditions

Can Loom avoid redundant test additions while retaining distinct defect detection?
Source baseline: `fbdc29af358413bc9d55b599231b2a6cbcb4524d`.
The broader local-project survey and outside-review raw records remain local;
this document retains only the repository evidence needed for this change.

## Local evidence

- `loom-code/tests/test_contract_charter.py::test_list_rules_includes_contract_charter_complete`
  and `loom-code/tests/test_probes_charter_charter.py::test_list_rules_carries_charter_complete_rule_id`
  invoke the same checker command with the same globals and rule-ID assertion.
  Both passed in an earlier targeted run; no test was deleted.
- `loom-code/agents/implementer.md`, Role contract item 2, already budgets additions
  and prefers existing helpers. `lenses.md`, tests row, already treats duplicates
  as findings. The missing emphasis is comparing the new case against existing
  protection, not another numeric ceiling.
- Similar source or shared covered lines alone cannot establish redundancy:
  decorators, fixtures, inputs, state, environment and oracles may differ.
- `closing-review/SKILL.md`, review.probe-graduation, remains mandatory for
  defect-catching adversarial programs. This change does not replace that gate.

## Decision and limits

Strengthen existing planning, implementation and review guidance. Retain the
existing test budget, TDD and quality checks. No bulk cleanup, test-count gate,
new schema, audit harness or runtime-saving claim is justified by this evidence.
Behavioral dogfood and independent acceptance must establish the candidate's
observed behavior; source inspection and green package tests alone cannot.
