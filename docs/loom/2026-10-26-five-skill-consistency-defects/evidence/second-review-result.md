# Adversarial Re-review of 5 Findings

## Verdict Summary

| Item | Verdict | Priority |
|------|---------|----------|
| 1 | real-defect | P1 |
| 2 | real-defect | P2 |
| 3 | real-defect | P2 |
| 4 | real-defect | P3 |
| 5 | real-defect | P2 |

---

## Item 1 — P1: Deadlock when no successful attack, no covering test, adversarial step not skipped

**Verdict: real-defect**

**Why:**
- `adversarial.md:49-52` states a probe program is committed only when red against the change; an attack the change survives writes no new program.
- `adversarial.md:73-78` says when no attack earned a new program, the adversary names one existing repository test that covers the change as this change's program, **when such a test exists** — committing zero programs is allowed ("The count is a ceiling and there is no minimum", line 63-64).
- `probes.py:566-576` `missing_adversarial_execution()` refuses when `count < 1 and "adversarial" not in skip`: "at least one adversarial execution is required".
- `finalize.py:283-285` calls this with `len(adversarial)` — which counts the `adversarial` input array entries. If the adversary reuses no program (no covering repo test exists) and commits none, the input array is empty → count = 0 → refusal.

The deadlock is real: a change with no successful attack, no covering repo test, and adversarial step not skipped produces zero adversarial entries. The checker then refuses with "at least one adversarial execution is required" even though the prose says "no minimum".

**Smallest repair:** (b) checker — accept a recorded no-program run as satisfying the count. Add a sentinel in the adversarial input when the adversary reports zero programs but the step ran, e.g. `{"command": "adversarial-no-program", "artifact": "adversarial-no-program"}`, and make `missing_adversarial_execution` count such a sentinel. This preserves the "no minimum" prose intent without weakening the rule.

**New conflict:** None. The `direct_pytest_style_failure` check (`probes.py:693-716`) and `concern:` requirement (`probes.py:559-562`) apply to actual probe programs; a sentinel bypasses them by design. The ceiling check (`probes.py:554-558`) counts the sentinel, but it should not count toward the 5-program cap — add an exception for the sentinel in `check_adversarial_proportionate`.

**Priority: P1** (blocks finalization on a legitimate no-attack change)

---

## Item 2 — P2: "Reuse spends nothing against ceiling" but checker counts all supplied artifacts

**Verdict: real-defect**

**Why:**
- `adversarial.md:76-78` states: "Reusing a program this change already committed, or a repository test that already covers a case, commits no new program and so spends nothing against the ceiling."
- `probes.py:538-553` `check_adversarial_proportionate` builds `counted` dict from three sources: `committed_probe_programs` (store), `graduated_probe_programs` (suite), and `artifacts` (the `adversarial` input array). Every artifact in the input is added to `counted` (line 549-552), deduplicated by path.
- If a change already has 5 programs committed, and the adversary reuses one (by adding it to the `adversarial` input array), `len(counted)` stays at 5 — no problem. But if the change has 5 store programs **and** the adversary supplies a different reused repository test (not already in the store), `len(counted)` becomes 6 → refusal at line 554-558.
- The prose "spends nothing against the ceiling" implies the reused program should not count toward the cap at all. The implementation counts it if it appears in the `artifacts` input.

No prose reconciles this. The full `adversarial.md` was read — the reuse rule (lines 76-78) is the only ceiling-related text.

**Smallest repair:** checker — change `check_adversarial_proportionate` to exclude reused programs from the count. The `adversarial` input items can carry a `"reused": true` field (the protocol already supports `"confirmation"`), and the ceiling check should skip those. This matches the prose "spends nothing against the ceiling" literally.

**New conflict:** None. The `concern:` line check (`probes.py:559-562`) still applies — a reused program must carry a `concern:` line (it does, per `adversarial.md:89-90`). The `direct_pytest_style_failure` check is orthogonal.

**Priority: P2** (blocks legitimate reuse when cap is near full)

---

## Item 3 — P2: loom-memory routes equivalent entries to Reconcile, but Reconcile trigger covers only contradiction or narrowing

**Verdict: real-defect**

**Why:**
- `SKILL.md:130-131` (Record step 3): "Read `index.md` and search for an equivalent or contradictory live entry before creating anything. A match routes to Reconcile instead."
- `operations.md:75-78` (Record step 3): "Read `index.md` and search matching or nearby entries for one that already says this, or says something this would contradict or narrow. A match routes to Reconcile — never create a second concept for the same subject."
- `SKILL.md:145` (Reconcile Trigger): "**Trigger:** a new lesson contradicts or narrows a current entry."
- `operations.md:92-93` (Reconcile step 1): "Reconcile activates when a new lesson contradicts or narrows a current entry found during Recall or Record's search step — never as a separate discovery pass."

Record's routing includes **equivalence** ("already says this", "equivalent"). Reconcile's trigger explicitly does **not** include equivalence — only "contradicts or narrows". If an equivalent lesson arrives, Record routes to Reconcile, but Reconcile's trigger doesn't match. No path is defined for equivalence in Reconcile (step 3 says "replace the old one outright, or narrow it"; no "do nothing" option). Record step 4 says "Author exactly one concept file" — which would force a duplicate if Reconcile doesn't handle it.

**Smallest repair:** Extend Reconcile's trigger to include equivalence with outcome = no-op + provenance touch. Change `SKILL.md:145` and `operations.md:92-93` from "contradicts or narrows" to "is equivalent to, contradicts, or narrows". Add to `operations.md` step 3: "If equivalent, touch the `sources[]` to add the new evidence; no content change needed." This preserves the never-two-entries invariant with minimal text (two word additions in two files, one sentence in operations).

**New conflict:** None. The Retire trigger (`operations.md:108-109`) explicitly distinguishes "not a narrowing — that is Reconcile", so no overlap.

**Priority: P2** (undefined behavior on equivalent lessons)

---

## Item 4 — P3: Template 04's node labels violate the six-━ separator rule

**Verdict: real-defect**

**Why:**
- `mermaid-cot-spec.md:196-208` "Node label — exact shape" defines the separator as literal `<br/>━━━━━━<br/>` — six U+2501 (`━`). Line 204-205: "The separator is the literal `<br/>━━━━━━<br/>` — six U+2501 (`━`). Not `---`, not `<hr>`, not a different count."
- `node-structure.md:58-63` "Mermaid counterpart": "Flowchart rectangles use the page-mode div-label convention: `<div style='text-align:left'>TITLE<br/>━━━━━━<br/>• …</div>`"
- Template `04-reasoning-chain.md` lines 70 and 74 have measured separator runs of 18, 22, 25, and 23 U+2501 characters — all violating the six-character rule.
- `verify_cot_html.py:60` defines `SEP = "<br/>" + "━" * 6 + "<br/>"` and line 467-471 fails if `label.count(SEP) != 1` — the checker enforces exactly six.
- `test_references.py:531` asserts `"<br/>━━━━━━<br/>"` exists in `node-structure.md` — the test pins the spec, not the template.
- The template's Mermaid is hand-authored (not generated). `SKILL.md` routes template 04 as "Reasoning chain" with `templates/04-reasoning-chain.md` (line 67). The spec's "Who owns what" table (lines 8-12) puts node-label format in the **Layout** layer, which applies to both page mode and chat templates — the spec doesn't restrict it to page mode.

**Smallest repair:** Normalize the four separators in `04-reasoning-chain.md` to exactly six `━` characters (matching `<br/>━━━━━━<br/>`). No test or checker changes needed — the existing `verify_cot_html.py` already enforces this, and the template simply wasn't updated when the spec stabilized.

**New conflict:** None. The change aligns the template with the existing enforced rule.

**Priority: P3** (cosmetic inconsistency in an example template; the checker already catches it on render)

---

## Item 5 — P2: pytest probe command form wording narrower than examples and implementation

**Verdict: real-defect**

**Why:**
- `adversarial.md:145-147`: "A probe file that defines test functions or test classes must be recorded as `python -m pytest <artifact>`: `finalize-review` refuses a bare `python3 <artifact>` run of it."
- `adversarial.md:134,136` and `SKILL.md:402` use `python3 -m pytest <path>` (with `python3`, not `python`).
- `probes.py:687-690` `runs_pytest()` accepts any executable whose name starts with `python` (`Path(tokens[0]).name.startswith("python")` and `tokens[1:3] == ["-m", "pytest"]`) — so `python`, `python3`, `python3.11`, etc. all pass.
- `_python_argv()` (lines 671-684) also unwraps `conda run -n ENV python -m pytest` and `uv run python -m pytest` — wrapper launchers are accepted.
- `adversarial.md:161-174` table lists "unittest" runner as `python -m unittest` (pytest's python/uv/conda launchers) — acknowledging wrapper launchers.

The rule text says `python -m pytest` as the only accepted literal; examples use `python3 -m pytest`; implementation accepts `python* -m pytest` plus `uv run`/`conda run` wrappers. A reader could take the rule literally and think `python3 -m pytest` is rejected.

**Smallest repair:** Reword `adversarial.md:145-147` to: "A probe file that defines test functions or test classes must be run with pytest through a supported Python invocation (for example `python3 -m pytest <artifact>`); a direct `python3 <artifact>` run is refused." This matches `runs_pytest()` (any `python*` prefix), `_python_argv()` (uv/conda wrappers), and the examples.

**New conflict:** None. The `direct_pytest_style_failure` check (`probes.py:693-716`) already implements exactly this logic — it only refuses bare `python3 <artifact>` runs of pytest-style files.

**Tests pinning current text/examples:**
- `test_loom_runtime_skill_commands.py:35-36` asserts exact strings `'"command":"python3 -m pytest <path>"'` in SKILL.md and `'"command": "python3 -m pytest docs/loom/<change-id>/evidence/probes/test_abuse_empty_input.py"'` in adversarial.md
- `test_probe_direct_python_pytest_style.py:50` asserts `f"python -m pytest {PROBE}" in result.stderr` (note: `python` not `python3`)
- `test_loom_attestation.py` lines 1045-1063 test many `python3 -m pytest` variants as accepted commands

All must be updated in the same change.

**Priority: P2** (documentation-implementation mismatch misleads readers)

---

## Missed Defects

1. **Template 02 and 08 also violate the six-━ rule**: `02-linear-steps.md:62` has `━━━━━━━━━━━━━━━━━━━━━━━` (23 chars), `08-system-architecture.md:63` has `━━━━━━━━━━━━━━━━━━━━━━━` (23 chars). The checker `verify_cot_html.py` will fail these on `--render`. Same root cause as Item 4.

2. **`adversarial.md` reuse rule (lines 82-90) says "Before writing any probe, the adversary checks what already covers the target... It reuses a program that covers a case" — but the protocol doesn't specify how the adversary signals reuse in the `adversarial` input to `finalize-review`. The `finalize.py:293-329` loop doesn't check for a `reused` flag; it only validates the command form. This is the mechanism gap behind Item 2.

3. **`loom-memory` SKILL.md line 18 says "loom-memory owns repository lessons that outlive a change... content does not move automatically between them" but operations.md Record step 1 (line 47-59) fails "a decision whose relevance is bound to one commit or PR (git-memory owns that)" — yet the boundary is fuzzy: a lesson learned during a change that *happens* to be durable but was observed in the change's context has no clear home. No test covers this boundary.**

---

## Second-Opinion Deltas

| Codex Framing | My Finding |
|---------------|------------|
| Item 1: "adversary may reuse a program this change already committed (line 76-78)" — asked if that changes the answer for a change that never committed one | **Yes, it doesn't change it.** The reuse path requires an *existing* program (either store or repo test). A first change with no covering test has nothing to reuse → deadlock stands. |
| Item 2: "if finalize-review is handed 5 store programs plus 1 reused repository test, the count reaches 6" | **Confirmed.** But also: the reused program must be in the `adversarial` input array to be executed, and the checker counts every array entry. The prose "spends nothing" is violated by implementation. |
| Item 4: "is the separator rule scope chat templates or only page mode?" | **Applies to both.** Spec's Layout layer (mermaid-cot-spec.md:8-12) owns node-label format; SKILL.md routes template 04 as a reasoning chain using the same Mermaid conventions. No scope restriction in either file. |
| Item 5: "reword to 'supported Python invocation... wrapper launchers (uv run, conda run) also accepted'" | **Accurate.** `runs_pytest()` and `_python_argv()` accept exactly those. The proposed wording is correct and complete. |
| Codex didn't note the two other templates (02, 08) with the same separator violation | **Added in Missed Defects #1.** |
| Codex didn't note the missing `reused` flag mechanism in the finalize-review input schema | **Added in Missed Defects #2.** |

---

Report written to `/tmp/loom-codex-review/result-subagent.md`