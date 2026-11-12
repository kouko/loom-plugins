# W1-01 implementation checks

## Scope and retained baseline

The implementation changes only `loom-design/skills/design-research/SKILL.md`.
Selection guidance stays inline; no reference, station, router, schema or gate
was added. The bundled research template is unchanged.

`baseline/SKILL.md` and `baseline/templates/research.md` are byte copies of
the original files at trunk `391fd017`, saved before editing for matched trials.
The baseline intentionally retains its former broader acquisition language;
it is evaluation input, not current runtime guidance.

## Verification status

The existing packaging test checks portability and resource links, not actual
agent research behavior. No new executable or keyword test was added for this
prose-only change. The six cases in `behavioral-cases.md` are inputs and checks,
not executed results; independent trial/acceptance evidence is still required.

The first focused test invocation could not create a lock in the default host
uv cache; a temporary-cache attempt then failed to resolve PyPI DNS. Neither
attempt executed tests. A narrowly escalated run used the existing host cache:

```
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-design/tests/test_design_research_package.py -q
..                                                                       [100%]
2 passed in 0.03s
```

The baseline skill and template were each compared byte-for-byte with
`git show 391fd017:<original-path>`; both comparisons returned true.
`git diff --check` passed. These checks establish packaging and retained input
integrity only; they do not establish the six unexecuted behavioral outcomes.
