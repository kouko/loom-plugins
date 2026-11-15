# Blinded audit one

## Scope and verdict

All six outputs are **acceptable**. No material or critical issue was found. Pairwise judgments: **C1 tie; C2 tie; C3 Y**. C3-Y adds a useful source-backed applicability distinction: today's JSON schema differs from the historical candidate. This is a modest quality advantage, not evidence of a general condition effect.

I read the three case requirements, rubric, six research outputs and six trajectories, and checked the material claims against the cited local implementation, tests, contract and historical records. I did not read variant instructions, manifest, protocol, other audits or memories. No tests, resolver calls, historical replays, network calls or installations were performed. Historical execution is treated as reported historical evidence, not witnessed execution in this audit.

Paths below are repository-relative. Output anchors refer to `docs/loom/research/2026-11-15-method-guidance-pilot/runs/`. Historical evidence anchors refer to `docs/loom/2026-11-11-intake-observation-pilot/evidence/`.

## Per-output findings

### C1-X — acceptable

- Correctly rejects universal repository coverage and local-CLI execution (`C1-X/research.md:23–28,33`). `scripts/run_package_tests.py:51–55` defines four roots; `:68–95` implements Python eligibility and root-local exclusion plus shell discovery; `:98–113` splits workflow sessions. The output correctly avoids turning workflow subfolder selection into universal exclusion of dotted/underscored descendants.
- Correctly identifies foreign-tree discovery and its limitations (`research.md:25`): runner `:123–149` filters nested repositories/worktrees, while `loom-code/scripts/repo_files.py:73–147` permits empty results when Git evidence is unavailable. Local hook test existence is corroborated by `loom-code/tests/local/test-superpowers-mode-on.sh:1–11`; this does not establish execution.
- Correct success scope (`research.md:27–29,33,37`): runner `:139–145` includes dependency installation/Mermaid checks; `:153–176` implements selected groups and first-nonzero return. It explicitly distinguishes zero subprocess exits from every test body running and disclaims fresh execution. Read test definitions at `tests/test_run_package_tests.py:222–298` corroborate intended exclusions without being passing results. Lock versions at `requirements-package-tests.lock:35–44` match.
- No consequential omission or misleading execution claim found.

### C1-Y — acceptable

- Same substantive coverage and execution guardrails (`C1-Y/research.md:25–30,34,38–42`), supported by the runner/helper anchors above. The concrete local test is a valid excluded counterexample.
- The phrase “discovery also filters node_modules” at line 25 is properly read with the output's eligibility-versus-pytest distinction: `_holds_tests` filters eligibility and `_shell_tests` filters shell inventory; this is not a claim that an explicit pytest ignore is universally installed. Its later pytest-configuration limitation prevents treating source eligibility as execution.
- Suggested success wording at line 38 abbreviates foreign-tree detection, but line 28 explicitly bounds it to Git-discovered trees and unavailable Git evidence. This is not a material overclaim in context.
- No consequential omission. Reading fewer test definitions than X does not weaken the decisive implementation evidence.

**C1 pair: tie.** Both answer discovery, root scope, exact root-local exclusions and observed-success boundaries. Extra corroboration in X does not change the supported decision.

### C2-X — acceptable

- Correctly separates supplied classifications from independent truth verification (`C2-X/research.md:23–25`). `loom-code/references/dispatch-profile.md:22–26` assigns assessment to the station; `loom-code/scripts/dispatch_profile.py:71–84` validates object keys and exact boolean types without corroborating task artifacts. `:263–299` supports the top-level/event/count validation account.
- Contradictory all-mechanical-plus-risk inputs really select mechanical by the first return (`research.md:27–35`; implementation `:80–84`). Standard/medium then becomes economy/medium, while complex becomes frontier/medium (`:147–160`). The contract explicitly gives mechanical precedence (`dispatch-profile.md:136–161`), so avoiding an unsupported contract-violation finding is correct.
- Test interpretation is appropriately conditional (`research.md`, Evidence and test meaning): `test_dispatch_profile_resolver.py:20–35,174–204` constructs supplied fixtures and asserts arithmetic/fallback. Implementation `:182–188` accepts supplied successful feedback; `_decision` `:105–124` checks supplied capability membership. Passing these tests would not prove real task risk, host invocation or acceptance. No test pass is claimed.
- No material issue found.

### C2-Y — acceptable

- Correct validation, missing/null versus empty evidence, overlap precedence and routing account (`C2-Y/research.md`, Findings), supported by the same classifier, entry point and initial-route anchors above. Its warning that a risk flag is not an unconditional safeguard against lowering the model is a valid bounded deduction, not a demonstrated real-world vulnerability.
- Useful test limitation: the CLI fixture compares JSON output to `resolve(payload)` (`test_dispatch_profile_resolver.py:559–580`), so agreement alone is not independent semantic validation. The output explicitly conditions test conclusions on actual execution and disclaims current test/runtime results.
- It also distinguishes a HEAD identifier from clean-tree identity and installed-host evidence. No material issue found.

**C2 pair: tie.** Y gives a useful additional CLI-test observation; X gives explicit compact input examples. Both retain all decision-relevant trust, precedence and execution distinctions.

### C3-X — acceptable

- Historical no-benefit conclusion is supported (`C3-X/research.md:23–24,36–38`). `comparison.md:5–20,170–190` and `acceptance-test-evidence.md:26–38` report six cases, one sequential consumer, 2,236 versus 2,681 packet bytes and no demonstrated incremental JSON benefit. The subtraction is 445. These records expressly do not measure model-token, parent-turn, monetary or total-latency savings.
- Correctly retains crash uncertainty and final-versus-candidate scope: `acceptance-test-evidence.md:52–101`, especially `:77,89–93`, records final guidance acceptance and correction of the shared crash-completeness overstatement. X does not relabel this history as newly executed evidence.
- Current-tree applicability correction is valid (`research.md:25,38`): `loom-code/scripts/loom_checker.py:576–621` already routes trailing intake `--json`; `command_handlers/intake.py:28–48` returns early on confirmation failure; `preparation_output.py:10–26` builds and populates structured results. It correctly declines to infer current removal authority or runtime correctness from the historical comparison.
- Its admitted lack of raw scoring inspection is acceptable because numerical and adoption claims are explicitly attributed to the inspected reports and independently supported there. No material omission found.

### C3-Y — acceptable

- Same supported bounded decision and safeguards (`C3-Y/research.md:25–29,39–45`). Its direct use of `consumer-scoring.json` correctly retains five-of-five real completeness resolutions for guided text/JSON, three for text alone, justified text unknowns, and the shared crash overstatement. These are reported semantic scores, not independent consumer samples or newly measured accuracy.
- Adds a consequential applicability detail at line 28: current `preparation_output.py:10–17` has schema_version/command/status/diagnostics/notices/error/suggested_next; the historical recipe in `comparison.md` uses state/checks_complete/failures. Therefore the old experiment is not a direct benchmark of today's interface. This is source-supported and usefully strengthens the recommendation's limits.
- Historical 42 net handler lines and 73 implementer-owned test lines match `acceptance-test-evidence.md:38` and `comparison.md:18`. Y explicitly avoids converting sunk effort into current marginal costs or savings. No material issue found.

**C3 pair: Y.** Both reach the correct bounded recommendation and inspect the final implementation. Y's explicit schema mismatch and direct semantic-score inspection improve applicability and preserve the distinction between justified unknowns and errors. This is not a length preference; X remains acceptable.

## Trajectories, citations and uncertainty

All six JSON trajectories parse. Their reported reads/actions are consistent with the outputs' bounded inspection accounts; none reports fresh tests, model reruns or external services. They are self-reported records, not independently captured complete tool transcripts. Missing actions cannot be inferred from omissions in their lists, and restrictions cannot be independently certified from those lists alone. No consequential prerequisite-read gap can be established without reading forbidden variant instructions; none is inferred.

I resolved every relative Markdown file target from its actual output directory; all exist, and numeric line anchors fall within their target files. Material cited passages were checked substantively against source. Historical heading links used for the comparison/acceptance claims point to the relevant sections; no Markdown renderer or UI behavior was verified.

Time and tool counts are not controlled efficiency evidence. Timestamp scopes differ (including acknowledged starts after orientation), tool-count schemas differ, and reported counts are not independently verified complete call logs. No exact model snapshot, token or monetary-cost telemetry is available. These six bounded results permit the pairwise quality judgments above; they do not justify a general speed/cost conclusion or production adoption verdict.
