#!/usr/bin/env bash
# Interactive installer for the Claude Code "handoff safety net":
# a PreCompact and/or SessionEnd hook that writes a minimal git-snapshot
# handoff automatically, plus an optional session-end phrase nudge.
#
# Safe to re-run: it merges into settings.json (never overwrites existing
# hooks) and skips a hook entry that is already present.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Handoff Safety Net — Claude Code installer"
echo "==========================================="
echo

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required to safely merge hook entries into settings.json but was not found."
  echo "Install it (e.g. 'brew install jq' on macOS, 'apt install jq' on Debian/Ubuntu) and re-run this script."
  exit 1
fi

# 1. Scope
echo "Where should this be installed?"
echo "  1) User level  (~/.claude/settings.json — all your projects)"
echo "  2) Project level (./.claude/settings.json — this repo only)"
read -r -p "Choice [1]: " scope_choice
scope_choice="${scope_choice:-1}"
if [ "${scope_choice}" = "2" ]; then
  TARGET_DIR="./.claude"
  TARGET_SETTINGS="${TARGET_DIR}/settings.json"
  HOOKS_DIR="${TARGET_DIR}/hooks"
else
  TARGET_DIR="${HOME}/.claude"
  TARGET_SETTINGS="${TARGET_DIR}/settings.json"
  HOOKS_DIR="${TARGET_DIR}/hooks"
fi
echo "-> ${TARGET_SETTINGS}"
echo

# 2. Which hooks
echo "Which hooks should write the minimal safety-net snapshot?"
echo "  1) PreCompact only (before /compact or auto-compaction)"
echo "  2) SessionEnd only (session ends: /clear, resume, logout, other)"
echo "  3) Both (recommended)"
read -r -p "Choice [3]: " hook_choice
hook_choice="${hook_choice:-3}"
INSTALL_PRECOMPACT=false
INSTALL_SESSIONEND=false
case "${hook_choice}" in
  1) INSTALL_PRECOMPACT=true ;;
  2) INSTALL_SESSIONEND=true ;;
  *) INSTALL_PRECOMPACT=true; INSTALL_SESSIONEND=true ;;
esac
echo

# 3. Session-end phrase nudge
read -r -p "Also install the session-end phrase nudge (UserPromptSubmit — recommended if the model tends to forget to run the handoff skill on its own)? [Y/n]: " nudge_choice
nudge_choice="${nudge_choice:-Y}"
INSTALL_NUDGE=false
[[ "${nudge_choice}" =~ ^[Yy]$ ]] && INSTALL_NUDGE=true
echo

mkdir -p "${HOOKS_DIR}"
cp "${SCRIPT_DIR}/hooks/auto-handoff-safety-net.sh" "${HOOKS_DIR}/auto-handoff-safety-net.sh"
chmod +x "${HOOKS_DIR}/auto-handoff-safety-net.sh"
SAFETY_NET_CMD="\"${HOOKS_DIR}/auto-handoff-safety-net.sh\""

if [ "${INSTALL_NUDGE}" = true ]; then
  cp "${SCRIPT_DIR}/hooks/session-end-phrase-nudge.py" "${HOOKS_DIR}/session-end-phrase-nudge.py"
  chmod +x "${HOOKS_DIR}/session-end-phrase-nudge.py"
fi

[ -f "${TARGET_SETTINGS}" ] || { mkdir -p "${TARGET_DIR}"; echo '{}' > "${TARGET_SETTINGS}"; }

TMP_SETTINGS="$(mktemp)"
cp "${TARGET_SETTINGS}" "${TMP_SETTINGS}"

add_hook_entry() {
  local event="$1" command="$2" timeout="$3" status_message="$4"
  jq --arg event "${event}" --arg command "${command}" --argjson timeout "${timeout}" --arg status "${status_message}" '
    .hooks[$event] //= [] |
    if ([.hooks[$event][].hooks[]?.command] | index($command)) then .
    else .hooks[$event] += [{"hooks": [{"type": "command", "command": $command, "timeout": $timeout, "statusMessage": $status}]}]
    end
  ' "${TMP_SETTINGS}" > "${TMP_SETTINGS}.next"
  mv "${TMP_SETTINGS}.next" "${TMP_SETTINGS}"
}

if [ "${INSTALL_PRECOMPACT}" = true ]; then
  add_hook_entry "PreCompact" "${SAFETY_NET_CMD} precompact 2>/dev/null || true" 15 "Handoff safety net (PreCompact)"
fi
if [ "${INSTALL_SESSIONEND}" = true ]; then
  add_hook_entry "SessionEnd" "${SAFETY_NET_CMD} sessionend 2>/dev/null || true" 10 "Handoff safety net (SessionEnd)"
fi
if [ "${INSTALL_NUDGE}" = true ]; then
  add_hook_entry "UserPromptSubmit" "python3 \"${HOOKS_DIR}/session-end-phrase-nudge.py\" 2>/dev/null || true" 15 "Session-end phrase nudge"
fi

jq empty "${TMP_SETTINGS}"  # fail loudly if the merge produced invalid JSON
cp "${TMP_SETTINGS}" "${TARGET_SETTINGS}"
rm -f "${TMP_SETTINGS}"

echo "Done. Installed into ${TARGET_SETTINGS}:"
[ "${INSTALL_PRECOMPACT}" = true ] && echo "  - PreCompact hook"
[ "${INSTALL_SESSIONEND}" = true ] && echo "  - SessionEnd hook"
[ "${INSTALL_NUDGE}" = true ] && echo "  - UserPromptSubmit session-end phrase nudge"
echo
echo "Also copy claude/SKILL.md to ~/.claude/skills/handoff/SKILL.md (or"
echo ".claude/skills/handoff/SKILL.md for a project-level skill) so the model"
echo "has the full handoff procedure to run when a hook nudges it."
echo
echo "Restart Claude Code (or open /hooks once) for the new hooks to be picked up."
