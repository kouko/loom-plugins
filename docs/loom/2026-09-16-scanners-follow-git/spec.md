# Loom asks git which files belong to the repository it is running in — spec
intent: 2026-09-16-scanners-follow-git@87b51761
pre-build-review: not-required — engineering change to file enumeration; no security, privacy, irreversible data, or promised public contract, and Out of scope records that the module is not documented or stabilised for callers outside loom's own gates

## Requirements
REQ-1 — Checker ignores a nested worktree in an adopting repository
  WHEN the loom checker runs in a repository that contains a git linked
  worktree inside its directory at a path that repository's git ignores, the
  checker shall take no file inside that worktree into account, using only
  files installed with the loom-code plugin. Where the worktree's path is not
  ignored, the pre-existing clean-tree check stops finalization; that is a
  stated exception this change does not alter → Acceptance #1

REQ-2 — This repository's scanners ignore a nested worktree
  WHEN a git linked worktree exists inside this repository's directory, each
  of the six scanners named in the intent's Constraints shall pass and report
  no finding anchored inside that worktree → Acceptance #2

REQ-3 — Package tests ignore a nested worktree
  WHEN a git linked worktree exists inside this repository's directory, the
  package-test command shall collect no test file from inside it → Acceptance #3

REQ-4 — Scanners still run without git
  WHEN the same commit is extracted with `git archive` into a copy that has no
  `.git`, each of the five archive-capable scanners named in the intent's
  Constraints shall run and reach the verdict it reaches in the git checkout.
  `loom-code/scripts/rehearse_probes.py` is the stated exception: it works by
  cloning the repository, so it cannot run without git, and in that copy it
  shall report an explicit skip naming that reason and exit zero instead of
  failing → Acceptance #4

REQ-5 — Untracked but not ignored files are still seen
  WHEN a violating file is present that git does not track and `.gitignore`
  does not exclude, the scanner whose rule it violates shall report it
  → Acceptance #5

REQ-6 — Ignored directories produce no findings
  WHEN a directory is excluded by `.gitignore`, no finding from those six
  scanners shall be anchored inside it → Acceptance #6

## Design decision
- agent-decided: one shipped module `loom-code/scripts/repo_files.py`, a
  top-level sibling of `git_exec.py`. `loom_checker/*.py` already reaches
  `git_exec` by bare sibling import (`loom_checker/helpers.py:6`), so the same
  import works from inside the package and from the plugin as installed.
- user-decided: the module lives in loom-code's shipped tree rather than this
  repository's `scripts/`, because the mechanism is for loom itself and must
  work in repositories that adopt loom; this repository's own checks are one
  consumer among them.
- agent-decided: enumeration is `git ls-files --cached --others
  --exclude-standard -z` run with `-C <root>`, so a root that is a
  subdirectory scopes the listing naturally — `check_plugin_boundaries.py` and
  `test_state_anchor_carrier_inventory.py` both scan a subtree, not the
  repository root. `-z` is mandatory: without it a filename containing a
  newline is emitted shell-quoted (https://git-scm.com/docs/git-config,
  core.quotePath).
- agent-decided: the module drops every listed entry that is not an existing
  regular file. `--others` emits a nested repository or linked worktree as one
  opaque directory entry such as `wt/` rather than its files, and `--cached`
  still lists a staged-but-deleted path. Both would reach a caller that expects
  a readable file. That directory entry is also the mechanism by which the
  worktree's contents stay out of the listing, so it is dropped, not expanded.
- agent-decided: submodule contents are not listed, because
  `--recurse-submodules` is documented as incompatible with `--others`
  (https://git-scm.com/docs/git-ls-files). This repository already recorded the
  same limitation at
  `loom-workflow/skills/loom-memory/scripts/test_skill_contract.py:253`. No
  consumer in scope scans a submodule.
- agent-decided: git absence is detected in two questions, in order:
  `git rev-parse --is-bare-repository` FIRST, because a bare repository is git
  yet owns no work tree and so owns no files; only then
  `git rev-parse --show-toplevel` returning nothing through `git_exec.run_git`,
  which already yields `None` on a non-zero exit (`git_exec.py:83`). No separate
  `.git` existence probe. Asking `--show-toplevel` alone sent a bare repository
  down the walk, which then listed the object store itself
  (`evidence/probes/test_abuse_walk_fallback_divergence.py`).
- user-decided: when there is no git the module walks the filesystem instead
  of failing, so a `git archive` copy keeps working.
- user-decided: on 2026-09-16 kouko narrowed the obligation to run in a
  `git archive` copy from six scanners to the five archive-capable ones, and
  chose a clean skip for the sixth.
- agent-decided: `rehearse_probes.py` run with no `--repo`
  in a directory git does not recognise prints one line saying it is skipping
  because rehearsal needs a git repository and this directory is not one, and
  exits zero. Only that case skips: an explicit `--repo` pointing at a
  non-repository, a bare repository, and any git failure inside a genuine
  repository all keep failing as before. The two cases are told apart
  without asking git, because git answers nothing both when there is no
  repository and when it refuses one or is not installed: the script walks
  upward from the working directory for a `.git` entry — a directory, or the
  file a linked worktree uses. No entry anywhere upward means this directory
  is not a repository, and it skips; an entry that git could not resolve is a
  git failure, and it fails with a message saying git failed.
- user-decided: both paths then drop any path with a component in a fixed
  ignore list holding the names already used in this repository — `.git`,
  `.pytest_cache`, `__pycache__`, `node_modules` (the intent's Constraints).
- agent-decided: names a single scanner excludes for its own rule, such as
  `docs` in `test_no_live_cot_explain_references.py:32`, stay with that
  scanner rather than joining the shared list, because they are that rule's
  scope and not a statement about what the repository owns.
- agent-decided: the module returns absolute paths; every caller already
  derives its own repo-relative form, and `check_plugin_boundaries.py:159`
  reports absolute paths.
- user-decided: nothing prevents callers outside loom's gates from importing
  the module; no documentation or stability promise is produced for them.
- agent-decided: `scripts/run_package_tests.py` excludes the UNION of
  `repo_files.nested_worktrees` (what `git worktree list` reports) and
  `repo_files.nested_repositories` (the opaque directory entries git collapsed),
  passing `--ignore` for each, rather than adding a repository-root
  `pytest.ini`; the repository has no root pytest config today and a bare
  root pytest run is known to abort on dbt-wiki collection. The union, not
  worktrees alone, because `evidence/probes/test_abuse_nested_repository_collection.py`
  showed a plain nested clone and a submodule still being collected — their
  failing tests failed this repository's suite — while `repository_files`
  already treated them as foreign.
- agent-decided: `check_doc_citations.py`'s module docstring argues that
  over-including untracked and ignored files is the conservative direction for
  its design (`check_doc_citations.py:114-121`). The rule it enforces does not
  change; only the candidate set does. That rationale is rewritten in the same
  task, because leaving it would document the opposite of the code.
- agent-decided: `check_doc_citations._exists_outside_the_candidate_set`
  consults the disk before an explicit-path finding is issued, and a hit
  DOWNGRADES the citation to UNCHECKED rather than resolving it. A target that
  is on disk but outside git's listing is not this document's repository to
  speak about, so the honest answer is loud skipping, not a clean verdict —
  resolving it would let the check read files the repository does not own. The
  walk is pruned at `nested_worktrees` ∪ `nested_repositories`, so a worktree
  anywhere, or a nested clone git does not ignore, cannot suppress a finding
  that CI will produce. A nested clone at a path git ignores is not listed by
  `nested_repositories` and can still downgrade such a finding, consistent
  with the intent's Out of scope.
- agent-decided: `repo_files.nested_worktrees` and `nested_repositories` live in
  the same module as `repository_files`, because they are the same git question
  seen from the other side — which subtrees inside this root are foreign — and
  keeping them together is what stops a second git invocation growing outside
  the module.

## Alternatives considered
- One shared helper in this repository's root `scripts/`: rejected because the
  shipped checker could not import it inside an adopting repository.
- One copy per tree (loom-code, loom-workflow, root `scripts/`): rejected as
  three copies of the same logic, the drift surface this repository avoids.
- Pure `git ls-files` with no fallback: rejected because it breaks the
  `git archive` use documented at
  `loom-code/scripts/test_write_plan_station_text.py:269`.
- Parsing `.gitignore` in-process instead of asking git, as ripgrep's `ignore`
  crate (https://github.com/BurntSushi/ripgrep/blob/master/crates/ignore/src/gitignore.rs),
  ruff (https://docs.astral.sh/ruff/settings/#respect-gitignore) and black via
  `pathspec` (https://github.com/psf/black/blob/main/src/black/files.py) do:
  rejected. Those tools must run in any directory; loom's gates only ever run
  inside a repository, which is the case where pre-commit shells out to git
  (https://github.com/pre-commit/pre-commit/blob/main/pre_commit/git.py). It
  would also add a dependency to a plugin that runs in arbitrary user
  repositories, and ripgrep's own tracker records where a hand-written parser
  still diverges from git (https://github.com/BurntSushi/ripgrep/issues/1221,
  https://github.com/BurntSushi/ripgrep/issues/1098).
- Honouring a `.gitignore` that is present when there is no `.git`: rejected.
  ripgrep, fd and ruff all ignore it in that case by default and require
  `--no-require-git` to opt in (ripgrep 12.0.0,
  https://github.com/BurntSushi/ripgrep/blob/master/CHANGELOG.md), so the
  fallback matches prevailing behaviour rather than inventing one.
- Bare `git ls-files` without `--others --exclude-standard`: rejected because
  it lists only tracked files, so a violating file not yet added would be
  missed — a silent pass, worse than a false report.

## Current state evidence
- Forward: `loom-code/scripts/git_exec.py:50` — `run_git(repo, *args, timeout,
  check, text, strip)` is the only git invocation body in loom-code/scripts.
- Reverse: `loom-code/scripts/loom_checker/helpers.py:249-267` —
  `changed_paths` already feeds `("ls-files", "--others", "--exclude-standard")`
  through `git_text`, so the shape is established.
- Error: `loom-code/scripts/git_exec.py:76,83` — OSError, timeout and non-zero
  exit all return `None` when `check=False`; there is no "not a git
  repository" branch, so absence of git is observed as `None`.
- Data: the six scanners keep their own skip sets and derive their own path
  forms — `check_doc_citations.py:228` skips only `.git`;
  `test_no_live_cot_explain_references.py:16` names five directories;
  `test_state_anchor_carrier_inventory.py:68-71` has no directory skip at all;
  `probes.py:96` keeps no path, only existence.
- Boundary: a live nested worktree exists at
  `<repo>/.claude/worktrees/fix+2026-09-16-plain-language-follow-ups` and is
  locked. Only three of the six scanners walk from the repository root and so
  currently reach it — `test_no_live_cot_explain_references.py:38`,
  `check_doc_citations.py:227`, `probes.py:96`. The other three scan a
  subtree or a fixed path and are exposed to ignored content inside their own
  scope rather than to that worktree. No pytest configuration in the
  repository sets `norecursedirs`, `testpaths` or `--ignore`, and
  `scripts/run_package_tests.py:31` hands pytest `loom-code/scripts/`,
  `scripts/` and `.claude/hooks/`, none of which contains that worktree today.

## UI flows
N/A — no interface a user reads or types into changes.
