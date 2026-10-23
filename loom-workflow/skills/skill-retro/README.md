# skill-retro

**English** | [日本語](README.ja.md) | [繁體中文](README.zh-TW.md)

Review selected past or current Claude Code and Codex sessions for recurring problems in a readable target skill. Current-session analysis uses only the captured snapshot through its capture cutoff, excluding later appended events. An explicit readable target source path works without installation in the reviewing host. Proposals can address its instructions or directly related plugin registration, loading, hooks, bundled scripts, and dependent connectors. This skill produces review artifacts; an independent implementation workflow makes any chosen change.

The old callable name `distill-sessions` was replaced by `skill-retro`. The operational contract is in [SKILL.md](SKILL.md).

## How it works

1. `scripts/main.py` reads supported local session records and ranks observable friction. Its JSON goes to `top.json`; its human preview goes to stderr.
2. After explicit consent to send selected session-derived text, per-trajectory analysts produce classified Memory Items. The operator collects them in `merged.json`, preserving the source session and target skill.
3. `scripts/propose.py` produces a per-target proposal. Two distinct sessions promote a pattern; one session remains pending. Instruction items need a real SKILL.md section; integration items need a directly related source pointer and no invented section anchor.
4. Review the proposed outcome and hand chosen changes to a separate implementation workflow. The retrospective does not apply them.

See the [runtime protocol](references/runtime-protocol.md) for the collection schema and host-specific dispatch details.

## Installation

The skill ships with `loom-workflow`. Install the plugin through the `loom` marketplace:

```sh
# Claude Code
claude plugin marketplace add https://github.com/kouko/loom-plugins.git
claude plugin install loom-workflow@loom

# Codex
codex plugin marketplace add https://github.com/kouko/loom-plugins.git
codex plugin add loom-workflow@loom
```

After the release containing this rename is installed, invoke `loom-workflow:skill-retro` in Claude Code or ask Codex to use `skill-retro`. The old name is not a callable alias. The Python scripts use the standard library and require Python 3.11 or newer.

## Quick start

From the repository root, generate a local preview without sending session data to an analysis agent:

```sh
python3 loom-workflow/skills/skill-retro/scripts/main.py \
  --target-skill-pattern 'loom-code:*' > top.json
```

The ranked summary appears on stderr. After reviewing the target, explicitly approve which trajectories may be dispatched. Collect each analyst result into `merged.json` using the [runtime schema](references/runtime-protocol.md), then render a review artifact:

```sh
python3 loom-workflow/skills/skill-retro/scripts/propose.py \
  --input merged.json \
  --target-skill /path/to/target/SKILL.md \
  --output proposals.md
```

`propose.py` reads the target SKILL.md and writes only `proposals.md`. A missing integration source stays an investigation candidate outside `merged.json`; a single-session item remains pending.

For selected sessions, replace the discovery flag with `--target-skill plugin:skill --session ID` and repeat `--session` as needed. This exact operator target permits sessions without a recorded invocation and does not require target installation. Selection bypasses discovery minimum/count caps; absent IDs fail. One session still produces pending observations; two distinct sessions may promote a proposal. For isolated inputs supply `--project-root` and/or `--codex-root`; unspecified transcript roots are then excluded. Use `--facets-root` to bound facet lookup separately.

## Configuration

`main.py` accepts a partial JSON threshold file with `--config /path/to/thresholds.json`. The six supported thresholds and their meanings are in the [runtime protocol](references/runtime-protocol.md#configuration-meanings). The common command flags are:

- `--target-skill-pattern` (default `loom-code:*`)
- `--top-n` (default `5`)
- `--max-trajectories-per-skill` (default `5`, discovery session cap)
- `--project-root` (override the Claude project log root, mainly for tests)
- `--facets-root` (override the Claude `/insights` facet root, mainly for tests)

## License

This skill is part of the [loom-plugins](https://github.com/kouko/loom-plugins) repository under its [MIT license](https://github.com/kouko/loom-plugins/blob/main/LICENSE).

### Third-party attributions

The failure and success analyst prompts in `agents/` adapt [Trace2Skill](https://github.com/Qwen-Applications/Trace2Skill) ([paper](https://arxiv.org/abs/2603.25158)), published under Apache 2.0. Preserve the upstream attribution when redistributing those adaptations.
