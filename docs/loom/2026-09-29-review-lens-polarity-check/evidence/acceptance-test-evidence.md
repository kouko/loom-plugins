# LLM reviewer compares rule direction against the base — acceptance test evidence

Tried on 2026-09-29, in a clean copy of the project at 2846730c (a fresh
`git clone` of the local repository, checked out at
2846730c899936620545aef8cfd775ec88dbfacf; base origin/main 10df847c).

## Setup check (clean copy)

- How I tried it: followed the README "Install" section, pointed at the
  clean clone instead of GitHub (GitHub `main` does not carry this branch),
  in a throwaway config directory:
  `CLAUDE_CONFIG_DIR=<scratch>/cfg claude plugin marketplace add <clone>`,
  then `claude plugin install loom-code@loom`, `loom-design@loom`,
  `loom-workflow@loom`, then `claude plugin list`. Also
  `claude plugin validate` on each plugin and on the marketplace root.
- What came back: marketplace `loom` added; all three installed and
  enabled at 3.22.4 / 2.6.3 / 5.5.4. The installed copy
  `plugins/cache/loom/loom-code/3.22.4/skills/closing-review/references/lenses.md`
  contains the new paragraph (line 74, "**Polarity against the base.**").
  `claude plugin validate`: all pass; the warnings (unknown field
  `requires-contract`, an unquoted `${CLAUDE_PLUGIN_ROOT}` in a hook) sit
  on manifest fields this change did not touch — only the `version` line
  of each manifest changed.
- Evidence: the command output above; `git diff origin/main..HEAD --stat`
  shows each manifest at `1 insertion, 1 deletion`.

## 1. closing review 的 skill 與 docs 審查規範寫明：diff 刪掉或改寫帶方向字眼的句子時，reviewer 要對照舊版逐句比對，方向被反轉或刪掉即為發現。

- How I tried it: read `git diff origin/main..HEAD -- loom-code/skills/closing-review/references/lenses.md`
  and the surrounding sections at HEAD; read `loom-code/agents/reviewer.md`
  "What each lens scores" table.
- What came back: `lenses.md:74-83` adds one paragraph under the Docs
  table: when the diff deletes or rewrites a sentence carrying a polarity
  word (never, must not, only, always, 不得; kin: no, do not, may not,
  forbid, 禁止, 絕不), read the base with `git show <base>:<path>`, compare
  each such sentence with its new form; a reversed direction or a polarity
  clause dropped with nothing else carrying it is an `inconsistency`
  finding; a rewording that keeps direction is not. It states it applies
  "in the docs lens and so in the skill lens that scores these five
  dimensions". `reviewer.md` table row `skill` = "the five `docs`
  dimensions, plus user-judgment-leak, deletion-first", so the skill lens
  inherits it. In the trial (row 2) both reviewers given `lens: skill`
  applied it.
- Evidence: `loom-code/skills/closing-review/references/lenses.md:74-83`;
  `loom-code/agents/reviewer.md` lens table (`skill` row).

## 2. 一位沒看過這個變更的 reviewer 拿到一份 diff，其中在大量無關改動裡藏了一句被寫反的規則，會照規範把它報出來；拿到一份只換說法、方向不變的 diff，不會報方向問題。

- How I tried it: built two scratch git repos outside the project
  (`trial-a`, `trial-b`) for a fictional "shelf-tools" publish skill:
  README, `skills/publish/SKILL.md`, `skills/publish/references/checklist.md`,
  `docs/guide.zh-TW.md`, plus a neutral `docs/intent.md` (add Requirements
  and Troubleshooting, state CLI 2.3 minimum, output example; out of scope:
  new skills — it does not mention the planted sentence). Both repos share
  the base commit `a66df542`; each change commit touches 5 files, 73
  insertions / 22 deletions. The two diffs are identical except one line.
  - Unrelated edits in both: new README Requirements / Troubleshooting /
    Contributing text; reworded SKILL description and intro; step 2
    expanded; step 6 "only after the upload succeeds" -> "Once the upload
    has succeeded, and not before"; rule "Do not print the registry token"
    -> "Keep the registry token out of every log line"; "Never delete a
    version" -> "Registry versions are permanent: never delete one"; new
    CLI-version rule; output example; checklist reordered and reworded;
    guide intro, prerequisites, FAQ token answer "絕不寫進設定檔" ->
    "不要寫進設定檔，也不要提交到版本庫", new FAQ item.
  - trial-a (planted flip, Chinese): `docs/guide.zh-TW.md:9`
    base `發布前不得略過簽章驗證。` -> `若時間緊迫，發布前可以略過簽章驗證，事後再補做。`
  - trial-b (reword only): same line -> `簽章驗證是發布前的必要步驟，任何情況下都不能略過。`
  Dispatched four fresh general-purpose agents, two per repo (one
  `lens: skill`, one `lens: docs`), each given only copies of HEAD's
  `lenses.md` and `reviewer.md` (sha-checked identical to
  `git show HEAD:<path>`), the repo path, `reviewed_sha: a66df542...`, the
  changed paths and the intent as ground truth. The prompts did not
  mention polarity, the planted line, or that anything was planted; the
  staging files were moved out of the scratch tree first.
- What came back:

  | Run | Diff | Lens | Planted/reworded line | Verdict |
  |---|---|---|---|---|
  | a1 | trial-a | skill | flagged `fatal` `inconsistency` at `docs/guide.zh-TW.md:9`, citing `git show a66df54:docs/guide.zh-TW.md` and "polarity is reversed against the base" | NEEDS_REVISION |
  | a2 | trial-a | docs | flagged `fatal` `inconsistency`: "the forbid became an allow", fix = restore base sentence | NEEDS_REVISION |
  | b1 | trial-b | skill | no polarity finding; note: compared every rewritten polarity sentence with `git show a66df54:<path>`, 不得略過 kept as 任何情況下都不能略過, none reversed or dropped | PASS_WITH_NOTES |
  | b2 | trial-b | docs | no polarity finding; note lists the five polarity sentences checked against base, all keep direction | PASS_WITH_NOTES |

  In trial-a both reviewers also listed the English decoy rewordings
  (token, never-delete, only-after-upload, must-not-tick) as checked and
  direction-kept — no false positive on them. All four also raised the
  same unplanted defect of my fixture (the checklist is read "before step
  3" but its signature item can only be ticked by step 3) and small nits;
  none of those is a polarity finding.
- Limits: 2 samples per diff, so this is an observation, not a rate —
  reviewer behaviour is probabilistic. The planted flip also contradicted
  unchanged text (SKILL step 3, checklist item), which the pre-existing
  changed-against-unchanged `inconsistency` rule could catch on its own;
  a flip with no contradicting text elsewhere was not tried. No control run
  with the base lenses.md was made, so the trial does not measure how much
  the new paragraph adds; what it shows is that reviewers followed the
  paragraph (the notes cite `git show <base>:<path>` per polarity
  sentence) and got both cases right.
- Evidence: scratch repos under the session scratchpad (`trials/trial-a`
  head `32e09974`, `trials/trial-b` head `afeae78e`), reviewer outputs
  quoted above.

## 3. 這條檢查不依賴任何逐條列出的規則或 skill 清單。

- How I tried it: read `lenses.md:74-83` for any enumerated rule, skill
  name or file path; checked the trigger.
- What came back: the trigger is a polarity word in a deleted or rewritten
  sentence; the words are examples ("and their kin"). The only path-like
  token is the placeholder `git show <base>:<path>`. No rule, skill or file
  is named. The trial repo was not a loom repo and its rules appear in no
  list anywhere, and reviewers still applied the check (row 2), including
  to a Chinese word (`不得`) and to 絕不 -> 不要.
- Evidence: `loom-code/skills/closing-review/references/lenses.md:74-83`.

## 4. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

- How I tried it (in the clean clone):
  - read `version` from `plugin.json`, `.claude-plugin/plugin.json`,
    `.codex-plugin/plugin.json` of each plugin; top `## [` heading of each
    CHANGELOG; version strings in root README and each plugin's three
    READMEs; grep for leftover `3.22.3` / `"2.6.2"` / `5.5.3` in json and
    README files.
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized loom-design/tests/spec/test_capture_intent_contract.py::test_loom_design_version_2_2_0_consistent loom-workflow/tests/scripts/test_release_metadata.py -p no:cacheprovider`
  - `python3 scripts/sync_codex_manifests.py --all --check`
  - full suite: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- What came back: loom-code 3.22.4, loom-design 2.6.3, loom-workflow 5.5.4
  in all 9 manifests; CHANGELOG tops `## [3.22.4]`, `## [2.6.3]`,
  `## [5.5.4]`; root README table and "Version X" lines and all nine plugin
  README version strings match; no leftover old version. Pin tests:
  `11 passed`. Sync check: exit 0. Full suite: exit 0, no FAIL lines; the
  largest pytest block `2047 passed, 2 skipped`, other blocks 188, 53, 260,
  121, 64, 22, 13, 1, 71, 201, 12, 155 passed (skips 1+3+5), shell checks
  all PASS.
- Evidence: command outputs above; `finalize-review` runs the same suite
  again before the change is accepted and blocks on failure.
