# Installation and scope selection

Back to the [German start page](../../README.md) · [English overview](../../README.en.md)

1. Download the current Codex archive from [codex/releases](../../codex/releases/).
2. Extract the ZIP file.
3. Open a terminal in the extracted directory and run `python3 install.py`.
4. Answer each scope question. Press Enter to accept the shown default.
5. Restart Codex. Open `/hooks` and trust new hook definitions after reviewing
   them.

For automated installation, specify every selected component explicitly:

```sh
python3 install.py --yes --handoff --engineering
```

A remaining-context threshold also needs your model's context-window size:

```sh
python3 install.py --yes --handoff --configure-compaction \
  --context-window 272000 --remaining-context-percent 20
```

Installation files live under `~/.codex/`. Project snapshots are stored in each
project under `docs/handoffs/`.
