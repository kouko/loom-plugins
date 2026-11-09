# Probe A observed routing findings

See design.md for limitations, frozen labels and ambiguity sensitivity. No global dogfood verdict.

## Completed observations

50/50 fresh trials valid; 0 timeout or harness errors. Target body was actually read in 40/40 positive trials and 0/10 negative trials. All-label positive and negative rates: 100% each. Excluding predeclared ambiguous P10/P18/P20, 34/34 positive and 10/10 negative trials matched labels. No observed trigger-miss or over-trigger in this corpus; this is no global dogfood verdict.

Native catalog receipts verify target name and all five adjacent descriptions, with the selected target body marker absent before execution. Target reads require a completed command whose output contains actual target body text. Each run retains prompt.txt, catalog.json, config.toml, events.jsonl, answer.txt and receipt.json, including target read command evidence. The 50 trials have distinct native thread IDs; frozen corpus/design/harness hashes remain unchanged. See summary.json and verification.json. Raw operational traces exclude reasoning items before writing.

Limitations: description unchanged, so no claim of trigger improvement over revision-4; no installed hooks or Claude Skill() testing. This measures route selection only, not workflow compliance or research correctness. Questions have clear engineering stakes, and five negatives cannot establish broad precision. Repetition is a small stochastic sample, not independent production reliability. Designer saw prior corpus embedded in orchestration reference, disclosed before freeze; old results were not read and old runner queries were not reused. No factual benchmark outcomes or private-session/vault material supplied. Config pins requested first-party OpenAI gpt-6.1-sol medium, but does not establish immutable backend weights. No observed mismatch means no localized fix recommendation is supported by Probe A.
