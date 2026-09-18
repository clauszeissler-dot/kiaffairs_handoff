![KI AffAIrs](docs/assets/ki-affairs-github-readme-banner.png)

# KI AffAIrs Handoff

Practical installation packages for reliable handoffs in coding agents. They
help preserve a useful work record before a session ends or the context is
compacted.

[Deutsche Anleitung](README.md) · [English guide](docs/guides/INSTALLATION.en.md)

## Who is this for?

It is for people and teams who work with Codex over longer sessions and want to
retain decisions, changed files, verification results, and next steps outside
the chat. Each agent has its own implementation because hooks and installation
steps differ between Codex and Claude.

## Codex quick start

1. Download the latest ZIP from [codex/releases](codex/releases/).
2. Extract it and run `python3 install.py`.
3. Select only the components you want to use.
4. Restart Codex and review and trust newly added hooks through `/hooks`.

The complete Codex documentation is available in [German](codex/README.md)
and [English](codex/README.en.md).

## Variants

| Variant | Status | Purpose |
| --- | --- | --- |
| [Codex](codex/) | available | Interactive installer, handoff skill, and optional context snapshot |
| [Claude](claude/) | planned | Separate Claude implementation with its own guide and releases |

## What is preserved

The Codex handoff records decisions, changed files, verification, and concrete
next steps. The optional `PreCompact` hook also writes a minimal local state
snapshot to the current project's `docs/handoffs/` directory before automatic
context compaction.

## Important limits

- A snapshot is not a substitute for a deliberate, written handoff.
- Codex hooks must be reviewed and trusted once.
- Local Insights and public research remain disabled until you explicitly
  enable them.
- The package is provided without warranty. Review the selected scope before
  using it in production or regulated environments.

## License

This repository is licensed under the [GNU GPL v3](LICENSE).
