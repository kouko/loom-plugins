# Package / Tool Discovery Guide

Use this when a decision needs a candidate list but none exists yet — before a
trade study (evaluation-selection.md, the "Which design, library or
implementation fits best?" question). If credible candidates already exist, go
straight to the trade study and skip this guide.

Discovery answers "what candidates exist"; evaluation answers "which fits best".
Do not let discovery turn into evaluation.

## Search sequence

Run the steps that apply to the domain. Stop when the stopping rules below are
met; these are levers, not a mandatory checklist.

### 1. Package registry

```bash
# PyPI has NO keyword search CLI. `pip search` and `pip index search` are dead.
# Keyword search is browser-only (the search page is JS-rendered; curl does not work):
#   https://pypi.org/search?q=<keywords>

# Scriptable existence/version check:
python3 -m pip index versions <pkg>

# Verify installability against the target interpreter:
python3 -m pip install --dry-run <pkg>
```

When you cannot open a browser, script the registry verification around
candidate names from GitHub searches (step 2) instead of scraping PyPI.

For npm: browse `https://www.npmjs.com/search?q=<keywords>`, then
`npm view <pkg>` for versions and metadata.

### 2. GitHub topics

Web search syntax (topic + popularity + recency):

```
topic:<keywords> stars:>50 pushed:>2024-01-01
```

`gh search repos` takes the same qualifiers inside the query string. The
`--topic` flag alone does not accept a free-text phrase; a multi-word phrase
returns nothing.

```bash
gh search repos "topic:<keyword> stars:>50 pushed:>2024-01-01" --limit 20 \
  --json fullName,description,stargazersCount,updatedAt,license

# topic-only enumeration (no free-text phrase):
gh search repos --topic <topic> --stars ">100" --limit 20 \
  --json fullName,description,stargazersCount
```

A plain keyword query with `--stars`/`--updated` filters works too when the
topic name is uncertain; treat a zero-hit result as "the phrase is wrong", not
"nothing exists".

### 3. Awesome lists

- Search `awesome-<language> <domain>`.
- Check the curated README for an entry for a project under consideration.

### 4. Dependents / "Used by"

Check that someone uses a candidate in production, not just that it exists.

```bash
# PyPI dependents are browser-only:
#   https://pypi.org/project/<pkg>/#data
# GitHub dependents are web-only too (there is no REST "dependents" endpoint):
#   https://github.com/<owner>/<repo>/network/dependents

# Scriptable substitute — find repositories whose manifests declare it:
gh search code 'api "pkg==<version>" filename:requirements.txt' --limit 5 \
  --json repository,path
gh search code '"<pkg>" filename:package.json' --limit 5 --json repository,path

# Local codebases that already depend on it:
grep -rl "<pkg>" ~/my-projects/ 2>/dev/null | head -5
```

### 5. Security filter (before keeping)

```bash
# pip-audit must be installed separately: python3 -m pip install pip-audit
pip-audit --format json <pkg> 2>/dev/null | head -c 2000

# OSV scanner (optional): https://github.com/google/osv-scanner
osv-scanner --pkg <pkg> 2>/dev/null || true

# CLI-free alternative — OSV API:
curl -s -X POST https://api.osv.dev/v1/query \
  -H 'Content-Type: application/json' \
  -d '{"package":{"name":"<pkg>","ecosystem":"PyPI"}}' | head -c 2000
```

Stop point: a known CVE/HIGH advisory → DROP unless the project's risk
tolerance explicitly accepts it (record why).

### 6. License filter

- Keep: MIT, Apache-2.0, BSD-3-Clause, MPL-2.0, ISC.
- Exclude: GPLv3/AGPL and commercial-only, unless the project policy allows.
- Read the actual LICENSE file; a GitHub topic or a short description is not a
  license.

### 7. Personal starred repos (the user's own signal)

Projects the user starred are pre-filtered by their own taste — likely
approved architecture, docs quality, or domain fit. Mine them for candidates,
reference implementations, or dependency lists.

```bash
# All starred repos (paginate — the default page returns 30 only):
gh api user/starred --paginate --jq '.[].full_name'

# Filter by keyword in name or description. Guard null descriptions:
# `test(null)` aborts the whole jq expression, so use (.description // "").
gh api user/starred --paginate --jq '.[] |
  select((.full_name | test("<pattern>";"i"))
      or ((.description // "") | test("<pattern>";"i"))) |
  .full_name'

# Detail view (name, description, language, stars, last update):
gh api user/starred --paginate --jq '.[] |
  {name: .full_name, desc: (.description // ""), lang: (.language // ""),
   stars: .stargazers_count, updated: .updated_at}'

# Reference implementation: read the starred repo's files / dependency manifests
gh repo view <owner>/<repo> --json files,description,primaryLanguage
```

Also inspect a starred repo's `requirements.txt` / `package.json` /
`Cargo.toml` and its Issue/PR discussion for known pitfalls.

### 8. Re-check after narrowing

After applying the security and license filters to the surviving candidates,
run the registry verification (step 1) once more on the finalists so the
candidate table records real, installable, current versions.

## Output format (input to the trade study)

| Candidate | Source | Stars | Last commit | License | Key fit | Gap | Verdict |
|---|---|---|---|---|---|---|---|
| `pkg-a` | PyPI | `5.2k` | `2026-11-20` | `MIT` | Full | — | **KEEP** |
| `pkg-b` | GitHub topics | `1.1k` | `2025-06-15` | `Apache-2.0` | Partial | Missing feature X | **DEFER** |
| `pkg-c` | awesome-list | `800` | `2026-10-01` | `BSD-3` | Full | — | **KEEP** |
| `pkg-d` | starred repos | `2.3k` | `2026-10-15` | `MIT` | Full | — | **KEEP** |

Verdicts:

- **KEEP** — enters the trade-study candidate list.
- **DEFER** — has a gap but may fit later; record the gap.
- **DROP** — fatal defect (security, license, missing core capability).

## Stopping rules

1. 3+ KEEP candidates → stop discovery, enter the trade study.
2. ~20 min of searching with <2 KEEP → broaden keywords, or ask the team.
3. Every candidate has a critical gap (security, license, core capability) →
   treat as "no suitable package exists" and switch to direct source
   inspection (build it, or modify a source).

## Integration with the trade study

- KEEP candidates → the trade study's credible-alternative list.
- DEFER / DROP → the trade study's "evaluated and rejected" column, with the
  reason.
- No KEEP → adjust keywords, or self-implement / modify a source.

Save the discovery table under
`docs/loom/<change-id>/research/<sequence>-discovery.md` so the trade study
and this table sit in the same directory. Discovery is part of the research
record: record the method and the evidence, per the skill's retained-records
rules.

## Worked example

Question: implement case-insensitive substring search in a skill — use a
package or Python stdlib? Steps below are the actually observed outputs from
running this guide on 2026-11-25.

| Step | Observed result | Verdict |
|---|---|---|
| PyPI keyword search (browser) | search page is JS-rendered; curl returns no result rows — browser-only | — |
| `python3 -m pip index versions regex` | `regex` 2026.11.23, installable | — |
| License check (PyPI API `license_expression`) | `regex` = Apache-2.0 AND CNRI-Python (permissive, allowed) | — |
| OSV API query for `regex` | `{}` — no known advisories | — |
| GitHub repo search `regex-trie` | `alexeld/regex-trie`, 57 stars, updated 2025-03-13; `pip index versions regex-trie` → not on PyPI | **DROP** (too small, not on registry) |
| Stdlib `re` | no dependency, no advisory | **KEEP** |
| Starred repos filter (null-safe jq) | no starred repo implements substring search specifically; the filter pattern ran clean | — |
| Final list | `regex` (mature, registered, clean), stdlib `re` | KEEP 2 → trade study |

Trade-study input: candidate list `regex` / stdlib `re`; dimensions:
capability, complexity, dependency risk, docs quality.
