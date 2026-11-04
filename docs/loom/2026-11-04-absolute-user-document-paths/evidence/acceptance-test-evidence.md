# Absolute user document paths — acceptance test evidence

Tried on 2026-11-04, in a clean copy of the project at adad5c7cd2830bc783c9325fbf2feed53989e605.

## Setup and witness boundaries

- Independent acceptance witness: native Codex subagent `/root/acceptance`; it implemented no part of the change.
- Clean copy: `git clone --no-hardlinks /Users/kouko/GitHub/loom-plugins /tmp/loom-absolute-acceptance-adad5c7`, then `git checkout --detach adad5c7cd2830bc783c9325fbf2feed53989e605`. `git rev-parse HEAD` returned the exact tested SHA. `git status --porcelain` returned no entries, before and after focused tests.
- Read README installation instructions for the three independently installable plugins. Existing `codex plugin list` completed with a remote catalogue warning under restricted network access; this inventory does not establish that the new version is installed. Installed plugin copies were not changed, as the intent excludes that work.
- Clean source load: `bash loom-code/hooks/session-start </dev/null` returned valid JSON with `hookSpecificOutput.additionalContext`. Parsing it confirmed the absolute-path, active-worktree and preservation guidance. Each cold driver read the clean-copy guidance specified below. This verifies source instruction loading, not a new global host installation.
- Fixture project `/tmp/Delivery Project 專案` was initialized with Git. `git worktree add --orphan -b fixture-branch '/tmp/Worktree 分支'` created a separate linked worktree. Its document `docs/設計 草稿.md` and the outside-project document `/tmp/Shared Notes/會議記錄.md` existed. `git worktree list --porcelain` reported both project and linked worktree (physical `/private/tmp` aliases point to the same files).
- The parent coordinated three sequential fresh-context native Codex drivers, with only the source guidance path and neutral delivery request; expected answers were not supplied. Driver identities: `/root/cold_code`, `/root/cold_design`, `/root/cold_workflow`. Responses below are exact output relayed by the parent, not answers synthesized by this witness.
- This is a bounded model-response sample. No claim is made about universal compliance across hosts/models, automatic skill routing, new installed cache behavior, or actual UI link opening.

## 1. Loom 對話中提供給使用者的本機文件位置皆為絕對路徑，涵蓋 loom-code、loom-design 與 loom-workflow 的文件交付。

- How I tried it: ran focused tests in the clean clone and requested three cold document-delivery responses, one for each family guidance surface.
- Focused command (no packages installed):

```sh
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q loom-code/tests/test_conversation_document_paths.py loom-code/tests/test_check_skill_crossrefs.py loom-code/tests/test_sync_codex_manifest.py loom-code/tests/test_write_plan_station_text.py loom-design/tests/spec/test_capture_intent_contract.py loom-workflow/tests/scripts/test_release_metadata.py loom-workflow/tests/scripts/test_visualization_card_hook.py
```

- What came back: `171 passed in 0.80s`. This includes all direct design document-delivery entry guidance, emitted code guidance, workflow guidance, portable crossrefs, manifest synchronization, release pins and workflow card hooks. System Python initially lacked pytest; default uv cache writes were denied by the sandbox; the transient locked interpreter suggested by the parent no longer existed. The successful run used an existing non-base environment without installing anything.
- Full package suite was deliberately left to finalization, per the acceptance agent contract. It was not skipped by user instruction and is not claimed as run by this witness. The blocking check is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, recorded in `docs/loom/KICKOFF-DEFAULTS.md`; finalization must execute it and refuse acceptance on failure.
- Guidance paths, each rooted at `/tmp/loom-absolute-acceptance-adad5c7/`:
  - Code: execute and parse `loom-code/hooks/session-start`, use emitted `additionalContext`.
  - Design: `loom-design/skills/capture-intent/references/conversation-paths.md`.
  - Workflow: `loom-workflow/skills/loom-visualization/references/plain-language.md`.
- Neutral request supplied to the parent (same delivery request for all three, only guidance source changes): “Active project /tmp/Delivery Project 專案, linked worktree /tmp/Worktree 分支; deliver existing worktree document docs/設計 草稿.md and outside document /tmp/Shared Notes/會議記錄.md with short labels; also say whether the stored project README link [設計](docs/設計%20草稿.md) and JSON {\"intent\":\"docs/loom/intent/change.md\"} should change. Environment supports local Markdown links.”
- Exact captured Code response:

```markdown
- [設計草稿](</tmp/Worktree 分支/docs/設計 草稿.md>)
- [會議記錄](</tmp/Shared Notes/會議記錄.md>)

README 的 `[設計](docs/設計%20草稿.md)` 和 JSON 的 `{"intent":"docs/loom/intent/change.md"}` 都不用改；它們是文件內的相對連結與儲存路徑。絕對路徑規則只適用於對話中提供的位置。
```

- Exact captured Design response:

```markdown
- [設計草稿](</tmp/Worktree 分支/docs/設計 草稿.md>)
- [會議記錄](</tmp/Shared Notes/會議記錄.md>)

README 的 `[設計](docs/設計%20草稿.md)` 和 JSON 的 `{"intent":"docs/loom/intent/change.md"}` 都不用改。絕對路徑規則只適用於對話中分享的位置；文件連結與儲存的相對路徑維持原樣。
```

- Exact captured Workflow response:

```markdown
可直接開啟這次 worktree 的草稿與外部會議記錄：

- [設計草稿](</tmp/Worktree 分支/docs/設計 草稿.md>)
- [會議記錄](</tmp/Shared Notes/會議記錄.md>)

README 的 `[設計](docs/設計%20草稿.md)` 和 JSON `{"intent":"docs/loom/intent/change.md"}` 都不必改；它們保留相對路徑，方便專案搬移與共用。聊天中的開啟連結才使用絕對路徑。
```

- Result: works in all three observed response samples; broader host/model compliance remains untested.

## 2. 支援本機文件連結的對話環境使用絕對路徑作為連結目標；顯示名稱可保留簡短檔名。

- How I tried it: inspected the exact three responses above against the fixture locations, including spaces and CJK characters.
- What came back: each response used `[設計草稿](</tmp/Worktree 分支/docs/設計 草稿.md>)` and `[會議記錄](</tmp/Shared Notes/會議記錄.md>)`. Both targets are absolute and angle-bracket wrapped; labels contain no directory prefix.
- Evidence: the three captured response blocks in section 1 and the passing `test_emitted_code_guidance_and_direct_visualization_cover_document_paths`.
- Result: works for emitted link syntax. Actual clicking in the host UI was not exercised.

## 3. 在不同專案目錄與 worktree 中交付文件時，路徑均指向該次工作的實際文件位置，不固定使用開發者的電腦路徑。

- How I tried it: delivered from a separate Git project and its linked worktree, both outside the plugin source clone, and requested another document outside both roots.
- What came back: all three responses resolved the design document under `/tmp/Worktree 分支`, rather than `/tmp/Delivery Project 專案` or the plugin clone, and retained `/tmp/Shared Notes/會議記錄.md` for the external document. No `/Users/kouko` development prefix appeared in delivered targets.
- Evidence: captured responses in section 1; `git -C '/tmp/Delivery Project 專案' worktree list --porcelain` reported both fixture roots; Python `Path(...).is_file()` returned `True` for both emitted targets.
- Result: works for these separate-project, linked-worktree and external-document fixtures.

## 4. 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。

- How I tried it: ran the portable cross-reference and capture contract tests, inspected the runtime guidance diff, and checked fixture contents after collecting the responses.
- What came back: focused tests passed; each response explicitly retained the stored README link and JSON reference. The fixture README still read `[設計](docs/設計%20草稿.md)` and parsed JSON remained `{'intent': 'docs/loom/intent/change.md'}`. No fixture was rewritten by the drivers.
- Evidence: `test_check_skill_crossrefs.py`, `test_capture_intent_contract.py`, exact response blocks above, and `python3` reads of the two fixture files. Diff inspection showed new conversation guidance explicitly preserves bundled resource references, stored relative paths and repository document links; the capture skill still resolves relative paths from its own directory and loads `references/conversation-paths.md` relatively.
- Result: works for the checked portable references and stored-data fixtures. Reading the diff is supporting scope evidence; the verdict also rests on executed tests and observed responses.

## Decisions, data and omissions

- Agent-decided choices disclosed in the report come from the committed plan: shared guidance plus standalone design entry coverage; absolute link targets with short labels and a plain-path fallback; minor releases for runtime guidance changes.
- No dismissed finding of severity important or worse was supplied by the station.
- No `skipped-by-instruction` records appear in the intent constraints or plan risks.
- This change modifies plugin instructions, tests and release metadata. It does not migrate or rewrite adopting projects' documents, links or structured relative-path data. Acceptance files are added to the original repository; no production code was edited by this witness.
