# Kickoff Defaults

> Minted from loom-code's contract package. From that moment it is
> THIS repo's own file — it never syncs back to the plugin; edit it
> freely.

<!-- One line per key, grammar `- <key>: <value> — <reason> (<date>)`.
Keys are declared in the `kickoff_defaults` list of loom-code's contract
manifest; loom-code's checker reads this file. Absent key = default. -->

- second-vendor: suggest — report another available model vendor without blocking; provider use remains opt-in (<date>)
- package-tests: <command> — the command a checkpoint's package-test probe must record; `none — <why>` when this repo has no suite (<date>)
- standing-docs: waived — <why> (<date>)          # silences the three-line WARN only; never the product PRINCIPLES rejection
- session-start-baseline: <sha> <words> — measured by running loom-code's `hooks/session-start` script with `</dev/null` and counting words with `python3 -c 'import sys;print(len(sys.stdin.read().split()))'` in an empty git repo (Python str.split — wc disagrees between macOS and GNU) (<date>)
- interface-surfaces: **/cli/**, **/api/**, **/commands/**, **/*.tsx, **/templates/** — <why> (<date>)   # this is the default; edit to match the repo
- artifact-types: <glob>=<type> — <why> (<date>)
