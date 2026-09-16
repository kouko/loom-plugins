# Locate `loom-code` and check the contract version

Step 0 of `capture-intent`, `write-spec`, `design-system` and
`product-principles` links here. "This SKILL.md" below is the SKILL.md whose
Step 0 sent you here; all four sit at the same depth.

The artifacts these skills write are defined by `loom-code`'s contract
package, so refuse to run against a version that does not declare them.

Plugins cannot read each other's files, so there is no
`${CLAUDE_PLUGIN_ROOT}` path that reaches `loom-code` from here. Find its
checkout on this host:

| Host | Where `loom-code` lives |
|---|---|
| Claude Code | the plugin cache — `~/.claude/plugins/cache/<marketplace>/loom-code/<version>/`, one directory per installed version; take the newest |
| Codex CLI, Antigravity CLI | on any other host: this plugin's root is the directory two levels above this SKILL.md, and if its parent directory is named `loom-design` (a versioned install) the root is that parent instead; the `loom-code` directory sits next to this plugin's root and it may contain one version subdirectory holding the plugin files — use the newest |

Then run, with that directory in place of `<loom-code>`:

```
python3 <loom-code>/scripts/loom_checker.py contract --require 2.1
```

Exit 0: continue. Anything else, the rule is `contract.requires`: print
what the checker printed, tell the user to update `loom-code`, and
**stop**. Do not work around it and do not guess a path.

If you cannot find the checkout, say so, stop, and either ask the user
where `loom-code` is installed or ask the user to install or update
`loom-code`; on Codex, ask for the install or update. On every host,
never create a repository-local copy of the checker.
