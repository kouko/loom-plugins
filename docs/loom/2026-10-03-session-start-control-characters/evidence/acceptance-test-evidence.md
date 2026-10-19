# Session start survives control characters in the repo defaults — acceptance test evidence

Tried on 2026-10-03, in a clean copy of the project at d01d6ddb (detached
`git worktree add` of HEAD; a second clean worktree at base c14e176c for
comparison). Neither worktree was edited.

Setup check: the README's install path is `claude plugin install
loom-code@loom` from the marketplace; installing into the user's real
Claude Code config was not done. Instead `claude plugin validate
<worktree>/loom-code` ran on the clean copy ("Validation passed"), and
`loom-code/hooks/hooks.json` still registers `hooks/session-start` for
SessionStart (`startup|clear|compact`). The hook was then run directly, which
is the command Claude Code runs at session start.

Harness: a scratch script (not committed) creates a fresh `git init` repo per
case, writes the bytes below to `docs/loom/KICKOFF-DEFAULTS.md`, runs
`bash <worktree>/loom-code/hooks/session-start </dev/null` with cwd = that
repo under both `LC_ALL=en_US.UTF-8` and `LC_ALL=C`, and parses stdout with
Python `json.loads(stdout.decode("utf-8"))` (strict: rejects raw control
characters and invalid UTF-8). Results were identical in both locales unless
noted.

## 1. With a form feed or a terminal escape character in a defaults line, the session-start output is valid JSON and still carries the station order and the repository's other defaults lines.
- How I tried it: cases, each with a second line `- standing-docs: waived (2026-09-02)`:
  - form feed: `- review-note: strict\x0cpage two (2026-10-03)`
  - ESC colour code: `- shell-note: \x1b[31mred\x1b[0m pasted (2026-10-03)`
  - ESC between dash and key: `-\x1b second-vendor: suggest (2026-10-03)`
  - BEL / DEL / NUL: `- note-a: x\x07y\x7fz\x00w (2026-10-03)`
  - invalid UTF-8 (Latin-1): `- lang-note: caf\xe9 \x85 pasted (2026-10-03)`
  - CJK plus form feed: `- 語言: 繁體\x0c中文 (2026-10-03)`
- What came back:

  | case | base c14e176c | HEAD d01d6ddb |
  |---|---|---|
  | form feed | exit 0, JSON invalid ("Invalid control character", char 2681) | exit 0, valid; `Station order:` present; defaults `- review-note: strictpage two (2026-10-03)`, `- standing-docs: waived (2026-09-02)` |
  | ESC colour | exit 0, JSON invalid (char 2674) | valid; station order; `- shell-note: [31mred[0m pasted (2026-10-03)` + standing-docs line |
  | ESC before key | valid, but the line was dropped (2728 bytes) | valid; `- second-vendor: suggest (2026-10-03)` kept + standing-docs line |
  | BEL/DEL/NUL | JSON invalid | valid; `- note-a: xyzw (2026-10-03)` + standing-docs line |
  | invalid UTF-8, UTF-8 locale | exit 1, no output at all | exit 0, valid; `- lang-note: caf  pasted (2026-10-03)` + standing-docs line |
  | invalid UTF-8, C locale | exit 0, not decodable as UTF-8 (byte 0xe9) | valid, same as above |
  | CJK + form feed | JSON invalid | valid; `- 語言: 繁體中文 (2026-10-03)` + standing-docs line |

  On HEAD no decoded context contained any character below U+0020 other than
  newline and tab.
- Evidence: captured harness output (scratch `walk.out`); also the graduated
  adversarial test `loom-code/tests/test_adversarial_session_start_c1_byte.py`
  and `loom-code/tests/test_session_start_words.py`, run in item 4.
- Observation: only the ESC byte is removed from a colour code; the visible
  remainder `[31m` / `[0m` stays in the line text. Invalid bytes are dropped,
  so `café` typed in Latin-1 arrives as `caf`.

## 2. With an ordinary defaults file, the session-start output is unchanged.
- How I tried it: same harness, comparing HEAD stdout to base stdout byte for byte.
  - the repository's own `docs/loom/KICKOFF-DEFAULTS.md` (UTF-8, em dashes, backticks)
  - a synthetic three-key file with a tab-indented non-list line
  - CJK only: `- 語言: 繁體中文、日本語 — 理由 (2026-10-03)`
  - no defaults file
  - classic-Mac file with lone CR line endings
  - Windows file with CRLF line endings
- What came back:
  - repo file: 4299 bytes both, byte-identical, 613 words
  - synthetic: 2808 bytes both, byte-identical
  - CJK: 2788 bytes both, byte-identical
  - no file: 2624 bytes both, byte-identical, 401 words
  - lone CR: byte-identical (both show no defaults block, as before)
  - CRLF: NOT identical — base 2771 bytes carried a trailing `\r` (escaped) on
    each defaults line; HEAD 2767 bytes drops those carriage returns. Both
    valid JSON with the same visible text.
- Evidence: captured harness output; `test_session_start_words.py::test_kickoff_defaults_lines_are_injected_when_the_file_exists` passed (item 4).

## 3. The loom-code 3.29.0 CHANGELOG no longer claims that pytest options which run no tests are always refused; it states that such an option passed through a configuration override still gets through.
- How I tried it: read the 3.29.0 first bullet at HEAD, then checked the
  statement against the checker itself in the clean copy:
  `python3 -c 'from loom_checker.probes import pytest_positionals, command_executes_artifact ...'`
  from `loom-code/scripts`.
- What came back: the bullet now reads "an unlisted option passed directly,
  including one that runs no tests (e.g. `--help`, `--collect-only`), is
  refused in any position ... A no-run option injected through a
  configuration override (`-o addopts=--collect-only`) still gets through;
  this is a known limitation." Checker behaviour matches:
  - `pytest_positionals(['--collect-only','t.py'])` -> None (refused)
  - `pytest_positionals(['--help','t.py'])` -> None (refused)
  - `pytest_positionals(['-o','addopts=--collect-only','t.py'])` -> ['t.py'] (accepted)
  - `command_executes_artifact('python3 -m pytest t.py --collect-only','t.py')` -> False
  - `command_executes_artifact('python3 -m pytest -o addopts=--collect-only t.py','t.py')` -> True
- Evidence: `loom-code/CHANGELOG.md` 3.29.0 first bullet; `loom-code/scripts/loom_checker/probes.py:312-347`.

## 4. The existing package test suite passes, and loom-code carries a new version consistent across manifests, CHANGELOG and READMEs.
- How I tried it (clean HEAD worktree):
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project --python /opt/homebrew/bin/python3 --with pytest --with pyyaml python -m pytest -q -p no:cacheprovider loom-code/tests/test_session_start_words.py loom-code/tests/test_adversarial_session_start_c1_byte.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`
  - `python3 scripts/sync_codex_manifests.py --check --all`
  - grep of `"version"` in the four manifests and `3.29.1` in the READMEs
- What came back:
  - `16 passed in 0.57s`
  - sync check exit 0
  - `loom-code/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`: all `3.29.1`
  - root `README.md:17` and `:132`, `loom-code/README.md:11`, `README.ja.md:11`, `README.zh-TW.md:9`: all 3.29.1
  - CHANGELOG top entry `## [3.29.1] — 2026-10-03`
- Full suite: not run by the acceptance tester. The suite command is the
  repo's `package-tests` default:
  `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`;
  finalize-review executes it and refuses the attestation on failure. (The
  orchestrator reported its own run of it at d01d6ddb with exit 0; not
  witnessed here.)

## Re-run on 2026-10-03, at 4dea7292
Fix range 834115b2..4dea7292 (a10e667d: `|| cat` fallback when iconv is
missing or fails, sed under `LC_ALL=C`; 4dea7292: form feed and vertical tab
become spaces, CHANGELOG 3.29.1 bullet reworded). Fresh detached worktrees at
4dea7292 (head), c14e176c (base) and 834115b2 (previous head), none edited.

Setup check: `claude plugin validate <head>/loom-code` -> "Validation passed";
`loom-code/hooks/hooks.json` still registers `hooks/session-start` for
SessionStart (`startup|clear|compact`).

Harness (scratch `walk2.py`, not committed): one fresh `git init` repo per
case, bytes written to `docs/loom/KICKOFF-DEFAULTS.md`, `/bin/bash
<tree>/loom-code/hooks/session-start </dev/null` under `LC_ALL=en_US.UTF-8`
and `LC_ALL=C`, stdout parsed with strict `json.loads(stdout.decode("utf-8"))`.
Every head case was also run with no working iconv, two ways:
- shim127: PATH prefixed with a dir whose `iconv` is `#!/bin/sh` + `exit 127`
  (exits without reading stdin);
- no-iconv: PATH set to a dir of symlinks to every `/usr/bin` and `/bin`
  tool except `iconv` (`command -v iconv` finds nothing).
A first attempt with a hand-picked tool list exited 127 because `paste` was
missing from that PATH; a harness gap, not the hook. Rebuilt as above.

- 1: re-tested — cases, each followed by `- standing-docs: waived (2026-09-02)`:

  | case | base c14e176c | head 4dea7292 (iconv) | head shim127 / no-iconv |
  |---|---|---|---|
  | form feed mid-line `strict\x0cpage two` | exit 0, JSON invalid (col 2682) | valid; station order; `- review-note: strict page two (2026-10-03)` + standing-docs | byte-identical to the iconv run, valid, both locales |
  | vertical tab mid-line | JSON invalid (col 2682) | valid; `- review-note: strict page two (2026-10-03)` + standing-docs | identical, valid |
  | form feed between dash and key `-\x0creview-note:` | valid, line kept | valid, line kept, byte-identical to base (834115b2 dropped this line) | identical, valid |
  | CJK + form feed `繁體\x0c中文` | JSON invalid (col 2669) | valid; `- 語言: 繁體 中文 (2026-10-03)` + standing-docs | identical, valid |
  | ESC colour code | JSON invalid (col 2675) | valid; `- shell-note: [31mred[0m pasted (2026-10-03)` + standing-docs (same bytes as 834115b2) | identical, valid |
  | ESC between dash and key | valid, line dropped | valid; `- second-vendor: suggest (2026-10-03)` kept (same as 834115b2) | identical, valid |
  | BEL / DEL / NUL | JSON invalid | valid; `- note-a: xyzw (2026-10-03)` (same as 834115b2) | identical, valid |
  | invalid UTF-8 `caf\xe9 \x85` | UTF-8 locale: exit 1, no output (`sed: RE error: illegal byte sequence`) | valid; `- lang-note: caf  pasted (2026-10-03)` | exit 0, 2769 bytes, NOT decodable as UTF-8 (0xe9 passes through), both locales |

  No head context (any PATH) contained a character below U+0020 other than
  newline and tab; station order present in every head run. The
  invalid-UTF-8-without-iconv row is outside line 1 (form feed / ESC) and
  matches the CHANGELOG's stated limitation; whether Claude Code accepts that
  output was not tried here.
- 2: re-tested — head vs base, byte for byte, both locales, plus shim127 / no-iconv:
  - repository's own defaults file: 4299 bytes, identical to base; identical under shim127 and no-iconv
  - synthetic three-key file with a tab-indented line: 2808 bytes, identical; same without iconv
  - CJK only: 2788 bytes, identical; same without iconv
  - lone CR endings: 2624 bytes, identical; same without iconv
  - no defaults file: 2624 bytes, identical; same without iconv
  - CRLF endings: not identical, as in the first run (base 2771 bytes with an
    escaped `\r` per defaults line, head 2767 without); same visible text, both valid
- 3: re-tested — the 3.29.0 first bullet is untouched by the fix (the diff
  changes only the 3.29.1 first bullet) and still reads "... A no-run option
  injected through a configuration override (`-o addopts=--collect-only`)
  still gets through; this is a known limitation." Checker re-run from
  `<head>/loom-code/scripts`:
  `pytest_positionals(['--collect-only','t.py'])` -> None,
  `(['--help','t.py'])` -> None, `(['-o','addopts=--collect-only','t.py'])` -> ['t.py'];
  `command_executes_artifact('python3 -m pytest t.py --collect-only','t.py')` -> False,
  `('python3 -m pytest -o addopts=--collect-only t.py','t.py')` -> True.
  The reworded 3.29.1 bullet was checked against the runs above: form feed and
  vertical tab become spaces, other control characters removed, invalid bytes
  dropped with iconv and passed through without it, and a missing or failing
  iconv no longer silences the hook (exit 0 in every shim127 / no-iconv run):
  all confirmed.
- 4: re-tested — the fix touched a test file, so the criterion's tests were re-run:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project --python /opt/homebrew/bin/python3 --with pytest --with pyyaml python -m pytest -q -p no:cacheprovider loom-code/tests/test_session_start_words.py loom-code/tests/test_adversarial_session_start_c1_byte.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`
  -> `17 passed in 0.88s` (one more than the first run: the new failing-iconv test).
  `scripts/sync_codex_manifests.py --check --all` exit 0. Versions:
  `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`,
  `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json` all 3.29.1;
  `README.md:17`, `README.md:132`, `loom-code/README.md`, `loom-code/README.ja.md`,
  `loom-code/README.zh-TW.md` carry 3.29.1; no manifest or README changed in the
  fix range. (Correction to the first run: those manifests and the ja / zh-TW
  READMEs live under `loom-code/`.) Full suite not run by the acceptance
  tester; `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  is executed by finalize-review, which refuses the attestation on failure.
  (Orchestrator reported its own run at 4dea7292 with exit 0; not witnessed here.)
