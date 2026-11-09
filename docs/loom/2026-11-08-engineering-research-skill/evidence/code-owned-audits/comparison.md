# Independent blind audit comparison

These are two advisory dogfood draft judgments, not formal closing-review verdicts. Both actors received identical frozen input and no author findings or the other actor result. No production edits or commits were performed.

| Case | A01 | A02 |
|---|---|---|
| F01 | met | met |
| F02 | met | met |
| F03 | met | met |
| F04 | met | met |
| F05 | partial | partial |
| F06 | partial | met |

Both find sound scoped source research, preserved sources and authorization boundaries. Both establish the approved F06 copy/readback/hash/links, while leaving broader lifecycle cleanup uncertain. A01 treats that uncertainty as reducing F06 to partial; A02 limits its met judgment to the explicitly authorized operation. Do not silently resolve this disagreement into an overall pass.

For F05, A01 allows an unresolved destination under the declared no-CLI fallback. A02 records a low-severity request-fit concern and asks for a complete proposed project-relative destination. Both identify narrower cleanup evidence and recommend qualifying any broader eligibility wording. No shared high-severity defect was reported. These are actor judgments, not an orchestrator adjudication.

Raw answers and complete filtered observable audit trajectories are in A01/ and A02/. Executor packet remains at the raw root recorded in freeze.json. All original observable executor calls remain in that frozen packet; auditor read deduplication did not delete evidence. Reasoning text was not retained; usage counters may include reasoning tokens.

Model/provider/effort were explicitly requested as gpt-6.1-sol/openai/medium with isolated HOME/CODEX_HOME, empty proxy environment inheritance, native first-party Codex CLI, read-only sandbox and separate 300-second bounds. The CLI receipts do not server-attest the served model version. Both exited 0 without timeout; packet hashes stayed identical; temporary auth symlinks were removed.
