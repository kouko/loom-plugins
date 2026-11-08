# Test-local persisted-save result probe

This is an unpromoted experiment, not a Loom capability, gate or installation.
`save_record(path, content)` writes only paths authorized by a trusted local
policy, reads the actual saved UTF-8 bytes and computes their SHA256. Full mode
returns the complete persisted body and bounded local inline-link observations;
confirmation mode performs the same internal operations but returns only the
same write confirmation. Tool name, description and argument schema are equal.

The policy JSON names an existing `root`, optional `create_roots` (directory
prefixes), `create_files` (exact filenames), `update_files` (exact existing
Markdown files), and `result_mode` (`full` or `confirmation`). With no write
paths all writes are denied. Preexisting collisions are never silently replaced.
Authorized updates and session-created files must still match the server's last
observed hash. Relative and absolute in-root targets are supported; traversal,
symlinks, source/config/instruction paths, and outputs over 32 KiB are rejected.

The stdlib newline JSON-RPC adapter exposes only this save operation. Launch
`python3 server.py --policy <trusted-policy.json>` through an explicit local MCP
configuration. It does not provide shell execution or outside-root read tools.
It has no credentials, network, dependency installation or persistent service.

Local link observations cover ordinary inline Markdown targets outside fenced
and inline code. Images/reference syntax, anchors, complex Markdown syntax and
external contents are not validated. Outside-root links and symlinks are not
followed. A present local file is not proof that it supports the research claim.
Malformed URL syntax remains an explicit unchecked result without losing the
truthful saved-body response. No semantic or overall validation pass is emitted.

Atomic file replacement/create-if-absent is followed by a point-in-time readback;
this is not a hardened concurrent-process sandbox or a guarantee that a later
writer cannot change the file. Server policy and native read-tool confinement
must both be validated before an actual agent experiment. Returning content does
not establish that an agent inspected or understood it.

Offline tests: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/local/engineering_research_save_probe/test_save_tool.py -q`.
Public synthetic control preparation and its scoped configurations live under
`/private/tmp/engineering-research-save-result-20261108/public-control/`; preparing
those files does not run a model or establish native integration.

`experiment.py public-run` explicitly invokes the two public controls and freezes
its inputs before requests. `experiment.py prepare` only creates eight opaque
private actors (four cases, one pair each), their instance policies and hashes;
it makes no model requests. `experiment.py run` refuses to launch until the
parent records specific eight-actor Anthropic authorization in
`private-run/authorization.json` and verified public custom-tool isolation in
`public-control/verified.json`. Preparing or passing tests is not that consent.
Public controls omit safe-mode because it disables explicit MCP; restricted
file tools, disabled slash commands, hooks/memory/instruction exclusions and
explicit-only MCP configuration therefore require actual public validation.
