---
name: a-host-tool-mapping-must-carry-every-argument-that-moves-where-the-call-acts
description: A host adapter that translates host tool calls into Claude-shaped hook payloads must carry every argument that changes where the call acts (workdir, cwd, a base directory), because path-based guards reason about where a call acts — an argument dropped from the mapping is invisible to every guard downstream and turns a denied write into a passing one
type: gotcha
sources:
  - resource: branch engineering/2026-09-29-opencode-v2-compatibility (2026-09-29) — closing-review Round 1 code reviewer found it fatal; fixed in commit 02f41629
---

Porting loom's hooks to OpenCode v2, the adapter copied only the tool
arguments seen in payload samples. OpenCode's `shell` tool also takes
`workdir` (the directory the command runs in). Dropping it meant the
selection guard's "cwd inside the loom record directory" check and the
loader's fallback never saw where the command ran, so a plain redirect with
`workdir` inside the record store passed both guards. Live samples had not
shown `workdir`; the host binary's own tool schema did.

**Why:** path-based guards decide by where a call acts. Any argument that
changes that (workdir, cwd, a base directory) is guard input, not
decoration; observed samples only show the arguments callers happened to use.

**How to apply:** when writing a host tool mapping, enumerate each tool's
full argument schema from the host's own definition (binary strings or a
schema dump), not only observed payloads. Map every location-changing
argument into the payload cwd or paths. Add one test per such argument
asserting that a store write through it is denied.
