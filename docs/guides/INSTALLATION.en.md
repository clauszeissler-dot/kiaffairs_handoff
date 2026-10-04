# Installation · KI AffAIrs Handoff 1.2.0

[Download: ki-affairs-handoff-1.2.0.zip](../../codex/releases/ki-affairs-handoff-1.2.0.zip).
Requires Python 3.11+, macOS/Linux. Extract and run `python3 install.py`.
Only Handoff is installed. Restart Codex, review and trust hooks via `/hooks`.

For different existing files: review changes and deliberately run `python3 install.py --overwrite`.
Replaced files are backed up. Review older manually configured hooks separately.
Do not use old `--handoff --engineering` arguments.

[Instructions, threshold and acceptance test](../../codex/handoff-package/README.md).
A snapshot is not a full handoff. Save and verify the full handoff before starting a fresh session.
Legacy 1.1.0 is historical and is not the current recommendation.
