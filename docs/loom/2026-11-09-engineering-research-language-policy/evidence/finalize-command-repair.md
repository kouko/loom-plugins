# Finalization command declaration repair

## Scope and retained refusal

W3-01 corrects the active temporary finalizer input's adversarial command declaration. The installed finalizer refused that declaration before running the tests:

```text
BLOCK finalize.adversarial: command must execute the artifact directly
```

The raw refusal is preserved outside the repository at `/private/tmp/loom-language-policy-review/finalize.round1.log`, SHA-256 `500f852ccc1876c7933219c785be4b8ccee3e2860dfdba50445ca0fab74e1265`. The original input and reviewer verdicts are preserved alongside it as `finalize-input.round1.json`, `code-verdict.round1.yaml`, and `skill-verdict.round1.yaml`. The active input remains `/private/tmp/loom-language-policy-review/finalize-input.json`; only its command declaration changed. Reviewer target fields remain unchanged for the orchestrator's same-reviewer Round 2.

Rejected declaration:

```sh
env UV_CACHE_DIR=/private/tmp/loom-uv-relative-cache uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py
```

Corrected declaration:

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py
```

## Cause and focused verification

The installed checker at `/Users/kouko/.codex/plugins/cache/loom/loom-code/3.59.0/scripts/loom_checker/probes.py` recognizes the `uv run` wrapper through `_python_argv`; it does not unwrap an initial `env` command. Calling its actual `command_executes_artifact` function with the same artifact, `loom-code/tests/engineering-research/test_package.py`, returned `false` for the rejected declaration and `true` for the corrected declaration. Both assertions completed with exit 0 under the existing locked uv environment. An initial system-Python import could not load `yaml`; the successful verification used the existing requirements lock instead, without adding dependencies or a maintained test program.

The corrected declaration was then executed from the delivery checkout with `UV_CACHE_DIR=/private/tmp/loom-uv-relative-cache` supplied by the launcher environment, outside the declaration string:

```sh
UV_CACHE_DIR=/private/tmp/loom-uv-relative-cache uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/engineering-research/test_package.py
```

Actual output, exit 0:

```text
collected 5 items
loom-code/tests/engineering-research/test_package.py .....               [100%]
============================== 5 passed in 0.02s ===============================
```

No runtime guidance, maintained tests, probe program, accepted requirement, or historical command in `acceptance-test-evidence.md` changed. This is validation invocation evidence, not a product fix or a new behavior claim. The first reviewed digest, Round 1 refusal, counters and bounded episode remain retained; this repair does not reset them. Full-suite execution and same-reviewer Round 2 remain with the orchestrator; no finalization success or new reviewer approval is asserted here.
