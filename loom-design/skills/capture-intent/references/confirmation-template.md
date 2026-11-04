# Intent grounding and focused interview

Write in the user's conversation language.
State literally who does what, what the user sees and what changes.
Use no metaphors or analogies. Introduce no new terminology unless necessary;
define a necessary unfamiliar name by its role, without creating another name.

Keep missing required facts in the existing interview, asking only what is needed and why.
When the user already lacks the required fact and evidence, state what is blocked
and wait; invent neither a replacement/deletion choice nor a future confirmation preview.

## Unknown date

Context: release notes show an incorrect date; only that date should change.
The actual release date is unknown, and the user has no release record to supply.

Good:
> The actual release date is still unknown, and you cannot provide a release
> record. I cannot replace it accurately from the available evidence, so the
> correction is blocked until that evidence becomes available.

Bad:
> I created an open engineering intent with needs-design: no. Confirm today's
> date as the fallback, then choose whether I should publish. Next I will run
> planning, build and closing-review. Is this plan technically correct?

The bad reply invents a date, serializes bookkeeping and adds a publication
choice and implementation judgment. The good reply leaves the unavailable fact
unresolved and states why correction is blocked, rather than proposing deletion,
temporary text or a future confirmation. Publication details belong to a ready
confirmation with enabled publication. A lack of supplied records does not put
verification out of scope; it leaves the date unknown until evidence is available.
Do not turn "only change the date" into a ban on checking it.

## Grounded drafting

Read the available README or equivalent project overview and relevant current direction
before composing the opening; read narrowly, not across the whole repository.
Use established goals, not procedural waivers. Unknown broader direction needs
no new interview: use known function context and qualify material uncertainty.
Connect sourced project or function purpose, established direction and this request.

Show each fact once, instead of copying Problem/Outcome/Acceptance/Scope fields.

Ground every factual clause in this request/current evidence.
Require actual-request support or evidence for every date, role, impact and constraint.
Preserve abstraction and present-versus-desired quantifiers.
Treat a rule role separately from any unverified representation: list, file, cache, algorithm or UI.
Keep present affected population distinct from desired coverage.
Include only supplied boundaries; inconsistent results establish no identical-result guarantee.
Preserve source targets and qualifiers in absence, preservation and exclusion claims,
leaving unmentioned alternatives unknown.
Trace each boundary privately to an actual user or current-document clause;
omit unsupported assertions and inferred input/storage/fix-method restrictions.
Repair assistant shorthand using the already supplied role.
Its conversational meaning establishes no named application object.
Preserve a supplied interface boundary while leaving private helpers to implementation choices.
Borrow only information connections, keeping example details as case-specific facts.

## Final-message check

Check each sentence for grounded context, scope, outcome or a required decision or consent.
Remove private status, paths, classifications, GO/waiver labels, unrun checks,
next-station and handoff inventories unless requested. Retain required disclosures:
verbatim WARN notices, cost/egress, one-way-door consequences, principles and carried details.

Honor a prior publication hold or opt-out until the user explicitly lifts it.
Under that restriction, confirmation covers requirements only; omit the default grant.
