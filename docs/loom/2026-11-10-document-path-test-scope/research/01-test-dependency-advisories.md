---
title: "Applicability of Mermaid test dependency advisories"
type: loom-research
status: concluded
created: 2026-11-10
updated: 2026-11-10
change: 2026-11-10-document-path-test-scope
tags:
  - loom/research
---

# Applicability of Mermaid test dependency advisories

## Question and scope

What do the reported npm vulnerabilities mean for this repository's Markdown
Mermaid parser tests? Inspect the locked graph and current invocation without
upgrading dependencies or executing advisory payloads. Local tracked sources
were inspected at `d7af54f1d70632dc8bbc05abb84da9ccdcdbd363` (W1-01 may have
concurrent test-only edits). Advisory pages were read on 2026-11-10.

## Method and rationale

Use direct manifest, installed-source and call-path inspection, complemented by
the exact primary GitHub advisory pages identified in the audit. This bounded
threat assessment compares exploit prerequisites with the test's input and output
boundaries; it is not a general dependency review. Known applicable primary URLs
made exploratory language searches unnecessary. Stop after attributing every
reported advisory and identifying material reachability limits.

## Findings

The retained [raw audit snapshot](../evidence/npm-audit.json) reports three
package findings: DOMPurify critical, KaTeX low and Mermaid low. These represent
six underlying advisories, not three independent exploits. Mermaid's finding
is inherited through KaTeX (`via: ["katex"]`); it does not name an additional
Mermaid advisory. All six affected-version ranges include the locked versions.
The critical label must remain visible: reduced local exposure is not a severity
reclassification. The snapshot's CVSS score fields are zero with null vectors;
they do not establish zero risk or a measured project-specific score.

The [test manifest](../../../../loom-workflow/tests/mermaid/package.json) puts
Mermaid and jsdom under `dependencies`, so npm's snapshot classifies 150 packages
as prod and zero as dev. That metadata describes this nested npm project, not
production use by the plugin. The
[package runner](../../../../scripts/run_package_tests.py) lines 139–144 installs
this project with `npm ci --prefix loom-workflow/tests/mermaid`, runs the
[validator](../../../../loom-workflow/tests/mermaid/validate_mermaid.mjs), then
runs its [negative test](../../../../loom-workflow/tests/mermaid-validator-negative.sh).
This observed integration is test-only. It still executes dependency code in the
developer/CI process and processes repository changes, including untrusted changes
when a contributor supplies them. Test-only status does not eliminate risk.

### Locked graph and advisory conditions

The [lockfile](../../../../loom-workflow/tests/mermaid/package-lock.json) fixes
jsdom 26.1.0 and Mermaid 11.17.0. Mermaid depends on DOMPurify `^3.3.3`, resolved
to 3.4.15, and KaTeX `^0.16.47`, resolved to 0.16.47. Both are transitive;
Mermaid is direct. The installed Mermaid package and its export target were read
and identify version 11.17.0 and `dist/mermaid.core.mjs`.

| Advisory / primary source | Published severity; affected / patched version | Required behavior and comparison with inspected path |
|---|---|---|
| [GHSA-p98j-92pf-mc4p](https://github.com/advisories/GHSA-p98j-92pf-mc4p) | Low; 3.4.13–3.4.15 / 3.4.16 | DOMPurify `IN_PLACE` on a live DOM subtree with an after-sanitize hook removing a node leaves event attributes armed. Inspected test sanitization accepts strings; Mermaid's inspected attribute hooks modify attributes rather than detach nodes. This required combination was not established. |
| [GHSA-6688-9rhm-gjv2](https://github.com/advisories/GHSA-6688-9rhm-gjv2) | Low; ≤3.4.15 / 3.4.16 | A rawtext DOM root returned from `IN_PLACE` must be serialized and reparsed as HTML. Validator does not consume returned DOM or reparse sanitizer output into a page. |
| [GHSA-cg2g-xh64-v4q7](https://github.com/advisories/GHSA-cg2g-xh64-v4q7) | Critical; 3.4.4–3.4.16 / 3.4.17 | `SAFE_FOR_TEMPLATES` plus DOM-returning mode and attacker-supplied attached shadow root; surviving expressions must reach a downstream template engine. Inspected validator passes diagram strings and reports parse results; no downstream template evaluation is present. |
| [GHSA-mrv2-3pqr-j5jr](https://github.com/advisories/GHSA-mrv2-3pqr-j5jr) | High; ≤3.4.16 / 3.4.17 | Incomplete earlier fix: an `IN_PLACE` hook detaches a parent or sibling, leaving descendant handlers armed. Same live-node/removing-hook combination is not established in the inspected path. |
| [GHSA-c6gr-qvv4-5v3f](https://github.com/advisories/GHSA-c6gr-qvv4-5v3f) | Low; ≤3.4.16 / 3.4.17 | XHTML parsing plus allowlisted SVG animation/`attributeName`, followed by activation of a surviving link. No XHTML sanitizer configuration or SVG page activation was observed in the inspected default test invocation. |
| [GHSA-238p-pmpm-9mq7](https://github.com/advisories/GHSA-238p-pmpm-9mq7) | Low; ≥0.11.0, <0.18.2 / 0.18.2 | KaTeX reads already polluted prototypes or attacker-influenced options prototypes; hostile math output inserted into a page without separate sanitization can enable links/resources. KaTeX does not itself create the pollution or execute scripts merely by rendering. Neither pollution nor page insertion was demonstrated here. |

These summaries derive from the read advisory descriptions, not only their
titles. DOMPurify's first two pages were updated September 30 / October 5,
2026; the latter three October 22, 2026; KaTeX October 5, 2026. No advisory was
inaccessible. Patch versions describe each advisory, not a tested upgrade path.

### Reachability and trust boundaries

The validator constructs an empty JSDOM document (without a `runScripts` option),
installs window/document globals, imports Mermaid and initializes it with
`startOnLoad: false`. It calls `mermaid.parse` on fenced strings from the skill's
`templates/*.md` and `references/*.md`, or explicitly named local files. Results
are terminal OK/FAIL messages; it calls no Mermaid rendering API.

Importantly, parsing is not isolated from DOMPurify. Installed Mermaid source
`dist/mermaid.core.mjs:1081` preprocesses configuration/directives then calls
`getDiagramFromText` (`:1404`) → `Diagram.fromText` (`:920`) → dynamically loaded
parser with database callbacks (`:943`). In
`dist/chunks/mermaid.core/chunk-RHFEMEQ7.mjs:103–104,193,634`, flowchart database
methods sanitize labels/subgraph titles. The shared
`chunk-DU6HZSFF.mjs:5064–5122` installs DOMPurify hooks and calls `sanitize`;
`sanitizeText` uses caller `dompurifyConfig` if supplied, otherwise forbids style
tags and returns a string. This establishes a reachable sanitizer surface, not
exploitability of the listed non-default modes.

The same shared chunk at `:5227–5254` dynamically imports KaTeX and calls
`renderToString` inside math-rendering helpers, with a sanitized wrapper also
present. The validator's entry point does not call those rendering helpers.
This partial static inspection did not enumerate every diagram's parser or
prove that KaTeX is unreachable for every possible input. Mermaid processes
frontmatter/directive configuration during parsing; absence of suspicious terms
in today's examples cannot prove hostile future inputs cannot influence it.
A scoped search of current templates/references found no `IN_PLACE`,
`SAFE_FOR_TEMPLATES`, `PARSER_MEDIA_TYPE`, `dompurifyConfig` or prototype-mutation
configuration. That negative result is supporting context only.

## Evidence and verification

- Read the complete audit JSON, manifest, validator and negative-test script;
  inspected the package runner's Mermaid commands and selected installed source
  bodies above. `python3` JSON inspection printed the locked dependency entries
  for Mermaid, DOMPurify, KaTeX and jsdom; results are the versions stated above.
- Source searches: `rg -n 'mermaid|validate_mermaid' scripts/run_package_tests.py
  loom-workflow/tests/mermaid`; targeted `rg -n` for parse, sanitization, KaTeX,
  and advisory configuration identifiers in the installed Mermaid modules and
  current visualization templates/references. Read matching function bodies with
  `sed`, including the parse-to-database boundary and sanitizer hooks.
- Read all six linked primary GitHub advisory pages, including their descriptions,
  affected ranges, severity and patched versions. No exploit snippets were run.
- Copied the supplied snapshot unchanged; this research did not rerun npm audit,
  install dependencies, change the lockfile, or infer the original audit command,
  npm version, timestamp or registry configuration from the snapshot.
- Read the saved record in full and resolved its relative Markdown links; checked
  the copied JSON equals the supplied source byte-for-byte.

## Decision impact

The existing locked test graph contains known vulnerable versions and should be
reported accurately. For the inspected parse-only test invocation, the concrete
browser/template execution chains in these advisories were not demonstrated;
that supports a bounded exposure distinction, not a claim of safety, a false
positive classification, or permission to silently suppress the critical finding.
The authorized action is retention and assessment; no remediation was applied.
The snapshot suggests a DOMPurify fix is available and a major Mermaid change
for its inherited KaTeX finding, but compatibility and effective remediation
were not evaluated. Reassess if test inputs, sanitizer configuration, rendering,
page consumption, prototype state, dependency versions or advisory content change.
See the owning [plan](../plan.md).

## Limitations and open questions

This is static inspection plus primary advisory comparison, not dynamic coverage
or exploit testing. No malicious inputs, call tracing, browser execution or
proof of absent prototype pollution was performed. Node/npm versions and original
audit collection provenance are not recorded in the supplied JSON. Installed
source was inspected locally at matching package versions; its complete contents
were not independently revalidated against registry integrity hashes. Ignored
`node_modules` source anchors are reproducible after installing the lockfile but
are not committed evidence links. Other vulnerabilities, supply-chain compromise,
and all arbitrary Mermaid configurations are outside this bounded assessment.
