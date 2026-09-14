#!/bin/bash
# Antigravity CLI (agy) PreToolUse adapter for the flat skill-folder rule.
#
# agy PostToolUse cannot block, so the check runs BEFORE the write, on the
# target path. The rule and its message stay in validate-skill-folder-structure.sh:
# this adapter rebuilds the target's shape (<skill>/SKILL.md + the target's
# parent directories) in a scratch copy and runs the original validator on it
# with a synthesised Claude-shaped payload, mapping exit 2 + stderr to deny.
#
# Why a scratch copy, not the real tree:
#   - pre-write, the nested directory does not exist yet, so a filesystem scan
#     of the real skill would miss it;
#   - only the target's own shape is judged, so a skill that already contains a
#     nested directory can still receive the flat writes that repair it;
#   - the validator runs outside any git repo, so its repo-level .claude copy
#     short-circuit cannot silence enforcement under agy (Claude Code only).
#
# stdin : {"toolCall":{"name":...,"args":{"TargetFile":...}}, "workspacePaths":[...], ...}
# stdout: {"decision":"allow"} or {"decision":"deny","reason":"..."}; exit 0 always.
# Unrecognised payloads are allowed — this is a structure lint, not a security gate.

HERE="$(cd "$(dirname "$0")" && pwd)"
VALIDATOR="$HERE/validate-skill-folder-structure.sh"

allow() { printf '{"decision":"allow"}\n'; exit 0; }

command -v jq >/dev/null 2>&1 || allow
INPUT=$(cat 2>/dev/null)

# TargetFile is agy 1.2.2's key for write_to_file / replace_file_content; the
# rest are defensive fallbacks. First non-empty string wins.
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '
  (.toolCall.args // {}) as $a
  | [$a.TargetFile, $a.AbsolutePath, $a.FilePath, $a.file_path, $a.path]
  | map(select(type == "string" and . != "")) | .[0] // empty' 2>/dev/null) || allow
[ -n "$FILE_PATH" ] || allow

case "$FILE_PATH" in
  /*) ;;
  *)
    WS=$(printf '%s' "$INPUT" | jq -r '.workspacePaths[0] // empty' 2>/dev/null)
    [ -n "$WS" ] || allow
    FILE_PATH="$WS/$FILE_PATH"
    ;;
esac

# Lexically normalise the absolute path (collapse '//', '.', '..') so the
# skill root and relative dir are derived from the path agy will really write,
# and so no '..' can steer the scratch mirror outside its directory.
normalise() {
  local rest="${1#/}" seg out=""
  while [ -n "$rest" ]; do
    case "$rest" in
      */*) seg="${rest%%/*}"; rest="${rest#*/}" ;;
      *)   seg="$rest"; rest="" ;;
    esac
    case "$seg" in
      ''|.) ;;
      ..) out="${out%/*}" ;;
      *)  out="$out/$seg" ;;
    esac
  done
  printf '%s' "${out:-/}"
}
FILE_PATH=$(normalise "$FILE_PATH")

# Same skill-root detection as the validator: <...>/skills/<name> with SKILL.md.
case "$FILE_PATH" in */skills/*) ;; *) allow ;; esac
SKILL_ROOT=$(printf '%s' "$FILE_PATH" | sed -E 's|(.*/skills/[^/]+).*|\1|')
[ -f "$SKILL_ROOT/SKILL.md" ] || allow
REL="${FILE_PATH#"$SKILL_ROOT"/}"
[ "$REL" != "$FILE_PATH" ] || allow
REL_DIR=$(dirname "$REL")
# Defence in depth: after normalisation REL has no '..' segment; if one ever
# appears, allow without mirroring rather than create anything outside scratch.
case "/$REL/" in */../*) allow ;; esac

SCRATCH=$(mktemp -d "${TMPDIR:-/tmp}/agy-skill-folder.XXXXXX") || allow
trap 'rm -rf "$SCRATCH"' EXIT
MIRROR="$SCRATCH/skills/$(basename "$SKILL_ROOT")"
mkdir -p "$MIRROR" && : > "$MIRROR/SKILL.md" || allow
if [ "$REL_DIR" != "." ]; then
  mkdir -p "$MIRROR/$REL_DIR" || allow
fi

STDIN_JSON=$(jq -cn --arg p "$MIRROR/$REL" '{tool_input:{file_path:$p}}')
ERR=$(cd "$SCRATCH" && printf '%s' "$STDIN_JSON" | GIT_CEILING_DIRECTORIES="$SCRATCH" bash "$VALIDATOR" 2>&1 >/dev/null)
CODE=$?

if [ "$CODE" -eq 2 ]; then
  REASON=${ERR//"$MIRROR"/"$SKILL_ROOT"}
  jq -cn --arg r "$REASON" '{decision:"deny", reason:$r}'
  exit 0
fi
allow
