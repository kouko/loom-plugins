# Document locations in conversation

When delivering a local document, provide its actual absolute location in the
active project or worktree, including files outside that root. Where local
Markdown links are known to be supported, use the document's project-relative
path as the link text (or its filename for an external document) and an
absolute target; wrap targets containing spaces in angle brackets. When support
is unknown or unsupported, show the full absolute path. Preserve portable references inside files,
including bundled resource references, stored relative paths and repository
document links. Leave incidental filename mentions and quoted source examples
unchanged; apply this rule to copyable document deliveries.
