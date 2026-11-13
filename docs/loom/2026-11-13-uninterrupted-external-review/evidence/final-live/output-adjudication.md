# Final live output adjudication

Decision: the caller's stated reason does not justify rejecting the whole leg as `unbacked-claim`. The raw review describes an environment-inheritance weakness and its failure mode, not an observed incident in this execution. This does not establish that every vendor finding is correct, or that any secret was present or transmitted to a remote service.

## Exact rule and disputed text

`loom-workflow/skills/independent-advisor/references/report-contract.md:45-46` defines `unbacked-claim` as “a claim cites a path or fact that does not check out”. The main skill requires mechanical checking and rejection of unchecked claims (`SKILL.md`, The report). Neither rule requires a concrete incident to have happened before a source-grounded conditional risk can be discussed.

The raw `result.json` review_output, Core claim item 3, says:

> **The child inherits the full environment.** (Popen, L151–153)
> Other vendors' API keys and tokens reach every CLI.
> Type: judgement call.
> Confidence: medium. CLIs may need some variables, such as HOME.

Its separate **Failure modes** section says:

> Secrets in the environment leak to a vendor CLI (item 3).

The opening explicitly bounds its evidence: “Read-only review of the pasted `target.py`. I made no edits and ran no commands.” It does not say it inspected the actual environment, observed a secret, observed a network transmission, or witnessed a leak in this run.

## Source check and classification

- Source-supported mechanism: `/private/tmp/loom-uninterrupted-final-live/target.py:151-153` launches `subprocess.Popen` with no `env` argument. The launch path does not filter inherited environment variables. The same `_launch` implementation runs the CLI commands produced at `target.py:472-491`; invocation occurs at `:557-559`. Exported variables available to that parent launch can consequently be available to the selected child CLI.
- Design judgement: whether an environment allowlist is warranted, and whether its operational cost is low. The vendor labels item 3 judgement-call/medium and proposes an allowlist with per-CLI testing. The code supports discussing the mechanism; it does not establish the proposed mitigation's completeness or cost.
- Conditional failure mode: secrets already in the inherited environment become accessible to that CLI. The failure-mode sentence is listed under that explicit heading and says “to a vendor CLI”; it does not say those values reached a remote vendor service. Local child-process exposure and remote data transmission are distinct.
- Unsupported as an incident assertion: actual other-vendor keys existing in this execution, their values, CLI use of them, and remote egress. No such facts are proved. Crucially, the raw text does not assert a particular observed incident; the caller's report adds that reading when it classifies the text as “將條件風險寫成已發生事實”.

The sentence “Other vendors' API keys and tokens reach every CLI” is categorical and insufficiently qualified on its own: it should not be repeated as proof that such keys exist, or that all credentials stored anywhere on the machine are inherited. Its heading, source anchor, medium confidence and failure-mode placement support the narrower environment-exposure reading. This ambiguity merits a qualification in the audit report, not the caller's high-confidence finding that an incident was fabricated. I am not rewriting the vendor's words into an observed event, nor treating its categorical phrasing as fully precise.

## Other findings and limits

Direct source inspection also supports several substantive observations independently of item 3: consent checks contain no packet digest or expiry (`target.py:70-111`); Antigravity puts the prompt in argv (`:488-491`); output accumulates in lists (`:155-176`); and Claude has no explicit executor/family compatibility check before candidate acceptance/probe (`:530-558`). These establish that the output adds real analysis rather than merely restating input. They do not validate every consequence, severity, or hardening proposal.

Some vendor statements remain uncertain or overbroad: “Anyone on the host” being able to inspect argv depends on OS/process visibility; helper-model and stderr-echo scenarios are expressly conditional and were not demonstrated; PID-reuse is called theoretical. The consent-quote discussion omits the importance of the required `selected_executor` equality visible at `target.py:61`, although it correctly identifies that negation is not semantically interpreted by that function. These points limit how the report should attribute the findings. I found no demonstrated false concrete fact in those lines that independently supplies the caller's stated whole-leg rejection rationale; I have not exhaustively validated every OS/CLI-dependent statement.

## Outcome

The existing `validation.json` correctly confirms environment inheritance but then applies a stronger interpretation than the raw evidence warrants. Its whole-leg `usable_leg: false` on the stated secret-incident rationale should not be retained as a grounded adjudication. A usable audit can preserve the vendor text as untrusted, qualify item 3 as conditional exposure with actual secret presence and remote egress unverified, and distinguish its supported mechanism findings from design judgements and speculative failure modes. This is not a formal owner verdict or an endorsement of all suggested code changes.

Execution and output quality remain separate: the saved result has status completed and observed model `claude-sonnet-5-5`, with effort only accepted explicitly; whether the caller ran without a second answer is trajectory evidence, not something the returned review can itself attest. This adjudication makes no additional outside call, changes no production artifact, and does not alter the prior closing-code verdict.
