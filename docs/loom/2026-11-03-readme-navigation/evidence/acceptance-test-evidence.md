# Linked skill documentation — acceptance test evidence

Tried on 2026-11-03, in a clean copy of the project at 47f24eac.

## Environment and setup

- Witness: the independently dispatched acceptance tester; did not implement this change.
- Clean clone: `/tmp/loom-readme-acceptance-20261103`.
- Command: `git -C /tmp/loom-readme-acceptance-20261103 rev-parse HEAD`.
- Initial captured output: `972d71c860f427fe1402345b39bdde5b28eb7e27`. Final tested HEAD: `47f24eac99b2e7a6a9bd4e4f548a7c791daf79a7`; see the re-run section below.
- Command: `git -C /tmp/loom-readme-acceptance-20261103 status --porcelain`, both before and after the checks.
- Captured output: empty, exit 0. No implementation, test or guide was changed by the witness.
- Opened the root README and the English, Japanese and Traditional Chinese plugin READMEs directly from the clean clone. This documentation-only change needs no build to read its guides. No host plugin was installed or updated; runtime loading is not claimed.
- Followed the root README's isolated locked environment setup, scoped to the two navigation modules rather than the full suite:
  `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest tests/test_readme_navigation.py tests/test_readme_navigation_adversarial.py -q`.
  Initial sandboxed result: `Could not acquire lock ... Operation not permitted` in the default uv cache. Retried with `UV_CACHE_DIR=/tmp/loom-readme-acceptance-uv`; dependency retrieval failed on PyPI DNS after three retries. System `python3 -m pytest ...` returned `No module named pytest`. These sandbox limitations did not establish a host setup failure. Re-ran the locked command with approved escalation and the absolute original-checkout lockfile path; captured result at 972d71c8: `17 passed in 0.54s`. Final targeted re-run at 47f24eac is recorded below. Independent standard-library navigation and branch probes below also ran successfully.
- The full package suite was not run. It is not skipped; closing-review finalization will execute it and block acceptance on failure. Its command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- No important-or-worse dismissed findings were supplied. Neither intent Constraints nor plan Risks records a `skipped-by-instruction:` line.

## 1. 所有目前的 27 個 skill 都有給使用者閱讀的 README，說明用途、使用方式、產出與限制。

- How I tried it: enumerated `*/skills/*/SKILL.md` for the three plugins, opened every neighboring English README, and read each guide's purpose, invocation guidance, results and boundaries. Checked actual explanation, not only heading names. Existing long-form guides use sections such as Invocation, How it works and Honest framing instead of the newer guide's four common headings.
- Supplementary executable check: a Python standard-library loop required a README longer than 500 characters for every discovered skill and searched for invocation, output and boundary language. This smoke check supplements the direct reading; keyword matches alone are not a content verdict.
- Captured inventory: loom-code 7; loom-design 6; loom-workflow 14; total 27, all with usable English guides. Newly structured guides are 36–44 lines; existing longer guides range up to 158 lines.
- Read evidence: `loom-code/skills/*/README.md`, `loom-design/skills/*/README.md`, `loom-workflow/skills/*/README.md` in the tested clone. All 27 were opened; independent-advisor was reopened individually after combined output truncation.
- Result: works. No missing purpose, use, result or limitation found.

## 2. 專案 README 的 plugin 與 skill 清單，以及各 plugin 的 skill 清單，都直接連到對應的 README。

- How I tried it: independently extracted visible Markdown links, excluding comments and fenced examples. For each discovered skill, walked from the root README to its English guide, and from all three language variants of its plugin catalog to a README in the same skill directory. Verified the root's direct plugin README routes too.
- Localized fallback check: for each plugin and each of `ja` and `zh-TW`, selected `README.<language>.md` when present and `README.md` otherwise, then required exactly that destination to appear in the catalog's actual links. All 54 per-skill localized choices passed.
- Captured output:

```text
FALLBACK loom-code ja localized 0 English 7
FALLBACK loom-code zh-TW localized 0 English 7
FALLBACK loom-design ja localized 0 English 6
FALLBACK loom-design zh-TW localized 0 English 6
FALLBACK loom-workflow ja localized 6 English 8
FALLBACK loom-workflow zh-TW localized 6 English 8
PASS 27 usable English guides; 54 localized catalog choices
PASS all 27 English guides reachable from project and all localized plugin catalogs
```

- All localized plugin READMEs explicitly explain that untranslated guides open in English.
- Result: works for the committed navigation. No live HTTP request or GitHub click-through was performed; not-yet-merged canonical `blob/main` destinations were resolved to the exact tested clone.

## 3. 各 skill README 能返回專案與 plugin，並連到相關技能與自身執行規則；導覽中的本機相對連結都有有效目的地。

- How I tried it: independently walked visible links from the root, all nine plugin READMEs and all 39 skill README variants. Percent-decoded link destinations, removed fragments and resolved relative paths from the containing file. Canonical `https://github.com/kouko/loom-plugins/blob/main/` paths were resolved from the clean clone root. Every resulting destination had to exist.
- For each skill guide, independently required destinations for the project README, its plugin README, its own SKILL.md and at least one different skill's README. This also checked related-skill links beyond the existing navigation test's backlink assertions.
- Captured output:

```text
PASS 518 navigation destinations opened;
PASS 81 canonical GitHub links resolved against tested clone;
PASS 39 skill guides include project/plugin/runtime/related-skill routes;
PASS all 27 English guides reachable from project and all localized plugin catalogs
```

- Counts include repeated destinations across pages; they are link visits, not unique files.
- Fragment anchors were excluded from filesystem destination checks; this does not claim full external-link health. Cross-plugin public links were evaluated for their intended repository file, not current online publication.
- Result: works.

## 4. 主要流程與工具清單分開；三語圖保留需要設計、審查退回、探索與交付的正確條件。

- How I tried it: read the root flow and all nine plugin flow/tool sections. Main change flow and on-demand tool catalogs are separate. Compared the English, Japanese and Traditional Chinese decision labels and accompanying prose, then ran an independent graph-edge assertion for all nine plugin diagrams.
- Verified branch cases:
  - loom-code: intent → design decision; design yes → spec → plan; design no → plan; plan → build → review; review needs changes → build; checks pass → ship. The prose keeps merge separate and explicitly authorized. Product behavior confirmation is distinguished from engineering work.
  - loom-design: design yes/no branches remain; required pre-build review is a second decision after spec; review success reaches plan. Standing principles, visual-system and architecture tools remain separate.
  - loom-workflow: unresolved/not-ready slices loop back to fog; ready slices write an intent requiring loom-code, then hand off to capture-intent or write-plan. Prose distinguishes grilling handoff and complete-map completion from one delivered slice.
- Captured output: all nine plugin branch graphs matched their expected edge sets. An initial witness-only regex missed the first edge when its source had an inline label; correcting the extraction to strip node labels made all nine pass. This was a probe defect, with no artifact modification.
- Command: `node /Users/kouko/GitHub/loom-plugins/loom-workflow/tests/mermaid/validate_mermaid.mjs /tmp/loom-readme-acceptance-20261103/README.md /tmp/loom-readme-acceptance-20261103/loom-code/README.md /tmp/loom-readme-acceptance-20261103/loom-code/README.ja.md /tmp/loom-readme-acceptance-20261103/loom-code/README.zh-TW.md /tmp/loom-readme-acceptance-20261103/loom-design/README.md /tmp/loom-readme-acceptance-20261103/loom-design/README.ja.md /tmp/loom-readme-acceptance-20261103/loom-design/README.zh-TW.md /tmp/loom-readme-acceptance-20261103/loom-workflow/README.md /tmp/loom-readme-acceptance-20261103/loom-workflow/README.ja.md /tmp/loom-readme-acceptance-20261103/loom-workflow/README.zh-TW.md`.
- The original checkout supplied only the existing parser and installed Node dependencies; every input README was the absolute path in the clean clone. The parser's built-in negative control rejected a known-invalid diagram before checking these inputs. No global dependency was installed.
- Captured output:

```text
OK /tmp/loom-readme-acceptance-20261103/README.md:30
OK /tmp/loom-readme-acceptance-20261103/loom-code/README.md:23
OK /tmp/loom-readme-acceptance-20261103/loom-code/README.ja.md:23
OK /tmp/loom-readme-acceptance-20261103/loom-code/README.zh-TW.md:21
OK /tmp/loom-readme-acceptance-20261103/loom-design/README.md:22
OK /tmp/loom-readme-acceptance-20261103/loom-design/README.ja.md:22
OK /tmp/loom-readme-acceptance-20261103/loom-design/README.zh-TW.md:21
OK /tmp/loom-readme-acceptance-20261103/loom-workflow/README.md:71
OK /tmp/loom-readme-acceptance-20261103/loom-workflow/README.ja.md:72
OK /tmp/loom-readme-acceptance-20261103/loom-workflow/README.zh-TW.md:66
10/10 mermaid blocks parsed
```

- Result: works for separation, syntax and branch meaning. No independent visual render, narrow-screen layout, live HTTP or GitHub renderer check occurred. Earlier writer-observed Safari/Mermaid 11.17.0 rendering is not this witness's independent observation.

## Re-run on 2026-11-03, at 47f24eac

- Commands: `git fetch origin`, `git checkout --detach 47f24eac`, `git rev-parse HEAD`, `git status --porcelain`, `git diff 972d71c8..HEAD --stat`, and `git diff 972d71c8..HEAD -- loom-design/tests/architecture-design/test_architecture_skill.py`, all in the clean clone.
- Captured HEAD: `47f24eac99b2e7a6a9bd4e4f548a7c791daf79a7`. Status output: empty. Diff: exactly one test file, one line replaced; the catalog assertion now requires `skills/architecture-design/README.md` instead of `skills/architecture-design/SKILL.md`. No guide, catalog, destination or diagram changed.
- 1: carried over — the sole test-assertion fix cannot change the inventory or any guide's purpose, invocation, outputs or boundaries; diff confirmed no documentation changes. Inventory checks also ran again through the targeted tests.
- 2: re-tested — all project and plugin catalogs, including every language variant, were exercised again, together with the changed architecture catalog assertion. Independently repeated the full language preference loop at final HEAD: `PASS 54 localized catalog choices at final HEAD`.
- 3: carried over — no link text, destination file or guide changed in the one-line test-only fix. Backlink and missing-destination tests additionally ran again.
- 4: carried over — no diagram or explanation changed; the prior independent parser and branch-meaning evidence remains applicable byte-for-byte.
- Final command (approved escalation; same locked environment as project setup, targeted modules only): `uv run --isolated --with-requirements /Users/kouko/GitHub/loom-plugins/requirements-package-tests.lock python -m pytest tests/test_readme_navigation.py tests/test_readme_navigation_adversarial.py loom-design/tests/architecture-design/test_architecture_skill.py -q`.
- Captured output:

```text
.........................                                                [100%]
25 passed in 0.46s
```

- No acceptance failure or new finding was observed. The full package suite remains the finalizer's separate blocking check; it was never run by this witness.
