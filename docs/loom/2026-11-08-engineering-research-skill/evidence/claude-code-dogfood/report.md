# Claude Code dogfood preflight

Status: public native model access confirmed; six frozen explicit executors blocked by automatic approval review before starting. No target behavioral result or dogfood-pass verdict exists.

## Preserved infrastructure attempts

Two isolated-HOME native auth checks returned no login (5.9 and 4.6 seconds). The second used only two opaque nonsecret account UUID fields in a mode-0600 temporary file, deleted afterward. One public health invocation with only HOME/PATH also returned Not logged in, API duration/tokens/cost zero. Those attempts remain preserved; they are not target skill failures.

The harness had omitted normal OS identity/context environment fields. Restoring the nonsecret OS allowlist (HOME, PATH, USER, LOGNAME, SHELL, TMPDIR, LANG, LC_ALL, SECURITYSESSIONID, __CF_USER_TEXT_ENCODING) under original HOME enabled native first-party access without copying credentials or private config. Provider/proxy credential variables remained absent. Therefore the earlier no-login outcomes do not establish that the user's login is broken.

## Final public control

One final public-only probe used safe-mode, restricted file access, strict MCP, no session persistence, a session-only harmless public plugin, and explicit `claude-sonnet-5-5` at medium effort. It completed in 6.275 seconds. Actual modelUsage confirms provider firstParty and the requested fixed model. Reported usage: input 4, cache creation 4132, cache read 7104, output 270 tokens; list-price equivalent $0.0199464 (not a claim of additional subscription billing).

The inline plugin appeared in native init, but its harmless skill did not. An actual Skill call returned Unknown skill. This establishes that native target activation cannot be measured using this safe-mode setup; it is not an engineering-research trigger miss. Built-in skills/plugins remained. No private custom skills/plugins appeared in the observed catalog.

## Frozen explicit executor plan and rejection

Six cases, the original minimal real fixture, seven current runtime Markdown files, unchanged prompts and auditor criteria were frozen before any private-payload request. Actors would read the raw skill explicitly; no native activation claim was planned. Two parallel actors, 300-second timeout, fixed firstParty Sonnet 5.5 medium, no installation/publication/real-Vault access, no self grading. The fixture and executable harness remain under /private/tmp; the non-executable freeze receipt is `execution-freeze.json`.

Automatic approval review rejected the run because sending internal skill Markdown, prompts and fixture data to Anthropic was considered sensitive egress without sufficiently explicit user approval. No executor started and no workaround or indirect run was attempted. Continuing requires the user's explicit approval for those specified data categories to Anthropic.

Activation: 0/56; executor: 0/6. Source/package code unchanged. No global configuration edits or installs, no credential extraction, no production/Vault writes. Full host packaging/hooks remain untested. Independent output audits cannot proceed until executors produce artifacts.
