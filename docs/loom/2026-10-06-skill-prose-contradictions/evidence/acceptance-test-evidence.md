# Fix four contradicting rules in write-plan and closing-review prose — acceptance test evidence

Tried on 2026-10-07, in a clean copy of the project at cdde0ea2
(`git worktree add --detach <scratch>/at-wt cdde0ea2`; branch base main a27baaf9).

## Setup

- How I tried it: followed the README's Claude Code install section as far as
  a clean copy allows without touching the user's installed plugins —
  `claude plugin validate .`, `claude plugin validate ./loom-code`,
  `claude plugin validate ./loom-design`; ran the SessionStart hook as a host
  would: `bash loom-code/hooks/session-start </dev/null`.
- What came back: every validate prints `Validation passed with warnings`; the
  only warning is `requires-contract: Unknown field`, present at the branch
  base too (a27baaf9 `loom-design/.claude-plugin/plugin.json` already carries
  `"requires-contract": ">=2.1"`). The hook emits valid JSON whose ① / ② lines
  are quoted under row 1.
- Not tried: a real `claude plugin install` / `codex plugin add` from the
  marketplace, which would replace the user's own installed copy.

## 1. ① 的訊息說明與 one-way door 規則一致：product 改動的無法回頭選擇在 ② 問，engineering 的在 ① 問；loom-code 與 loom-design 兩邊說法相同。

- How I tried it: read every surface that states where one-way doors are asked,
  at HEAD, and the diff `git diff a27baaf9 cdde0ea2`.
- What came back:
  - `loom-code/skills/write-plan/references/one-way-door.md:44-46` merge gate:
    "① for engineering, ② for product where its spec is written, ① for product
    when no spec will be written."
  - `loom-code/skills/write-plan/references/confirm-intent.md:28-37` item 2:
    "The engineering one-way doors found so far … A product change's one-way
    doors, class (e) actions included, are asked at decision point ② of the
    station writing its spec … They are asked in this message instead when no
    spec will be written."
  - `loom-design/skills/capture-intent/SKILL.md:42-54` (decision-point list) and
    `:197-202`, `:215-217` (item 2 and merge gate): same split, same wording as
    confirm-intent.md, naming `write-spec` or `loom-code:write-plan`.
  - `loom-code/skills/write-plan/SKILL.md:89-93`: "At ①, restate the intent;
    merge one-way doors ② skips … At ②, only for a product spec you write:
    confirm visible behaviour, carried details, product one-way doors."
  - `loom-design/skills/write-spec/SKILL.md:178` asks "The one-way doors of this
    change" at ② (unchanged, consistent).
  - `loom-code/hooks/session-start` output: "① … (engineering changes, or
    product changes with no spec) any one-way-door choice …" / "② … product
    one-way-door choices and irreversible actions on existing data are asked
    here, not in ①, when a spec is written".
  - `loom-code/contract/manifest.yaml:40` restate-and-confirm summary,
    `AGENTS.md:123`, `loom-code/README{,.ja,.zh-TW}.md`,
    `loom-design/README{,.ja,.zh-TW}.md`: all carry the same split including the
    "no spec → ①" fallback.
- Criterion tests run (clean copy):
  `uv run … python -m pytest -q loom-code/tests/test_adversarial_product_one_way_door_without_spec.py loom-code/tests/test_adversarial_decision_point_one_restatements.py loom-code/tests/test_adversarial_graduated_probe_classification.py loom-code/tests/test_write_plan_station_text.py loom-design/tests/spec/test_capture_intent_contract.py`
  → `61 passed in 0.15s`.
- Residual (nit, not one of the four): `write-plan/SKILL.md:290-297` — the ②
  gate paragraph for a spec write-plan writes lists "the Requirements and the UI
  flows … and nothing from `## Design decision` down, ever", without naming the
  product one-way doors that `SKILL.md:92` and `confirm-intent.md:30-32` route
  to "this station (step 4)". The recheck detector raised the same tension as
  low-confidence wp finding 8. A literal reader of step 4 alone could skip them;
  the overview list at `SKILL.md:92` says to ask them.

## 2. 所有提到 Codex 授權停頓的地方，都說它在 plugin 新裝或更新時出現，不再說是每個 repo 第一次使用時。

- How I tried it: `grep -rn -i -E "first time (this|a) repo|first-use|first use|per[- ]repo|each repo|every repo|repo is (first )?used|authoris|authoriz|授權|認可|承認"`
  over `loom-code loom-design loom-workflow AGENTS.md README.md CLAUDE.md`
  (CHANGELOGs, tests and `docs/loom/` excluded); also read every README's Codex
  section and `codex-first-contact.md`.
- What came back: the only two mentions of the stop are
  `loom-code/skills/write-plan/SKILL.md:85-87` "one non-decision authorisation
  stop, when the plugin is installed or updated (step 0b)" and
  `loom-design/skills/capture-intent/SKILL.md:59-61` "one authorisation stop
  when the plugin is newly installed or updated." Every other hit is unrelated
  (per-repo setup in an old spec, "authorization" in ship/closing-review error
  text). `codex-first-contact.md:11-18` keys the trust to the installed plugin,
  matching. No README describes a per-repository prompt.

## 3. adversary 的規則清楚區分攻擊時試跑的案例與最後提交的程式，兩份文件不再互相衝突。

- How I tried it: read `loom-code/skills/closing-review/references/adversarial.md`
  §Two parts, `adversarial-code.md` opening, and `loom-code/agents/adversary.md`
  §The order you run in.
- What came back:
  - `adversarial.md:39-45`: "it commits no new program: it may write and run
    trial cases to make its attacks, but leaves them uncommitted … a program is
    written and committed under `docs/loom/<change-id>/evidence/probes/`".
  - `adversarial-code.md:13-17`: "write executable abuse or boundary cases …
    as uncommitted trial cases, run them, and record each one. Only a case whose
    attack succeeded (red) is committed … per the two parts in adversarial.md".
  - `agents/adversary.md:40-54`: "the first part commits no new program" / part 2
    commits one RED program per successful attack. Consistent with both.
  - Recheck: original cr-1 absent from the scc2 cr report.

## 4. reviewer 的規則對已轉正進測試資料夾的 probe 只給一種指示：當作改過的測試檔照跑。

- How I tried it: read `loom-code/skills/closing-review/references/lenses.md`
  round rule and `tests` lens row; grepped `agents/reviewer.md`,
  `closing-review/SKILL.md`, `adversarial.md` for "adversarial program",
  "probes/", "graduat".
- What came back:
  - `lenses.md:35-41`: reviewers never run "the adversarial programs still
    under `docs/loom/<change-id>/evidence/probes/` … A probe graduated out of
    `evidence/probes/` into the repository's tests … is also an ordinary changed
    test file, which reviewers run."
  - `lenses.md:58` `tests` row: "except the adversarial programs still under
    `…/evidence/probes/` (a probe graduated into the repository's tests is a
    changed test file the reviewer runs)".
  - `agents/reviewer.md` defers test-file selection to lenses.md; no competing
    instruction found. `adversarial.md:150-157` names the graduated home
    `loom-code/tests/…`, matching.
  - Recheck: original cr-2 absent from the scc2 cr report.

## 5. 對這幾個 skill 重跑一致性檢查時，上述四點不再被列為矛盾；完整 package suite 通過，loom-code 與 loom-design 的版號字串與 CHANGELOG 新區段一致。

- Consistency recheck (run by the station on cdde0ea2, 4 fresh Sonnet
  detectors): read `<scratchpad>/scc2/wp/consistency-report.md` and
  `<scratchpad>/scc2/cr/consistency-report.md`, compared with the originals in
  `<scratchpad>/scc/{wp,cr}/consistency-report.md`.
  - Original wp-1 (product one-way doors ② vs ①) and wp-2 (Codex stop per repo):
    absent from scc2/wp; verdict pass, 0 high-confidence.
  - Original cr-1 (attack part trial cases) and cr-2 (graduated probe run vs not
    run): absent from scc2/cr; verdict pass, 0 high-confidence.
  - Remaining advisory items are other topics. scc2/wp #8 (product one-way doors
    at ② vs "nothing from Design decision down") touches the same area as the
    fix — see row 1 residual. scc2/cr #2 (a reused existing test named as the
    program vs "a program that caught none is deleted") is outside the four.
  - capture-intent (loom-design) was not in the recheck; verified by reading,
    rows 1 and 2.
- Package suite (clean copy):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  → exit 0 in 2:05.60; 13 pytest runs totalling 3083 passed, 11 skipped,
  0 failed (largest: `1920 passed, 2 skipped in 69.44s`); every shell-script
  check prints `Summary: N PASS / 0 FAIL`; mermaid check `11/11 mermaid blocks
  parsed`. `finalize-review` runs this suite again before the change is accepted
  and blocks it on failure.
- Versions: `loom-code/{.claude-plugin/plugin.json,.codex-plugin/plugin.json,package.json,plugin.json}`
  all `"version": "3.37.0"`; `loom-design/{…same four…}` all `"version": "2.13.0"`;
  `README.md:16-17,117,132` and each plugin README (en/ja/zh-TW) show 3.37.0 /
  2.13.0; `grep -rn "3\.36\.0\|2\.12\.1"` outside CHANGELOGs and `docs/loom/`
  finds only an unrelated npm lockfile entry (d3-array 2.12.1).
  `loom-code/CHANGELOG.md` top section `[3.37.0] — 2026-10-06` and
  `loom-design/CHANGELOG.md` top section `[2.13.0] — 2026-10-06` describe the
  four fixes (loom-design: the first two, which are the only ones touching it).
