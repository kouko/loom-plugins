# Document locations in conversation

Use absolute paths for every local document location shared in conversation.
Resolve the actual document location from the active repository or worktree
and the file's location, including documents outside that root. Use absolute
Markdown link targets with short labels where local file links are supported.
Wrap targets containing spaces in angle brackets: `[name](<absolute-path>)`.
Use an absolute plain path when local links are unsupported. Never use
`file://` or a fixed developer home directory in conversation. Preserve
bundled resource references, stored relative paths and repository document
links; this rule changes conversation output only.
