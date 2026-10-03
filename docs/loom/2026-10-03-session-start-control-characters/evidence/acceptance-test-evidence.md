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
