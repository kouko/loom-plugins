change_id: 2026-09-19-publication-hook-false-positives
kind: engineering
needs-design: no
publication: automatic — authorized 2026-09-19 by kouko
status: confirmed 2026-09-19

## Problem
The publication hook has false positives for heredoc carve-out cases. Specifically:
1. Commands like `cat <<EOF | bash` were incorrectly identified as not containing a merge when they actually do
2. The shell detection logic for `-c` flags was incomplete, missing cases like `bash -cl`
3. Heredoc body execution detection was too narrow, only checking the command word instead of the full pipeline

## Proposed outcome
Fix the publication hook's shell command recognition to correctly identify merge/push commands in heredoc pipelines and improve the `_shell_c_argument` function to properly detect shell commands with bundled flags.

## Acceptance
1. The hook correctly identifies `cat <<EOF | bash\nMERGE\nEOF` as containing a merge command
2. The hook correctly identifies shell commands with bundled short options like `-lc`, `-euxc`, `-cl`
3. Heredoc body execution detection considers the full pipeline, not just the command word
4. Existing true positives (direct pushes, etc.) continue to be recognized
5. Adversarial tests for heredoc carve-out pass

## Constraints
- Only modify shell command recognition logic in publication hook
- Do not change the fundamental push/merge recognition rules
- Preserve all existing true positive detections
- Focus on fixing false negatives in heredoc and shell flag parsing

## Open questions
- none