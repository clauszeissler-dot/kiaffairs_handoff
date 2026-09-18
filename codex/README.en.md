![KI AffAIrs](../docs/assets/ki-affairs-github-readme-banner.png)

# Codex Handoff

The Codex variant preserves important work information before context
compaction and supports complete handoffs when a session ends. It requires
Codex CLI 0.155.0 or later.

[Deutsche Anleitung](README.md) · [English guide](README.en.md) ·
[Release files](releases/)

## Install

Download the latest ZIP from [releases](releases/), extract it, and run this
inside the extracted directory:

```sh
python3 install.py
```

The installer asks for the scope before making changes. It never installs the
whole package by default.

## Available components

| Component | Purpose |
| --- | --- |
| Handoff protection | Handoff skill, session-end hook, and optional PreCompact snapshot |
| Engineering skills | Planning, testing, debugging, verification, and code review |
| Security skills | Security foundations and threat modeling |
| n8n skills | Support for n8n workflows |
| Agent profiles | Scout, Researcher, Worker, Reviewer, Advisor, and Orchestrator |
| Local Insights | Local Codex-session analysis; disabled by default |

The installer creates a timestamped backup before changing `hooks.json` or
`config.toml`. Existing toolkit files are not replaced unless you pass
`--overwrite`.

## Context snapshot with low remaining context

When you select handoff protection, the installer can configure an automatic
compaction threshold. It asks for your model's context-window size and desired
remaining percentage. For a 272,000-token window and 20% remaining context,
the threshold is 217,600 tokens.

The `PreCompact` hook writes a snapshot immediately before automatic
compaction to `docs/handoffs/AUTO_<timestamp>.md` in the active project. After
installation, restart Codex and review and trust the new hook once through
`/hooks`.

## Everyday use

For a deliberate handoff, use `/handoff` or finish with a clear phrase such as
“Ende für heute”. A complete handoff records decisions, changed files,
verification, and next steps. The automatic snapshot is a safety net, not a
replacement.

## Local data and limits

Handoffs are stored in each project under `docs/handoffs/`. Local Insights are
only installed when selected and remain disabled until Codex starts with
`CODEX_TOOLKIT_ENABLE_INSIGHTS=1`. Public research is disabled separately.

The hook can save the state of work, but it cannot write a complete semantic
handoff without a Codex run. Review handoffs and snapshots before relying on
them for critical work.

## Help and recovery

- Read the installer's output: it lists every installed or skipped file.
- If a hook does not run, open `/hooks` in Codex and check its trust status.
- Installer backups sit next to the changed configuration file and use the
  `.toolkit-backup-…` suffix.
- To reinstall, run the installer again with your chosen options; `--overwrite`
  only replaces toolkit files.

The package is provided without warranty.
