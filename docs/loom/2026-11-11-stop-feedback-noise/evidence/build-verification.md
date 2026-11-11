# Build verification

## W1 core behavior

Commit: b642d749257a94b49aaa031a98bb0c695e1e69c8.

The focused command was `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_delivery_stop.py loom-code/tests/test_delivery.py loom-code/tests/test_hooks_json.py loom-code/tests/test_hook_recovery_literal_path.py -q`.

- RED: 15 failed and 79 passed before implementation.
- GREEN: 94 passed after implementation.
- Restoring the old Claude block response made the response assertion fail; restoring the fix passed. This checks the actual response rather than host argument parsing alone.
- Existing explicit delivery and literal-dollar-path recovery tests passed. Both packaged hook recovery tests execute the recovered command after removing the hook-only host argument.
- Tests grew by 50 net lines across existing modules; no new test file or production abstraction was introduced.

Agent-decided metadata validation: each entry in a nonempty Claude background array must be an object with a nonempty string ID after trimming. No status or natural-language inference is performed. Codex does not use those arrays for pause decisions.

Native host evidence remains separate in `host-framing.md`: these tests validate source behavior, not an installed repair or interactive host UI. No installed configuration or persisted hook trust was modified.
