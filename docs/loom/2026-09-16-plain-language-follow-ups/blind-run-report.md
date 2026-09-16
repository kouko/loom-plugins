# Close the follow-ups left by the plain-language reminder change — what I tried and what happened

Tried on 2026-09-16, in a fresh copy of the project at 4ddf5478 (not the working copy the change was built in).

## What you asked for, one line at a time

### 1. A card sentence whose meaning is negated fails the card tests, and an executable adversarial case covering the coexist card records that failure.
- **How I tried it**: In the fresh copy I changed one sentence of the reminder used when the other diagram plugin is also installed, from "Verify prescribed box diagrams" to "Never verify prescribed box diagrams", ran the reminder's tests, then put the sentence back.
- **What happened**: The tests went red. One failure named that exact sentence as the problem, a second flagged the added word pushing the reminder over its word limit. The previous change's attack program now also holds two cases aimed at this reminder: one flips the table sentence, one flips the checking sentence.
- **Evidence**: 2 failed, 81 passed on the flipped copy (the card hook tests); the two attack cases are named "coexist-markdown-table-negated" and "coexist-align-verify-negated".
- **Verdict**: works.

### 2. No shipped text of the plugin calls the per-turn card a "trigger card" while its own header does not; the three README languages, the changelog, the Codex description and the hook docstring agree on one name.
- **How I tried it**: Searched the three READMEs, the Codex description and the hook's own description for "trigger card", then read what they call it instead.
- **What happened**: All of them now say "visualization card", which matches the card's header. The hook description only says "diagram trigger instruction" in passing. The changelog's older entries still say "trigger card", because they describe what shipped at the time.
- **Evidence**: search returned no "trigger card" in the READMEs, Codex description or hook text; the changelog's 5.3.0 entry still uses the old name.
- **Verdict**: works. See "I decided for you" about the changelog.

### 3. The repository's memory store holds the two lessons from the previous change, each with the evidence it came from.
- **How I tried it**: Read the lesson files this branch added or changed.
- **What happened**: The routing lesson is a new entry. It records that the guide was opened 0 times in 6 trials and that the inline rule worked in 5 of 5, and it points to the earlier blind-run report and its trial transcripts. The phrase-presence lesson was added to an existing entry about tests that pass a flipped rule rather than getting its own file. It now says the problem came back on the reminder, and that loosening a check is how it came back, and it points to the earlier review record and attack program. A third lesson was added too: a narrower rule has to say which case it overrides.
- **Evidence**: the new "an inline rule reaches replies that a routed guide never does" entry; the extended "a prose pin must require an affirmative un-negated sentence" entry; one commit records all three.
- **Verdict**: works.

### 4. `loom-code` declares one new version above 3.7.0 across every place it states its version, and the repository's own consistency checks accept it.
- **How I tried it**: Read the version in the three plugin manifests, the root README and the three loom-code READMEs, and ran the Codex manifest sync check.
- **What happened**: All of them say 3.7.1. The sync check reported no drift, and the package tests that compare these version numbers passed.
- **Evidence**: all seven places show 3.7.1; the manifest sync check exited cleanly.
- **Verdict**: works. Whether your installed copy actually refreshes can only be seen after merge, as the intent says.

### 5. The repository's package tests and mechanism checks pass, and the number of registered mechanisms does not grow.
- **How I tried it**: Ran the package suite with the command the project uses, then recomputed the mechanism count against the current trunk.
- **What happened**: The suite finished with exit code 0. The mechanism check said "all clear", with 136 mechanisms on this branch and 136 on trunk. The check that runtime text cites no repository records also passed.
- **Evidence**: package suite exit 0; mechanism recompute "net 136, baseline 136, all clear".
- **Verdict**: works.

### 6. When the agent asks or answers how to do something, the per-turn reminder says that doing nothing or later, a smaller version, and combining two options are each offered or ruled out, and both reminder versions stay within 181 words.
- **How I tried it**: Read both reminder versions and counted their words.
- **What happened**: Both say "list or rule out doing nothing or later, a smaller version, and combining two". The full version has 172 words and the other has 181, which is exactly the limit.
- **Evidence**: word counts 172 and 181; the suite's word-limit test passed.
- **Verdict**: works. The second version has no room for even one more word.

### 7. The reminder names the everyday situations that carry a table, so an agent reaches them without opening a separate file.
- **How I tried it**: Read both reminder versions for the eight situations.
- **What happened**: Both name all eight: progress, a before and after, what each choice means, readiness, confirmed against unconfirmed, findings, risks, and supported environments.
- **Evidence**: the text of both cards as shipped.
- **Verdict**: works. I did not run a live session to see an agent actually draw a table from this.

### 8. Shaped content in a reply is a markdown table by default, and the drawn form is kept for places that cannot show markdown; no rule still says to prefer the drawn form because of the client.
- **How I tried it**: Read the visualization skill's rules for choosing a form, the client reference, and the client-detection tool, and searched for any rule that still pushes the drawn form for a terminal or remote viewer.
- **What happened**: The skill says a chat reply gets a markdown table by default, and the drawn form is for code comments, commit messages or plain-text files. It says outright that the client never decides between the two, and a remote viewer now only matters for whether Mermaid is safe. I found no rule left that prefers the drawn form because of the client.
- **Evidence**: the visualization skill's "Which of the two forms to send" rules; the client reference saying the remote viewer "changes nothing here".
- **Verdict**: works. This checks the written rules; I did not watch a live reply.

## 對你既有的資料做了什麼 (what this did to data you already had)

Nothing. The change edits plugin text, tests, version numbers and the repository's lesson notes, and it reads or rewrites none of your own files. Your installed loom-code stays as it is until you update the plugin after merge.

## I decided for you

- **Old changelog entries keep the name "trigger card"**: the plan decided to rename only the current descriptions, because a changelog entry records what shipped at the time. Changing it later means editing old history lines.
- **The phrase-presence lesson extends an existing note instead of getting a new one**: the store already had a lesson on exactly this problem, so the new evidence was added to it. You will find it under that older title.
- **No reviewer dismissals were passed to me**, so none are listed.

## Things I am not sure you want

- The second reminder version is at exactly 181 words, and you said the limit will not go up again in this change. The next wording fix will have to cut words somewhere else. Is that acceptable?
- Acceptance lines 7 and 8 are proven only in the written rules, not by watching an agent reply live. Do you want a live trial before you accept?
