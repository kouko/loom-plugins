# Adversarial execution evidence

The independent attacker `/root/release_flow_adversary` inspected committed
functional content at `8d6c1e471cb83dc4958261fd1ad5ccc9bbe39c1a`.
It recorded seven attack points: three textual temptation checks and four
executed recipe-width cases. No defect earned a new probe program.

The literal, reviewed on-disk recipe executed at widths 72, 40, 61 and 62.
Final-composition alignment passed for widths 72 and 40. Alignment at the
other two widths and unequal-topology variants was not completed; these are
not passing checks. A local command guard rejected dynamic launcher forms,
and that form was stopped without disabling or bypassing the guard.

The attacker nominated the existing
`loom-workflow/tests/loom-visualization/test_templates.py` as reusable
coverage. Its existing concern marker covers example/diagram drift. The
attacker could not start pytest because of cache permissions and DNS in its
environment. The orchestrator subsequently executed that exact existing
test module in the repository's locked environment:

```text
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-workflow/tests/loom-visualization/test_templates.py
22 passed
```

The existing suite checks the saved outer-frame ASCII block, template
structure and prior generator examples. Independent acceptance separately
reproduced the new saved comparison exactly and checked both supported
layouts. These executions establish bounded artifact coverage, not automatic
host selection or human comprehension. The finalizer will execute the
nominated existing module again as the recorded adversarial program.

There are no unresolved product findings and no new adversarial programs.
