---
name: handoff
description: Creates a structured HANDOFF.md BEFORE a context compaction or session end that preserves full working context. Triggers: "/handoff", "save context", "capture before compact", "session handoff", ctx display above ~20%, a closing statement like "that's it for today" or "good night", or when a session is marked complete. NEVER wait for the built-in compaction or freehand a handoff text — always use this skill so structure and depth stay consistent.
metadata:
  author: Claus Zeißler
  version: 1.0.0
  license: GPL-3.0
---

# Handoff Skill

## Purpose

The built-in `/compact` summary is lossy and its prompt is not steerable. This
skill INSTEAD writes a structured `HANDOFF.md` to disk BEFORE compaction or a
session ends. The file lives outside the context window and survives any
compaction or a `/clear`.

Rule of thumb: trigger at roughly 20% context usage — not only at the system
warning. From 25–30% signal quality already drops noticeably, and the skill
itself still needs room to distill the session cleanly.

## Recognizing a session end

Run the full handoff procedure before your final reply whenever the user
clearly ends the session or defers it, even without an explicit `/handoff`.
That includes closing statements such as:

- "that's it for today", "we'll continue tomorrow", "see you tomorrow"
- "good night", "I'm calling it for now"
- German equivalents: "Ende für heute", "Feierabend", "Gute Nacht", "bis morgen"

What matters is the recognizable intent to end or pause the session, not the
exact wording. Don't write a handoff for a casual greeting or an offhand
mention with no closing intent.

## Procedure

1. Finish the current micro-task (don't abort mid-step).
2. Determine the target folder: default is `docs/handoffs/` in the project
   root (found via `git rev-parse --show-toplevel`; use the current working
   directory outside a git repo). If files matching `YYYYMMDD_NN_slug.md`
   already exist there, continue the running numbering. If the folder is
   empty, start at `01`.
3. Go through the entire session (not just the last few messages) and distill
   it — don't transcribe. Abandoned dead ends, already-resolved errors, and
   intermediate exploration do NOT belong in the document, only the outcome.
4. Write `HANDOFF.md` (or the numbered file) following the schema below.
5. Proofread briefly (~30 seconds): are decisions, changed files, and the
   next step in there? Then done — don't over-polish.
6. Only then run `/compact` or `/clear`. If a compact-instructions block
   exists in CLAUDE.md, also point it to the handoff document's path (e.g.
   "Focus on the HANDOFF under docs/handoffs/..., current git diff, next
   step").

## Structure of HANDOFF.md

```markdown
# Handoff — <Project/Feature> — <Date, absolute, no "yesterday">

## What happened
- Key decisions of this session (with brief reasoning, not just "what")
- Results achieved

## Where things live
- Changed/created files with path
- Relevant existing files that matter for the next step
- Reference to CHANGELOG.md / TEST-LOG.md / CLAUDE.md if entries already
  exist there (don't duplicate, just reference)

## Verification
- What was tested and passed
- What was EXPLICITLY NOT tested or verified (this section is the honesty
  brake — better too much than too little, so the next session doesn't
  treat something as done that only looks that way)

## Git status
- Branch, last commit hash, pushed yes/no, open changes (git status short
  form)

## Open next steps
1. Numbered, concrete, immediately actionable
2. ...

## Handoff prompt for the next session
> Read docs/handoffs/<file>.md and continue from "Open next steps".
```

## Rules

- Distill, don't log. A handoff is a briefing, not a session transcript.
- The verification section is mandatory, even when it's uncomfortable
  ("Feature X was built but NOT tested against real data").
- No security details or attack vectors in plain text — sanitize, full
  detail only internally, consistent with any existing project standard for
  CHANGELOG.md/TEST-LOG.md.
- Always translate relative time references ("just now", "earlier") into
  absolute time/date, so the document is still useful in a week.
- A running session series (`01`, `02`, `03`, ...) in one folder is
  preferable to a single overwritten `HANDOFF.md` once a project runs over
  several days — this also produces a traceable session log as a side
  effect.

## Safety net: PreCompact + SessionEnd hooks (mechanical backstop)

The manual trigger above depends on the model noticing — that is not
mechanically enforced. Two hooks close the biggest part of that gap by
writing a minimal handoff (git status + last commit + branch, ~30 lines)
automatically, regardless of whether the model remembers:

- `PreCompact` (no matcher — fires on both `manual` and `auto` compaction)
- `SessionEnd` (no matcher — fires on `clear`/`resume`/`logout`/`other`)

Both call `hooks/auto-handoff-safety-net.sh <tag>` and write to
`docs/handoffs/AUTO_<tag>_<timestamp>.md`, anchored at the git project root
(via `git rev-parse --show-toplevel`, not the raw cwd, which may have moved
via `cd` during the session) — falls back to cwd outside a git repo.

Two noise guards keep this from littering `docs/handoffs/` on every
`/clear`: it skips when the git tree is clean (nothing new since the last
commit message), and it skips when the same directory already got a
snapshot in the last 2 minutes (back-to-back clear/resume cycles).

These two hooks guarantee only that *some* minimal snapshot exists after
every compaction and every session end — they don't replace the full skill
run. Claude Code has no hook event that reports remaining context
percentage, so the "call the skill at ~20% context" half of the trigger
still depends on the model noticing on its own.

## Optional: session-end phrase nudge (closes the noticing gap)

`hooks/session-end-phrase-nudge.py`, registered on `UserPromptSubmit`,
detects a closing statement (see "Recognizing a session end" above) in the
user's own message and injects a directive telling Claude to run this skill
in full BEFORE its final reply — instead of relying on Claude to notice
that the session is ending. It also fires the safety-net snapshot
immediately as a floor. This is the same technique used by the equivalent
Codex CLI nudge hook (also part of this repo, see `../codex/`); see
`install.sh` to enable it.

## Installation

See `install.sh` for a non-interactive install, or ask an agent running
this skill to "install the handoff safety net" — it should then use
`AskUserQuestion` (or an equivalent prompt) to ask:

1. **Scope** — user-level (`~/.claude/settings.json`, all projects) or
   project-level (`.claude/settings.json`, this repo only)?
2. **Which hooks** — `PreCompact` only, `SessionEnd` only, or both
   (recommended)?
3. **Session-end phrase nudge** — enable the optional `UserPromptSubmit`
   nudge above (recommended if the model routinely forgets to call this
   skill on its own)?
4. **Noise guards** — keep the clean-tree-skip and 2-minute throttle
   (recommended), or disable for debugging?

Then: copy `hooks/*.sh` (and `hooks/session-end-phrase-nudge.py` if chosen)
into `~/.claude/hooks/` or `.claude/hooks/`, `chmod +x` them, and merge (not
overwrite) the corresponding entries into the target `settings.json`'s
`hooks` object — see `install.sh` for the exact JSON shape and a safe `jq`-
based merge.

### Optional tuning: trigger compaction earlier

Claude Code exposes `autoCompactWindow` in `settings.json` (a token count
between 100000 and 1000000) to make auto-compaction happen earlier in a long
session — indirectly making the `PreCompact` safety net fire more often
without needing a "context percentage" signal that doesn't exist as a hook.
