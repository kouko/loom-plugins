# Blocked publication names the legal routes — spec

intent: 2026-09-18-blocked-publish-names-the-legal-routes@3bdaa258
pre-build-review: required — owed and not run. The declaration written at spec time (`not-required`) said the whole change was one refusal string plus the tests that lock it, and that no public contract changed shape; the build outgrew both clauses. What shipped also adds a refusal site inside the `PreToolUse` hook's PR-create route (REQ-9, REQ-10), a PR-body reader with a file-type guard (REQ-12), and an allowlist that narrows which PR-create commands that hook admits (REQ-11) — so a ship-canonical create carrying `--label` or `--assignee` is refused where it was admitted, and the hook's admission criterion is a public contract every adopting repository depends on, which is this repository's own threshold for `required`. Nothing in the gate is loosened and no data is touched, and the narrowing is reversible, carries no bill and loses nothing, so the scope stayed agent-decided; the review it owed is what did not happen. What stands in its place is the branch-end closing review, which recomputed the risk from the diff independently of this line and returned exactly this finding.

This spec exists under a `needs-design: no` intent because intake carried three
details the user stated about how the refusal must behave, and the repository's
two-document convention gives them no other home. REQ-1 to REQ-8 add no
requirement the intent's Acceptance lines do not already carry; REQ-9 to
REQ-13 were written at the closing review to record behaviour that shipped
after this spec's only commit, and the section they sit under says so.

## Requirements

REQ-1 — The refusal names both legal routes
  WHEN the publication gate refuses because the branch carries no attestation,
  the refusal shall name running the closing review and proposing a step
  selection the user confirms by typing → Acceptance #1

REQ-2 — The merge refusal carries the same information
  WHEN the merge command refuses for the same missing attestation, its output
  shall carry the same two routes → Acceptance #2

REQ-3 — The station prose forbids handing the command over
  WHEN an agent reads the ship station's prose, it shall find a rule stating
  that a blocked publication command is never handed to the user to run
  → Acceptance #3

REQ-4 — A confirmed skip publishes end to end
  WHEN the user has typed a skip confirmation, the closing review shall emit an
  attestation recording the skipped steps, and the publication command shall
  push and open a Ready pull request whose body carries the skip disclosure
  → Acceptance #4

REQ-5 — This change publishes and merges without user-typed git commands
  WHEN this change itself is published and merged, every git and gh action
  shall be executed by the agent → Acceptance #5

REQ-6 — No rule is loosened
  WHEN a branch carries neither an attestation nor a confirmed skip, the gate
  shall still refuse, and every existing refusal assertion shall still hold
  → Acceptance #6

REQ-7 — The blind run attributes each action
  WHEN the blind run walks the Acceptance lines, its report shall name the
  executing actor for each git and gh action observed → Acceptance #7

REQ-8 — The suite stays green
  WHEN the package suite runs, every existing test shall pass → Acceptance #8

### Recorded after the build

REQ-9 to REQ-13 were written into this spec at the closing review, not before
the build. Each records behaviour that shipped after this spec's only commit
`fe52c3a4`: REQ-9 in `f8a5559a`, REQ-10 to REQ-12 in `775eba95`, REQ-13 in
`bf3cfc81` and `41cbcf1b`. Only REQ-9 and REQ-13 answer to something the user
asked for. REQ-10, REQ-11 and REQ-12 were asked for by no Acceptance line and
no Constraint; each exists only to make REQ-9's check sound, and each names
what authorises it below. They are recorded rather than removed because
removing REQ-9 re-opens the hole it closed, and removing any of the other
three leaves REQ-9 holed.

REQ-9 — The hook's PR-create route discloses every skip
  WHEN the `PreToolUse` hook admits a PR-create command, the body it reads
  shall disclose every step the user's confirmed selection skipped, judged by
  the same function the publication command uses → Acceptance #4
  Authorised by the intent's Constraints line 3（每一次跳站都必須在 PR 內文揭露）
  and `PRINCIPLES.md` non-negotiable 2, which ends "every such skip must be
  disclosed in the pull request". Acceptance line 4 states that guarantee for
  the publication command's route; this is the other route that opens a pull
  request, and it was undisclosed until `f8a5559a`.

REQ-10 — That route enforces the whole rule whose id it prints
  WHEN the hook refuses a PR-create body, the refusal shall apply the whole of
  `push.contextual-body` — the nine headings, their substance and the ban on
  claiming to expose hidden reasoning — and not the disclosure clause alone
  → Acceptance #4
  Asked for by no Acceptance line and no Constraint. It exists because REQ-9
  made the hook print a rule id while enforcing one clause of it, which makes
  the rule id false about what was checked.

REQ-11 — Only an allowlisted trailing option is admitted
  WHEN the hook judges a PR-create command, it shall admit only the trailing
  options this repository lists as canonical, and refuse every other spelling
  as non-canonical → Acceptance #6
  Asked for by no Acceptance line and no Constraint. It exists because REQ-9
  introduced a body read whose path resolution could diverge from the shell's,
  and a denylist can only ever be as current as the release notes of the tool
  it lists. Its adopter-visible cost is recorded deliberately: a ship-canonical
  create carrying `--label` or `--assignee` is refused where it was admitted,
  which is an obligation on future commands in every adopting repository. It
  admits strictly less than before, so Acceptance line 6 still holds.

REQ-12 — The body reader reads only a readable regular file
  WHEN the hook reads the body a PR-create command names, it shall read only a
  readable regular file, treat `-` as no path at all, and read an unreadable
  body as empty → Acceptance #4
  Asked for by no Acceptance line and no Constraint. It exists because REQ-9's
  read runs inside a hook with no timeout of its own, where an unguarded read
  of a FIFO blocks the agent forever and one of a character device never ends;
  an empty body has none of the nine headings, so an unreadable body refuses.

REQ-13 — The refusal tail names only what is true of its own state
  WHEN the publication or merge refusal reports an attestation count, the tail
  it appends shall name the two legal routes only where both are live, and
  otherwise name what is true of that state instead: above one attestation,
  what reduces the count; on an empty delta over a base that already attests
  and that the remote's own default branch already contains, that there is
  nothing here to publish; and where the count could not be read, no count and
  no route
  → Acceptance #1
  Authorised by Acceptance line 1, which asks the refusal to name the routes.
  A route named where it cannot reach the state it claims is worse than none:
  the agent runs it forever. The spec as first written described one tail;
  four shipped. The published-trunk clause is the closing review's round-2
  finding: an empty delta over an attesting base is also what a finished,
  attested branch looks like once its local trunk is fast-forwarded onto it,
  and telling that branch there is nothing here to publish sends a complete
  change back to a new intent. The two states are identical in git, so only a
  remote separates them, and where no remote default branch resolves the tail
  is withheld and the two routes stand.

## Design decision

- Naming the routes rather than downgrading the refusal is the user's choice,
  taken after the adversarial review of the downgrade exposed the four surfaces
  it would sever; the gate keeps every rule it has today. user-decided.
- Extend the existing missing-attestation reason (`command_handlers/push.py:483-490`)
  rather than adding a second emission path. The hook, `publish` (`publish.py:415`)
  and `land` (`land.py:939`) all route that verdict through `_cmd_push`, so one
  string reaches three callers. agent-decided.
- The reason stays a **single line**. `report()` (`helpers.py:40-43`) writes one
  `BLOCK <rule>: <reason>` line per failure, and
  `test_adversarial_push_reason.py:113-116` asserts every stderr line on a
  hostile unattested push begins with `BLOCK `. A wrapped reason would emit
  continuation lines without that prefix. agent-decided.
- `report()` itself is not touched: it is shared by every command handler, and
  the intent forbids changing its semantics. agent-decided.
- The two test constants asserting the current reason
  (`test_loom_publish.py:1210`, and the equivalent in
  `test_adversarial_push_reason.py:147-155`) are updated to the new text. They
  keep asserting a refusal; neither assertion is removed or weakened.
  agent-decided.
- The ship station's rule (REQ-3) is advisory prose, not a gate, and is not the
  primary carrier. `PRINCIPLES.md:18` forbids prose-only gates, and the observed
  failures happened mid-build where that file is not loaded. The refusal string
  is the carrier guaranteed to be read at the moment of failure; the prose only
  covers an agent that declines before attempting. agent-decided, from the
  complexity gate.
- `land` refuses earlier than the shared check when no attestation exists
  (`land.py:920-924` derives the change id and acceptor set from the
  attestation path). REQ-2 is therefore satisfied by the earlier refusal
  carrying the routes too, not by reaching `_cmd_push`. agent-decided.
- REQ-9 and REQ-10 call `publish`'s own `selection_disclosure_failure`
  (`publish.py:182`) and `validate_contextual_pr_body` from inside the hook
  (`command_handlers/push.py:306-312`), never a second copy of either rule: a
  copy is a second drift surface, and the rule id the hook prints is publish's.
  The import is deferred inside the branch because `publish` imports
  `_cmd_push` from that module and the two would cycle at module level.
  agent-decided.
- The disclosure's several-line rendering is flattened onto one line at this
  emission only (`command_handlers/push.py:321`). `report()` writes the reason
  verbatim and every caller of the hook parses the `BLOCK ` prefix, so a
  newline would emit a line carrying none; `publish`'s own output is a terminal
  and keeps the shape a reader can act on. agent-decided.
- REQ-11 is an allowlist (`rule_checks/push.py:233-235`) rather than the
  repo-override denylist it replaced, and only the separate-value spelling is
  canonical. Its cost — `--label` and `--assignee` now make the canonical form
  non-canonical — is an obligation on every adopting repository, and it is
  agent-decided rather than user-decided because it is reversible, carries no
  bill and loses no data. agent-decided.
- REQ-12 puts the same readable-regular-file guard on the hook's body read that
  `_publish_args` already puts on `--body-file`, and treats `-` (gh's spelling
  for stdin, which the gate cannot see) as no path. agent-decided.
- REQ-13 is four module constants selected by one pure function
  (`publication_advice`, `command_handlers/push.py:142-156`), not four emission
  sites: `nothing_left_to_publish` is recomputed from the repository by the
  caller and passed in, so the function that picks the tail reads no state
  itself. agent-decided.
- The published-trunk fact asks the remote which branch is its default, through
  `intent_state.remote_default_snapshot` (`base_is_published`,
  `command_handlers/push.py:160-184`), the same resolver
  `selection skipped-review` already uses. It reads `refs/remotes/origin/HEAD`,
  which git writes from the remote's own default at clone time, so a repository
  whose trunk is called `trunk`, `develop` or `release` is read correctly and no
  branch name is carried in this checker. `helpers.TRUNK_CANDIDATES` cannot
  serve: a local `main` is moved onto a branch by one `git branch -f`, and
  `@{upstream}` is the branch's own upstream, which an unmerged pushed branch
  contains trivially — neither witnesses a publication. agent-decided.
- Boundary, recorded rather than closed: the witness is a local ref, and an
  agent can write `refs/remotes/origin/HEAD` and a remote-tracking branch
  itself; a stale cache after a remote rewind reaches the same state with
  nobody acting. No offline check can tell a fetched ref from a written one —
  git records no provenance for either — and confirming one would mean a
  network call inside a `PreToolUse` hook that runs on every Bash tool call and
  has no timeout of its own, which is a worse defect than the one it would
  close. The failure direction is the safe one: a false witness makes an agent
  withhold its own finished publication, and admits nothing, because the
  attestation, origin and PR gates are untouched by it. agent-decided.

## Alternatives considered

- Downgrade the refusal to a warning — rejected by adversarial spec review: the
  attestation is also the change-id source, the delivery witness, the
  skip-audit key and the disclosure input, so downgrading its verdict severs
  four unrelated surfaces and breaks two ratified non-negotiables. Recorded in
  the intent's Out of scope.
- Put the rule only in the ship station's prose — rejected: prose-only gates are
  forbidden, and the file is not loaded where the failure occurs.
- Give `report()` a severity dimension — rejected: it is shared by every command
  handler and the intent forbids changing its semantics.
- Fix it in the user's own global instructions — rejected: it would hold on one
  machine only, and the intent asks for behaviour the mechanism carries.

## Current state evidence

- Forward: `command_handlers/push.py:483-490` returns the missing-attestation
  refusal through `report()`.
- Reverse: `publish.py:415` and `land.py:939` both call `_cmd_push`;
  `land.py:920-924` refuses earlier when the attestation is absent.
- Error: `helpers.py:40-43` writes exactly one `BLOCK <rule>: <reason>` line per
  failure and returns 1.
- Data: `command_handlers/finalize.py:86-98` drops the reviewer floor to zero for
  a bound skip and records the selection in the attestation it emits.
- Boundary: `test_adversarial_push_reason.py:113-116` asserts every stderr line
  on fourteen hostile unattested pushes begins with `BLOCK `.
- Forward (hook route, REQ-9/REQ-10): `command_handlers/push.py:306-312` runs
  the body check after the shared push check returns 0 on a PR-create command.
- Boundary (REQ-11/REQ-12): `rule_checks/push.py:238-253` walks the trailing
  tokens against the allowlist; `rule_checks/push.py:292-336` reads the body
  from the last `--body-file` and returns "" for anything it cannot read.
- Data (REQ-13): `command_handlers/push.py:160-215` recomputes the empty-delta,
  attesting-base and published-base state from the repository — the third
  through `intent_state.remote_default_snapshot`, which `selection
  skipped-review` (`command_handlers/selection.py:228`) already reads the same
  way — and answers False on any doubt.

## UI flows

| case | what the caller does | what they see |
|---|---|---|
| unattested publication | runs the publication command on a branch with no attestation | the existing refusal, extended on the same line with the two routes and the instruction not to hand the command to the user |
| unattested merge | runs the merge command | the same two routes |
| confirmed skip | the user types the skip confirmation, then the agent runs closing review and publication | an attestation recording the skipped steps, a push, and a Ready pull request whose body discloses the skip |
| no attestation, no confirmation | anything else | refused exactly as today |
| hook route, skip undisclosed | the agent runs the canonical PR-create command through the hook on a branch whose confirmed selection skipped a step, with a body that does not disclose it | `BLOCK push.contextual-body: …`, carrying the disclosure it expected, flattened onto the one line every caller parses |
| hook route, body below the floor | the same command with a body missing one of the nine headings, or claiming to expose hidden reasoning | the same rule id, naming what the body lacks |
| PR-create with an unlisted option | adds `--label`, `--assignee` or any other spelling outside the allowlist to the canonical form | `BLOCK push.attestation: PR creation must use the canonical trusted-gh command from loom-code:ship` |
| PR-create whose body file cannot be read | names a FIFO, a device, a directory, an unreadable path, or `-` | the body reads as empty, so the create is refused on the nine headings, and the hook returns instead of blocking on the read |
| more than one attested change | publishes or merges a delta carrying two attestations | the refusal naming what reduces the count, and no route |
| empty delta over an attesting base the trunk carries | publishes a branch that adds nothing to a base that already attests and that the remote's default branch contains, whatever it is named | the refusal saying there is nothing here to publish, and that the change starts from a new intent on its own branch |
| the same delta, base not published | publishes a finished attested branch whose local trunk was moved onto it, or any branch where `refs/remotes/origin/HEAD` does not resolve | the two legal routes, because the branch may still hold work nobody has published |
| count nobody could read | merges where the count after `found ` is not a plain integer | the refusal naming no count and no route, pointing at `push` in the repository |
