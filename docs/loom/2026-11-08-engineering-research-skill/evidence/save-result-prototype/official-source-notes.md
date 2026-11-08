# Native-host configuration references

Consulted 2026-11-08; verify actual behavior with a public-only local control before private fixtures.

- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference): restricted mode excludes command tools unless explicitly named, confines native file tools, and loads only managed/explicit settings. Safe mode disables custom MCP servers, so custom tool availability cannot be assumed there. Explicit --strict-mcp-config limits MCP sources; --settings applies only to the session.
- [Instruction and memory loading](https://code.claude.com/docs/en/memory): claudeMdExcludes matches absolute paths and covers instruction/rule exclusions; managed instructions require separate handling. The current built-in instructionFiles managed-only option excludes ordinary user/project instructions at launch, with on-demand descendants still requiring exclusion. Auto memory can be disabled. These are configuration claims, not measured isolation or permission to read private instructions.

Only official primary documentation supports these notes; third-party search results were not adopted. No global settings changes are proposed.
