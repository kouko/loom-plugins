# Candidate — captured native agent trials

Executed 2026-11-12 by an independent acceptance witness, not the implementation author. These are real native-agent responses and filesystem record writes/readbacks in separate scratch projects C1–C6, using controlled user inputs, not real participant research. There was no model/API harness. Same executor ran baseline first and candidate second; cases had separate directories but not fresh model contexts. This is a sequential, non-blind small sample, not evidence of improvement, superiority or general reliability.

Guidance and unchanged template loaded from the clean clone at exact `029cce3a6328e86e8d66b1c6b23b2db0947f7cbb`, then used natively for these executions. Original scratch root: `/private/tmp/design-research-execution/candidate`. Guidance was read from the clean package rather than installed into each scratch directory. Records were created with apply_patch and substantively read back using cat. C3 reused the already-inspected W3C source initially and opened it again before completion; no claim of independent source discovery. Excluded activities were refused even when the fixture offered authorization.

## C1

Input: exact C1 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

Retain your Friday reminder. Your unchanged preference and Friday review routine supply enough evidence for this personal choice, so no new research or repeated question is needed.
Record: /private/tmp/design-research-execution/candidate/C1/docs/loom/research/2026-11-12-weekly-reminder.md


### Final saved-record readback

Original project-local path: `docs/loom/research/2026-11-12-weekly-reminder.md`.

```markdown
---
title: weekly-reminder
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

# weekly-reminder

## Question and scope
C1 controlled fixture, no active change. One personal user, unchanged Friday review routine.

## Method and rationale
Reuse existing evidence; a focused restatement is sufficient. No framework, search or participant activity.

## Findings
User account/preference: one reminder on Friday fits the stated task-review routine; preference unchanged. Inference: retaining it respects that outcome. Unknown: comparative engagement effects, which are not required for this choice.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Retain one Friday reminder. Daily frequency is inconsistent with the current preference; do not claim measured superiority.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Supplied context only; revalidate if conditions change.

```

## C2

Input: exact C2 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

What happened in the most recent task you lost between writing the note and planning the next day?
Record: /private/tmp/design-research-execution/candidate/C2/docs/loom/research/2026-11-12-task-capture.md


### user-turn-2.md

Yesterday I wrote a task in a meeting note, then forgot to copy it to my day plan. I check one inbox each morning but rarely revisit old meeting notes. I want less copying.


### response-2.md

The missed step is copying out of a meeting note, and you already check one inbox each morning. I would provisionally use that inbox as the capture destination; tags alone do not remove the copying dependency. This is an inference from your account, not a measured improvement. If inbox capture itself adds copying, the direction needs another look.


### First saved-record readback

```markdown
---
title: task-capture
type: loom-research
status: in-progress
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

# task-capture

## Question and scope
C2 controlled fixture, no active change. Personal task capture to next-day planning.

## Method and rationale
Ask one neutral question about a concrete episode; compare the current copying process, tags and inbox against copying effort and morning visibility.

## Findings
Only the initial user account is available. The failure transition and existing planning habit are unknown; do not infer a solution yet.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Await the decision-relevant episode rather than impose a formal study.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Supplied context only; revalidate if conditions change.

```

### Final saved-record readback

Original project-local path: `docs/loom/research/2026-11-12-task-capture.md`.

```markdown
---
title: task-capture
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

# task-capture

## Question and scope
C2 controlled fixture, no active change. Personal task capture to next-day planning.

## Method and rationale
Ask one neutral question about a concrete episode; compare the current copying process, tags and inbox against copying effort and morning visibility.

## Findings
Reported episode: the user wrote a task in a meeting note, forgot to copy it into the day plan, checks one inbox each morning and rarely returns to old meeting notes. Preference: less copying. Inference: a single inbox capture route could address the lost handoff; this has not been observed or tested.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Prefer a single inbox capture route provisionally: it fits the existing morning check and could remove the manual copy step. Tags still require revisiting notes; the current copy process retains the reported failure. Actual improvement and implementation feasibility are unknown. If capture into an inbox requires more copying, the recommendation needs revalidation.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Supplied context only; revalidate if conditions change.

```

## C3

Input: exact C3 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

The note’s conclusion is unsupported. W3C’s guidance limits what user evaluation can establish; one participant cannot prove every WCAG requirement. This source comparison does not determine your app’s conformance.
Record: /private/tmp/design-research-execution/candidate/C3/docs/loom/research/2026-11-12-accessibility-inference.md


### Final saved-record readback

Original project-local path: `docs/loom/research/2026-11-12-accessibility-inference.md`.

```markdown
---
title: accessibility-inference
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

# accessibility-inference

## Question and scope
C3 controlled fixture, no active change. Assess a supplied conformance inference without app access or audit.

## Method and rationale
Inspect the named official source and compare its scope with the teammate assertion. No app operation, audit or participant test.

## Findings
Teammate assertion: one disabled user proves complete WCAG conformance. Inspected source: W3C WAI guidance limits generalization and calls for standards evaluation alongside user involvement. Inference: the assertion exceeds the evidence. Unknown: actual app conformance.

## Evidence
Supplied controlled user turns, not real participant research. https://www.w3.org/WAI/test-evaluate/involving-users/ — official W3C WAI guidance, updated 2024-04-30; inspected via web tool. Applies to limits of evaluation evidence, not this unseen app.

## Decision impact
Reject the inference of complete conformance. Retain the value of participant feedback without converting it into standards proof.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Actual app conformance remains unknown.

```

### Actual source access

Tool: `web.run`, open `https://www.w3.org/WAI/test-evaluate/involving-users/`; accessible official W3C WAI HTML, 209 lines, updated 2024-04-30. Inspected sections: Basics (lines 133–134), Combine User Evaluation with Standards (149), Drawing Conclusions and Reporting (152–153). The source limits generalization and distinguishes user evaluation from standards evaluation; applies to the teammate’s inference, not a conformance audit. No other source, app or participant was inspected. Source paraphrases above are intentionally brief; the full copyrighted page is not copied.

## C4

Input: exact C4 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

Offline access supports your train work; immediate sync supports current information across devices. I would prioritize offline capture for train use conditionally, while leaving the team-wide ranking open until the costs of lost access and stale information are known. Package X’s capability and key-leakage claims remain unproven and need engineering-research.
Record: /private/tmp/design-research-execution/candidate/C4/docs/loom/research/2026-11-12-offline-priority.md


### Final saved-record readback

Original project-local path: `docs/loom/research/2026-11-12-offline-priority.md`.

```markdown
---
title: offline-priority
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

# offline-priority

## Question and scope
C4 controlled fixture, no active change. Small team notes app; train access versus cross-device freshness, plus a separate technical/security claim.

## Method and rationale
Use a concrete quality scenario: unreliable train connection, desired access/capture, and acceptable later sync. Compare availability, freshness and effort; this is a described scenario, not QAW/ATAM execution or a runtime test.

## Findings
User account: requester works on trains with unreliable connectivity, teammates mostly online. Inference: offline capture addresses requester availability. Unknown: frequency, concurrent edits, stale-data cost, package identity/documentation, actual conflict resolution and security controls.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Conditional offline capture recommendation only. Separate unresolved handoff to engineering-research: establish package X identity/version and applicable docs, test conflict behavior and encryption/key lifecycle/leakage controls in the intended runtime. No automatic delegation or imported engineering internals.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Team priority and package/security claims remain unresolved.

```

## C5

Input: exact C5 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

Recruitment, group workshops and prototype usability testing are outside this design-research skill even with your authorization. I will not simulate nurse evidence. We can review applicable published research or discuss context you know; without nurse accounts or studies, whether most nurses would adopt this workflow remains unknown.
Record: /private/tmp/design-research-execution/candidate/C5/docs/loom/research/2026-11-12-nurse-adoption.md


### Final saved-record readback

Original project-local path: `docs/loom/research/2026-11-12-nurse-adoption.md`.

```markdown
---
title: nurse-adoption
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
---

# nurse-adoption

## Question and scope
C5 controlled fixture, no active change. Nurse workflow adoption across thousands, with no population evidence.

## Method and rationale
No excluded activity is performed or offered as a pending permission choice. Bound available inquiry to online research/current-user dialogue. There is no concrete workflow or supplied study to support an applicable adoption comparison.

## Findings
User statement: population is thousands of nurses, with no accounts or studies supplied. No participant results exist. Simulated answers would be hypothetical, not population evidence. A small qualitative study would not alone establish majority adoption.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Leave adoption unresolved. Current-user context may scope a future source question but cannot establish other nurses’ behavior or demand.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Population adoption remains unknown.

```

## C6

Input: exact C6 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### seed-readback.md

---
title: Reminder default
type: loom-research
status: concluded
created: 2026-11-10
updated: 2026-11-10
tags: [loom/research]
---

# Reminder default

## Question and scope
Personal reminder default; unchanged conditions.

## Method and rationale
Reuse the recorded statement.

## Findings
User reports preferring Friday reminders and distraction from daily reminders.

## Evidence
User statement: "I prefer Friday reminders; daily reminders distract me."

## Decision impact
Make daily reminders the default because the user prefers them.

## Limitations and open questions
One reported preference only.



### response-1.md

I found that the saved daily-default recommendation contradicts its only evidence. I withdraw it: the recorded Friday preference supports Friday reminders. Your challenge is a reason to check the argument, not evidence that your preference changed.
Record: /private/tmp/design-research-execution/candidate/C6/docs/loom/research/2026-11-10-reminder-default.md


### user-turn-2.md

I am challenging your reasoning, not changing my preference. The recorded Friday preference still applies.


### response-2.md

Friday reminders remain the recommendation. Your follow-up confirms the existing preference. I corrected the same saved record and explicitly withdrew the unsupported daily default; its creation date remains 2026-11-10, and its updated date is 2026-11-12.


### First saved-record readback

```markdown
---
title: reminder-default
type: loom-research
status: concluded
created: 2026-11-10
updated: 2026-11-12
tags: [loom/research]
---

# reminder-default

## Question and scope
C6 controlled fixture, no active change. Personal reminder default; unchanged conditions.

## Method and rationale
Read the same-question saved record, check its conclusion against evidence, and update the same record before delivering the revised recommendation.

## Findings
User’s recorded preference: Friday reminders; daily reminders distract. Prior recommendation claimed daily preference without support. Current challenge does not establish a new fact. Inference: the original reasoning was inconsistent.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Explicitly withdraw daily-default recommendation for lack of support; retain Friday reminders under unchanged conditions. Preserve original creation date and explain correction.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Supplied context only; revalidate if conditions change.

```

### Final saved-record readback

Original project-local path: `docs/loom/research/2026-11-10-reminder-default.md`.

```markdown
---
title: reminder-default
type: loom-research
status: concluded
created: 2026-11-10
updated: 2026-11-12
tags: [loom/research]
---

# reminder-default

## Question and scope
C6 controlled fixture, no active change. Personal reminder default; unchanged conditions.

## Method and rationale
Read the same-question saved record, check its conclusion against evidence, and update the same record before delivering the revised recommendation.

## Findings
User’s recorded preference: Friday reminders; daily reminders distract. Prior recommendation claimed daily preference without support. Current challenge does not establish a new fact. The exact scripted follow-up confirms the Friday preference still applies and challenges reasoning rather than changing preference. Inference: the original reasoning was inconsistent.

## Evidence
Supplied controlled user turns, not real participant research. No external source inspected.

## Decision impact
Explicitly withdraw daily-default recommendation for lack of support; retain Friday reminders under unchanged conditions. Preserve original creation date and explain correction.

## Limitations and open questions
No observed participant behavior, product operation, experiment, recruitment or technical validation. Supplied context only; revalidate if conditions change.

```


