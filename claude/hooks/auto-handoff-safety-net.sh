#!/usr/bin/env bash
# Auto-handoff safety net for the handoff skill.
#
# Registered from TWO hook points in ~/.claude/settings.json:
#   - PreCompact  (before /compact or auto-compaction)
#   - SessionEnd  (session terminates: /clear, resume, logout, other)
#
# The handoff SKILL.md promises coverage for both "before compaction" and
# "session end" — but a skill can only fire if the model remembers to call
# it. This script is the mechanical backstop for the case where it forgot.
# It writes a minimal handoff (~50 lines: git status + last commit + branch
# + recently changed files) to docs/handoffs/AUTO_<TAG>_<timestamp>.md,
# anchored at the git project root (not the raw cwd, which may have moved
# via `cd` during the session). Does not replace a full /handoff run.

set -uo pipefail

TAG="${1:-UNKNOWN}"
TS="$(date +%Y%m%d_%H%M%S)"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT_DIR="${ROOT}/docs/handoffs"
OUT_FILE="${OUT_DIR}/AUTO_${TAG}_${TS}.md"
IN_GIT_REPO="$(git rev-parse --is-inside-work-tree 2>/dev/null || echo false)"

# Noise guard 1: nothing to report. A clean tree + a recent commit means the
# last commit message already documents the state — a fresh empty snapshot
# on every /clear adds no information, just clutter in docs/handoffs/.
if [ "${IN_GIT_REPO}" = "true" ] && [ -z "$(git status --short 2>/dev/null)" ]; then
  echo "Auto-Handoff uebersprungen (sauberer Git-Status, nichts Neues): ${TAG}"
  exit 0
fi

# Noise guard 2: throttle. Back-to-back /clear + resume cycles would otherwise
# write duplicate snapshots seconds apart.
if [ -d "${OUT_DIR}" ]; then
  LATEST="$(find "${OUT_DIR}" -maxdepth 1 -name 'AUTO_*.md' -newermt '-2 minutes' 2>/dev/null | head -1)"
  if [ -n "${LATEST}" ]; then
    echo "Auto-Handoff uebersprungen (< 2 Min. seit letztem Snapshot): ${LATEST}"
    exit 0
  fi
fi

mkdir -p "${OUT_DIR}" 2>/dev/null || exit 0

{
  echo "# Auto-Handoff (${TAG} safety net) — ${TS}"
  echo
  echo "> Minimal snapshot, generated automatically. Not a substitute for a full /handoff run."
  echo
  echo "## Git status"
  echo '```'
  git status --short 2>/dev/null || echo "(no git repo or git unavailable)"
  echo '```'
  echo
  echo "## Last commit"
  echo '```'
  git log -1 --oneline 2>/dev/null || echo "(no commit found)"
  echo '```'
  echo
  echo "## Branch"
  echo '```'
  git branch --show-current 2>/dev/null || echo "(unknown)"
  echo '```'
  echo
  echo "## Recently changed files (last commit)"
  echo '```'
  git diff --name-only HEAD~1 2>/dev/null | head -20 || echo "(no comparison possible)"
  echo '```'
} > "${OUT_FILE}" 2>/dev/null

echo "Auto-Handoff geschrieben: ${OUT_FILE}"
