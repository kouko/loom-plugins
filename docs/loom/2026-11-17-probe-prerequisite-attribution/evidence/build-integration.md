# Build integration

## Selected content

- Branch: `testing-file-limit`.
- Branch base: `d3faa624d436f22aaa083b8f2b163bb924c2e7ba`.
- Tested HEAD: `8d3fa86fab76013f23da5572102a8beec108318f`.
- Release: loom-code `3.84.0`; installed cache is not updated.
- `sync-trunk` after conflict resolution and again before closing review:
  exit 0, up to date against `origin/main` at the base above; no commit added.

## Functional checks

The implementer recorded behavioral RED before each correction and focused
GREEN in [W1 evidence](w1-01-tests.md). Final focused result: 84 passed.
Release/protocol checks after trunk integration: 56 passed; generated manifest
check passed. The independent [adversarial report](adversarial-report.md)
records 17 attack points, zero successful attacks, zero new programs and one
reused program. Its exact declared command passed nine tests:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_probe_attribution.py -q
```

No important or fatal adversarial finding remains unresolved. The adversary
was dispatched once; it was not an implementer. No program required graduation.

## Complete package suite

Executed once after all implementation, release, trunk integration and
adversarial commits:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

Exit status: **0**. The 16 pytest group summaries total **4040 passed,
5 skipped**. All discovered shell tests also completed successfully. These
counts are distinct from adversarial program paths. Raw combined output was
captured at `/private/tmp/loom-probe-build-package.log`; counts were recomputed
from its final per-group summaries, not inferred from progress percentages.
The five skips remain disclosed; this result does not claim those tests ran.

## Handoff and limitations

The checked reviewer-count result was accepted with exit 0, status `passed`,
the unchanged change ID and `reviewer_floor: 2`. Independent acceptance will
test the same functional content in a clean copy before reviewers read it.
Finalization still owes its own package/probe execution and generated
attestation. No publication, installation, old finance test/finalizer execution
or reopening of the finance terminal episode is claimed.
