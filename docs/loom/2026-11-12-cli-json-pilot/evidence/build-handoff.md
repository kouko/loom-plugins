# JSON pilot implementation and release handoff

W0 preregistration: `030eb89604df322e6dafea25294c76c97edd645e`.
W1 implementation: `1cc65be288ddb6390342e112e49b7f2b58591254`.

W1 added four public-entry tests, one positive and one boundary case for each
of Acceptance 1 and 2. Actual first execution was RED: 3 failed, 1 passed;
the three failures were absent JSON output rather than setup failure. The
minimal implementation subsequently passed 48 focused JSON/CLI/architecture
cases. Another 224 existing intake, intent and field-cap cases passed.
The original architecture guard and existing tests were not weakened.

Raw retained outputs: [w1-red.txt](w1-red.txt), [w1-green.txt](w1-green.txt),
[w1-legacy.txt](w1-legacy.txt). Each was executed through the repository's
locked isolated uv environment. Cache access required normal host escalation;
no package was installed into the base environment.

W2 synchronizes loom-code 3.71.0 in the SSOT and generated manifests, root and
three language READMEs, the new CHANGELOG entry and CURRENT_VERSION test pin.
`python3 scripts/sync_codex_manifests.py --all --check` exited 0.
The focused JSON, CLI, architecture and release checks passed all 91 cases:
[w2-focused.txt](w2-focused.txt). Scoped whitespace checking passed.

These executions do not establish the independent comparison, complete
package-suite result, adversarial result, independent acceptance, review,
attestation, remote publication or installed-host behavior. Those are later
Build and closing-review obligations. No efficiency improvement is claimed.
