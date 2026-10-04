# KI AffAIrs Handoff

Current Codex download: [ki-affairs-handoff-1.2.0.zip](codex/releases/ki-affairs-handoff-1.2.0.zip).
Python 3.11+, macOS/Linux. Extract and run `python3 install.py`; restart Codex and review/trust hooks via `/hooks`.

Only Handoff is installed: full handoff skill, local snapshot, session-end reminder.
[Instructions](codex/handoff-package/README.md) · [German guide](docs/guides/INSTALLATION.de.md).
For an intentional upgrade of existing different files, review the changes and use
`python3 install.py --overwrite`. Existing files are backed up before replacement.
Legacy 1.1.0 is retained for history and is not the current recommendation.

A snapshot is not a full semantic handoff. The optional threshold configures compaction;
it does not clear context automatically or guarantee error-free model responses.
Write and verify a full handoff before a fresh session.
The separate Claude variant is legacy and not covered by the 1.2.0 Codex test report.
GNU GPL v3.
