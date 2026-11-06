# Relative iteration 3 — candidate behavior

## Outcome

In single observations the candidate retained informed automatic-publication
disclosure, wrote the ready code-only intent before confirmation, preserved
the explicit ongoing hold, and wrote the complete-CSV intent in Chinese. The
natural-default invoice draft did not repeat the prior unsupported daily-export
claim. The requested held-invoice chart passed width alignment; the two simple
CSV/PDF cases used tables instead of the misaligned unsolicited charts seen in
round 2.

However, the unknown-date reply categorically says today's date is not the
release date, which the evidence does not establish. The new inventory case
describes the currently filtered list's contents as manually selected, although
the supplied workflow says staff transcribe an already filtered list. Other
known ambiguities and omissions remain. These are two new unsupported claims,
not a zero-error or general release pass. The original baseline also had
different factual and premature-confirmation errors on these fixtures.

## Test

Eight isolated native Claude Code sessions used the same synthetic cases,
first-party `claude-sonnet-5-5` (all eight modelUsage receipts matched), and
requested medium effort. Original hooks and isolation preflight passed. There
were no observed permission denials, fixture commits or changed inputs. CLI
estimated cost is USD 1.2859135. `relative-iteration-3-data.json` retains
case inputs, replies, drafts, receipts and source hashes; email-shaped strings
are redacted. Released-baseline outputs are from the earlier paired test, not
the same batch. This is one author-reviewed observation per case, not a
statistically robust, independently judged or novel-case benchmark.

## Case notes

| Case | Observation |
|---|---|
| Unknown release date | Remains blocked and does not ask for ready confirmation. The reply states today's date is not the release date despite no evidence for that inequality; it also groups a marked unknown label with an invented actual date. |
| Incomplete CSV | Leaves required answers open. A full five-section preview is presented even though confirmation is not yet ready; it asks for answers before the later yes. |
| Complete CSV | Chinese intent and a table; the user-facing claim that existing filters affect only the on-screen list may overstate the source. The future duration of the fixture's `do not publish` wrapper is ambiguous, so do not label its opted-out treatment as a definite consent regression. |
| Natural-default invoice | Discloses automatic publication after both checks, opt-out and separate merge. The draft preserves the source's routine/occasional wording without adding a daily export frequency. The acceptance examples concentrate on multi-customer batches, so universal coverage remains worth inspecting. |
| Held invoice and explicitly requested comparison | Keeps the explicit ongoing hold. The graph has labeled outer panels and passes width-aware alignment. The reply and saved draft distinguish the intent file from unchanged project files. |
| Existing setup command | Writes the intent before confirmation, in Chinese. The wrapper's future publication scope is ambiguous. |
| New calendar setup | Writes a Chinese intent before confirmation and reports the saved draft separately from unmodified project files. The wrapper's future publication scope is ambiguous. |
| New inventory PDF | Writes a Chinese intent, uses a table, and retains permissions and fields. Its current-state table says stock is chosen manually, whereas the supplied current workflow is to transcribe an already filtered list; the table adds an unsupported distinction. |

No genuine repository implementation, push or PR was performed. The sampled
language and state improvements are local observations, not proof that the
new instructions caused them or will generalize to other cases or hosts.
