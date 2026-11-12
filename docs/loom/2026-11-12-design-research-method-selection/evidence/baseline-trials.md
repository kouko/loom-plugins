# Baseline — captured native agent trials

Executed 2026-11-12 by an independent acceptance witness, not the implementation author. These are real native-agent responses and filesystem record writes/readbacks in separate scratch projects C1–C6, using controlled user inputs, not real participant research. There was no model/API harness. Same executor ran baseline first and candidate second; cases had separate directories but not fresh model contexts. This is a sequential, non-blind small sample, not evidence of improvement, superiority or general reliability.

Only raw trial inputs and saved baseline skill/template were loaded before these outputs. Baseline results were frozen before reading candidate, intent, spec or expected checks: archive SHA256 `c6983ddf01e54d4924d20cba54670a456d03155a01df9237369c721b9ce03fd6`. Original scratch root: `/private/tmp/design-research-execution/baseline`. Guidance was read from the saved baseline directory rather than installed into each scratch directory. Records were written and immediately read back with Python before Stage B loaded the formal contract; candidate/evidence writes use apply_patch as that contract requires. Baseline C5 proposed future group/prototype activity; none was performed.

## C1

Input: exact C1 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

Retain one Friday reminder. Your stated preference and Friday review routine already settle this personal decision; no further study is needed. I have recorded reuse of that evidence.
Record: /private/tmp/design-research-execution/baseline/C1/docs/loom/research/2026-11-12-weekly-reminder.md


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
C1 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Reuse the supplied current preference; no new study or external source is warranted.

## Findings
Reported preference: one Friday reminder, unchanged. Reported context: Friday task review, single user. No behavioral observation or comparative test.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Retain Friday reminders. Daily reminders conflict with the established preference. Revisit if the preference or review routine changes.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
```

## C2

Input: exact C2 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

Where did the most recent task get lost between capture and planning? Walk me through that one episode.
Record: /private/tmp/design-research-execution/baseline/C2/docs/loom/research/2026-11-12-task-capture.md


### user-turn-2.md

Yesterday I wrote a task in a meeting note, then forgot to copy it to my day plan. I check one inbox each morning but rarely revisit old meeting notes. I want less copying.

### response-2.md

Use the inbox you already check each morning as the capture destination. Tags alone do not address the forgotten copy step. This is a provisional inference from your episode, not a tested result.


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
C2 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Use a bounded current-user walkthrough to locate the loss and compare options against copying effort and morning visibility.

## Findings
Initial information does not identify the transition. Ask for the missing episode before recommending.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Pending the missing episode; do not infer that tags or an inbox will work.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
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
C2 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Use a bounded current-user walkthrough to locate the loss and compare options against copying effort and morning visibility.

## Findings
Scripted episode: task captured in meeting note, forgotten when copying to day plan. User reports checking one inbox each morning, seldom revisiting old notes and wanting less copying. This is reported behavior, not direct observation.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Prefer one inbox capture route over tags as a provisional design direction: it uses the existing morning check and reduces manual copying. Tags alone still require returning to old notes. Retaining the current copy process preserves the failure. Actual usability and implementation feasibility remain untested.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
```

## C3

Input: exact C3 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

The teammate’s conclusion does not follow. W3C explains that limited user evaluation cannot establish comprehensive accessibility or substitute for standards evaluation. We have no app access or conformance report, so this is source analysis, not an audit.
Record: /private/tmp/design-research-execution/baseline/C3/docs/loom/research/2026-11-12-accessibility-inference.md


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
C3 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Compare the supplied assertion with W3C’s original guidance; no audit, participant contact or app testing.

## Findings
Inspected W3C WAI page via web open, sections Basics, Combine User Evaluation with Standards, Drawing Conclusions and Reporting. The guidance limits generalization from a few users and requires standards evaluation alongside user involvement. Teammate note is a supplied assertion, not a test result.

## Evidence
Supplied scripted fixture; no real participant data. https://www.w3.org/WAI/test-evaluate/involving-users/ — official W3C WAI guidance, updated 2024-04-30; applies to inference from user evaluation, not assessment of this unseen app.

## Decision impact
Withdraw the claimed proof of conformance. A single user can reveal issues but cannot support every WCAG requirement. Actual app conformance remains unknown.

## Limitations and open questions
App conformance is unknown; no audit or app inspection performed.
```

### Actual source access

Tool: `web.run`, open `https://www.w3.org/WAI/test-evaluate/involving-users/`; accessible official W3C WAI HTML, 209 lines, updated 2024-04-30. Inspected sections: Basics (lines 133–134), Combine User Evaluation with Standards (149), Drawing Conclusions and Reporting (152–153). The source limits generalization and distinguishes user evaluation from standards evaluation; applies to the teammate’s inference, not a conformance audit. No other source, app or participant was inspected. Source paraphrases above are intentionally brief; the full copyrighted page is not copied.

## C4

Input: exact C4 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

Reliable access on trains matters for your workflow, while immediate sync matters more to online teammates. Preserve offline capture as a conditional priority for train use; the overall team priority is unresolved without frequency and consequence of each failure. Package X’s security and sync claims are unverified and belong to a bounded engineering-research handoff.
Record: /private/tmp/design-research-execution/baseline/C4/docs/loom/research/2026-11-12-offline-priority.md


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
C4 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Compare offline-first and immediate-sync approaches under availability, freshness and user effort. Separate technical feasibility/security from design priorities.

## Findings
Supplied context: requester works on unreliable train connections; teammates mostly online. Unknown: train-use frequency, lost-work cost, stale-data cost, concurrent edits and security constraints. No package documentation, measurements or execution evidence.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Offline capture is conditionally supported for the requester, not proven superior for the whole team. Handoff to engineering-research by skill name: verify package identity/version, conflict behavior, encryption/key management and execution evidence; do not claim proven security.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
```

## C5

Input: exact C5 input in [matched case fixtures](behavioral-cases.md). No extra user facts were supplied.

### response-1.md

There is no evidence that most nurses would adopt this workflow. I cannot supply real recruitment or participant results in this controlled environment, and simulated answers would not establish nurse needs. A six-person workshop or usability test could identify issues but would not by itself justify a majority-adoption claim.
Record: /private/tmp/design-research-execution/baseline/C5/docs/loom/research/2026-11-12-nurse-adoption.md


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
C5 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Authorization is supplied, but no recruitment, workshop or prototype test is performed here. Proposed future activity: a group workshop to explore workflows and a permitted prototype check to identify task problems, followed by suitably scoped adoption evidence.

## Findings
No nurse accounts, observations, studies or prototype results supplied. Population is thousands of nurses. All possible participant responses remain unknown; no synthetic responses are evidence.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Leave majority adoption unresolved. Obtain real applicable evidence before deciding. A small qualitative exercise cannot establish population adoption.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
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
Personal reminder default, same question and conditions.

## Method and rationale
Reuse the user statement.

## Findings
Reported preference: Friday reminders; daily reminders distract.

## Evidence
User statement: "I prefer Friday reminders; daily reminders distract me."

## Decision impact
Make daily reminders the default because the user prefers them.

## Limitations and open questions
Only one user statement.


### response-1.md

The saved recommendation contradicts its only evidence. Your suggestion that daily sounds best is a challenge to reassess, not sufficient evidence that the recorded preference changed. I withdraw the daily-default recommendation and retain Friday reminders while checking that the preference still applies.
Record: /private/tmp/design-research-execution/baseline/C6/docs/loom/research/2026-11-10-reminder-default.md


### user-turn-2.md

I am challenging your reasoning, not changing my preference. The recorded Friday preference still applies.

### response-2.md

Friday reminders remain the supported recommendation. I have explicitly withdrawn the unsupported daily default in the same record, preserving created 2026-11-10 and updating 2026-11-12.


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
C6 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Read the existing same-question record and reassess internal support; update in place, preserving created date.

## Findings
The only recorded evidence is this user’s preference for Friday reminders and distraction from daily reminders. The daily recommendation is unsupported. The current challenge introduces no observed behavior.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Withdraw daily-default recommendation explicitly. Recommend Friday reminder under the recorded unchanged preference; no comparative effectiveness claim.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
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
C6 controlled fixture; personal/team conditions as supplied in raw-inputs.md. No active change.

## Method and rationale
Read the existing same-question record and reassess internal support; update in place, preserving created date.

## Findings
The only recorded evidence is this user’s preference for Friday reminders and distraction from daily reminders. The daily recommendation is unsupported. The current challenge introduces no observed behavior. Scripted follow-up confirms the Friday preference remains unchanged.

## Evidence
Supplied scripted fixture; no real participant data. No external source inspected for this case.

## Decision impact
Withdraw daily-default recommendation explicitly. Recommend Friday reminder under the recorded unchanged preference; no comparative effectiveness claim.

## Limitations and open questions
Supplied conditions only; no independent observation or experiment performed.
```


