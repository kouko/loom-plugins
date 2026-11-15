# Integration fix evidence

## W3-03 — OpenCode command inventory

The existing exact inventory test failed before this correction: the actual
loader registered `loom-workflow:whats-next`, while the expected list omitted
it. The skill declares `user-invocable: true`; the existing loader already
turns that metadata into a command. The correction adds the command at its
sorted position while retaining exact equality and the no-agents assertion.
The same missing invocation was added to the OpenCode command lists in all
three plugin README languages. No loader implementation or separate command
wrapper changed.

- RED: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_opencode_loader.py::test_plugin_without_agents_registers_no_agents_and_its_entry_commands -q` — 1 failed; extra actual item `loom-workflow:whats-next`.
- GREEN: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_opencode_loader.py -q` — 18 passed.

The orchestrator's integration handoff reports a complete changed-file search,
including runtime, the three skill guides and the plugin README invocation
sections. This task rechecked the actual loader, invocation metadata and
documentation references, locating the stale exact expected inventory and
the three README command lists. These results establish repository-loader
capability, not installation, discovery
reliability or successful invocation in an installed OpenCode host.

Earlier integration context supplied by the orchestrator: the complete package
suite had 13 failures and 2,846 passes; navigation verification subsequently had
17 passes, and skill-admission verification had 138 passes. Those runs were not
repeated by the W3-03 implementer and are not this task's verification claims.
