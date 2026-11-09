# Git delivery enforcement — complexity analysis

Mode: complexity. Mindset: Design is taking apart. Keep observation, permission and enforcement separate; reuse existing entry points rather than adding a second workflow owner.

## Q1 — Smallest equivalent end state

Keep publish and land as the only writers. Add a read-only delivery observer and a Git-native protection capability. Give existing command refusals explicit categories and remedies without a global recovery registry. Thin host adapters invoke the same observer where the host can support it. Do not add a daemon, scheduler, retry queue, receipt ledger, second publisher, mandatory draft-PR lifecycle, or blanket rewrite of unrelated errors.

The proposed separate command-handler module is optional: expose a small cmd_delivery entry from the observer itself if it meets the module criteria. Avoid two files whose only distinction is argument parsing. Hooks must distinguish human decision boundaries and an evidenced external blocker from premature task completion; a hook firing at the end of a turn is not proof the whole task should have finished. This applicability check is part of required behavior, not a later enhancement.

## Q2 — Measured baseline and estimated growth

Source inspected at 4c555b14. Four existing handlers total 2,199 lines and 71 Python functions: publish 657/13, land 1,155/41, push 109/5, github_rules 278/12. Other touched integration surfaces include checker entry 105/1, helpers 390/23, OpenCode loader 323 lines and Antigravity adapter 301/18. These scopes overlap no files; they are not the entire repository.

Seven relevant existing test modules total 3,588 lines and 183 test functions before parametrization: test_loom_publish 1427/65, test_land_merge 601/27, test_github_rules 350/18, test_main_branch_hook 83/6, test_hooks_json 460/27, test_opencode_loader 263/14, test_agy_adapter 404/26. Counts describe current coverage, not new test requirements or passing execution.

Initial broad estimate of 300-600 added runtime lines excluded meaningful hook activation, installer preservation and cross-host handling. It is not a supported total estimate and is superseded here. Tentative bounded design allowance: 500-900 net runtime lines across 2-4 new capability/adapter modules and existing consumers, 15-30 functions; 500-900 net regression-test lines across 3-6 added test modules plus affected existing modules; 60-120 net hand-maintained configuration/contract/documentation lines, excluding generated release metadata. These are pre-spec planning ranges, not measurements or quotas. Host feasibility can invalidate them. Count generated manifests separately during implementation.

Observation overlap is substantial: publish already compares local HEAD to live remote refs and PR head/base/repository; land already checks PR identity, all checks and the merge result. Its two check loops are not identical: publish watches required checks, land watches all registered checks. Preserve that policy distinction rather than merging the loops merely to save lines. Reuse semantic state evaluation and evidence, not a generic callback framework.

## Q3 — Deletions

Verified replaceable behavior: superseded station text claiming publication hooks universally only remind; reminder-only explanations that treat Git policy as a workflow-simplification choice. Reuse the existing branch/remote/PR observations instead of copying them into an independent delivery engine. No whole production function is yet proven deletable; zero executable deletion credit is counted. Keep the shallow shell guard as early feedback until native Git protection is confirmed installed; removing it globally would reduce coverage on unprotected repos.

## Verdict

RESHAPE the initial file-by-file proposal into the smaller composed design before implementation. The goal survives; the earlier growth estimate and suggestion of universal end-of-turn enforcement do not. An equivalent smaller alternative retains mechanical observation, Git-native ordinary-operation protection and actionable structured refusals, but deletes the proposed independent command-handler layer when unnecessary and avoids centralized recovery orchestration.

Proceed with implementation only after the spec resolves hook applicability, preservation of existing Git hooks, observed versus unconfirmed server protection, remote-only versus local-only delivery, and the lack of a universal unbypassable local Git hook. No new user outcome is substituted: unsupported host enforcement must be disclosed rather than claimed. No host capability has yet been established by runtime observation.

## Evidence and verification

Counts produced with Python ast and splitlines over the actual sources. Source inspection: publish.py cmd_publish/_cmd_publish_trusted/_observe_required_ci; land.py _merge_preconditions/_observe_all_checks/_verify_merge; github_rules.py _ruleset_state/setup_command; push.py _protect_main; opencode/loader.js registerHooks. Existing hooks register startup and pre/post-tool behavior, not a universal termination gate. The user's selected native Git enforcement intentionally revises the current no-Git-hooks fixed choice; installations and other-repo server changes remain outside the current authorized implementation.

## User-directed reuse amendment

After this assessment the user asked whether existing scripts could be shared or merged, and accepted the reuse direction. The spec now places delivery observation in publish.py, native Git protection in push.py, and shares CI classification with land.py. No new delivery command-handler or git_protection.py is planned. The earlier numeric growth range remains an uncertain ceiling estimate, not a claimed reduction; measure the final diff and count functions/files again. The behavior and seven Acceptance lines remain unchanged.
