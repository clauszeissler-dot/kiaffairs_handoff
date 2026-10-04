# Codex Handoff

Download [ki-affairs-handoff-1.2.0.zip](releases/ki-affairs-handoff-1.2.0.zip).
Extract, run `python3 install.py` with Python 3.11+, restart Codex, review/trust hooks via `/hooks`.
Only Handoff is installed; no Engineering, Security, n8n or Insights modules.
For a deliberate upgrade review changes and run `python3 install.py --overwrite`.
Backups are kept beside replaced files. Review earlier manually configured hooks separately.

[Full instructions and acceptance test](handoff-package/README.md).
The old toolkit 1.1.0 has known installer path and TOML bugs and is not recommended.
A technical snapshot does not replace a verified full handoff, does not clear context,
and does not guarantee absence of context rot or drift.
