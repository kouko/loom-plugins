# Behavioral dogfood observations

## Scope and provenance

Candidate guidance was read from commit
`339a4d89eecd087899940052fd6a032bda3b8050` (functional content
`992a3048de769c2a65132cd3de54bba2cd9ae0a7`); baseline was
`fbdc29af358413bc9d55b599231b2a6cbcb4524d`.
The three guidance files are unchanged by the subsequent main integration.
Only public Loom source and synthetic tasks entered these runs. Private
cross-project research fixtures were excluded. Raw streams remain local;
they are not part of the publication packet.

The explicitly selected CLI profile was OpenAI Codex, `gpt-6.1-sol`, low
effort. This records the requested CLI configuration, not independent backend
identity attestation. All 65 authorized CLI attempts were consumed:
one activation smoke, 52 routing trials, one cold reader, one role launch
failure before model execution, six role executions, two mutually exclusive
flag parser failures before model execution, and two corrected completion
runs. No further model CLI run is authorized by that allocation. Two native
fresh-context agents independently audited anonymized observable outputs;
these were separate from the CLI allocation. Monetary cost was not measured.

## Automatic routing

Twenty positive and six negative prompts each ran twice in fresh read-only
scaffolds, with five adjacent skill descriptions as distractors. Both
no-design-plugin cases correctly omitted the design-plugin registry.
Successful completed commands opening the expected skill file, rather than
final self-assertions, determined selection: 40/40 positive, 12/12 negative,
52/52 exact expected skill or no skill; all 52 processes exited zero.
Descriptions were unchanged, so this demonstrates routing compatibility,
not a measured triggering improvement. These scaffolds stopped at missing
station prerequisites and did not validate installed-host integration.

## Workflow observations against the fixed rubric

The role rubric was recorded before execution. Baseline and candidate each
ran planner, implementer and reviewer tasks against matched public-source
or synthetic inputs. Completion trials repeated only candidate planner and
implementer after correcting fixture prerequisites; original runs were kept.

| Role | Observable candidate result | Boundary |
| --- | --- | --- |
| Planner | Named both existing rule-discovery owners, reused their coverage for unchanged discovery, and separately planned a carriage-return regression with structurally valid rows. | The fixture prohibited the independent plan review and lacked installed plugin identity. Both initial and completion plans explicitly remained drafts, not finalized station deliveries. |
| Implementer | Existing newline cases failed before the validator edit and passed after it. Ordinary text, CJK, pipe and newline variants remained; no test file or test line was added. The completion run actually committed only the validator fix and ended clean. | The seam was synthetic; this does not prove production integration. Original commit-block statements were not accepted without command evidence. |
| Reviewer | Compared two rule-discovery tests by command and assertion, named surviving detection, and rejected deletion of distinct separator and filesystem/index divergence coverage. | Focused pytest attempts in read-only fixtures failed before collection because no usable temporary directory existed. Source-based review observations are not executable deletion-equivalence proof. |

Baseline actors also showed much of this behavior. The small matched sample
does not establish a causal reduction in future test growth, a permanent
test-count limit, or superiority across projects. It supports that the added
guidance can be followed without adding duplicate tests or sacrificing the
named boundaries in these cases.

## Blind assessment and adjudication

Two auditors received eight opaque samples containing outputs, task artifacts
and completed command observations, without variant labels or target guidance
bodies. Both accepted the bounded candidate implementer and reviewer outcomes.
One marked a baseline planner incomplete for naming only one discovery owner;
the other accepted its bounded scope. This difference does not establish a
statistical baseline/candidate advantage.

One auditor marked completion planner sample 7 deficient because it targeted
`cmd_charter` documentation rather than public CLI help. The other accepted
it. Coordinator adjudication: the fixture's Proposed outcome explicitly says
"Clarify the internal charter command description" and its needs-design
rationale says "internal validation and documentation only". The plan targets
the existing `cmd_charter` documentation, preserves registry dispatch and both
discovery owners, and separately covers the missing separator. Thus the
public-help interpretation is not a confirmed violation of this fixture's
scope. Its terse Problem sentence remains ambiguous; no public CLI help
change or completed planner delivery is claimed. The dissent is retained
rather than turned into an unanimous assessment.

Both audits noted unsupported ancillary commit-failure or escalation narratives
in implementer final prose. Completed command records establish RED/GREEN and
the completion commit, but not those claimed preceding failures. Those claims
are excluded from the result; this is a reporting limitation, not evidence
that the claims occurred. Neither reducing tests nor the new guidance caused
those narratives on the available evidence.

The cold reader raised six static candidates in unchanged baseline workflow
sections. It understood the new reuse paragraph and its distinct-boundary
exception. These candidates were not executed or confirmed as regressions;
they remain outside this bounded change, not repaired or counted as passes.

## Local audit trail

Local-only evidence locations (not portable repository dependencies):

- `/private/tmp/loom-native-dogfood-qgfp988v/activation-52/`: invocation,
  completed-event, output and observation files for all 52 routing trials.
- `/private/tmp/loom-native-dogfood-cold-reader/`: original prompt and stream.
- `/private/tmp/loom-native-dogfood-role-runs/`: pre-execution rubric,
  provenance hashes, baseline/candidate runs, initial environment failure,
  both parser failures, valid completion streams and anonymized audit bundle.

## Decision for this change

No confirmed violation of the four test-addition-value acceptance conditions
was observed in these bounded trials. Continue to independent acceptance
testing and closing review; this document is not an installed-host certification
or a blanket dogfood-pass stamp. Existing tests were not deleted. No product
guidance fix was made on the strength of unverified ancillary narratives.
