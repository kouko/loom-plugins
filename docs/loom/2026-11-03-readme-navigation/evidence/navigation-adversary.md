# Documentation navigation — independent adversarial observations

The fresh-context navigation adversary read the intent, plan and navigation checks. It changed only its own permanent regression module; all destructive mutations ran in temporary copies.

## Observed RED

- The original inventory/navigation checks passed: 9 passed.
- Removing the project, plugin or runtime-instruction link from the Japanese and Traditional Chinese handoff guides escaped the English-only backlink check: six missing-link cases.
- A Markdown link inside an HTML comment or fenced example was incorrectly counted as live navigation: two parser cases.
- `python3 -m pytest tests/test_readme_navigation_adversarial.py` reported 8 failed before the correction.

## Observed GREEN

- After correction, that same independent module reported 8 passed.
- A temporary snapshot with a canonical GitHub link to a nonexistent sibling guide reported 1 failed, 8 passed; removing that mutation restored 9 passed.
- The orchestrator's locked-environment navigation and isolated-install checks reported 63 passed after the portability corrections.

## Independent-install corrections

The first complete package invocation reported 6 failed, 2709 passed, 2 skipped. Cross-plugin relative links violated existing installation boundaries; those documentation links now use canonical public GitHub URLs while within-plugin links stay relative. The boundary checker was not relaxed.

The local install-layout fixture also copied ignored macOS metadata. Two skill inventories now discover directories containing SKILL.md, matching host discovery, without deleting that metadata. A duplicate text assertion distinguishes public web documentation URLs from private installed filesystem paths.

## Retained regression command

`uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest tests/test_readme_navigation_adversarial.py -q`

These tests are permanent repository tests, not temporary probe programs. No independent reviewer verdict is asserted by this observation record.
