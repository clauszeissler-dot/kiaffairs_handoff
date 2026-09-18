# Installation und Auswahlumfang

[🇩🇪 Deutsche Startseite](../../README.md) · [🇬🇧 English version](INSTALLATION.en.md)

1. Lade die aktuelle Codex-Datei aus [codex/releases](../../codex/releases/) herunter.
2. Entpacke die ZIP-Datei.
3. Öffne ein Terminal im entpackten Ordner und starte `python3 install.py`.
4. Beantworte jede Umfangsfrage. Mit Enter übernimmst du die angezeigte
   Standardauswahl.
5. Starte Codex neu. Öffne `/hooks` und vertraue neue Hook-Definitionen nach
   Prüfung.

Du kannst die Auswahl auch für automatisierte Installationen explizit angeben:

```sh
python3 install.py --yes --handoff --engineering
```

Eine Restkontext-Schwelle benötigt zusätzlich das Kontextfenster deines
Modells:

```sh
python3 install.py --yes --handoff --configure-compaction \
  --context-window 272000 --remaining-context-percent 20
```

Die Installationsdateien liegen unter `~/.codex/`. Deine Projekt-Snapshots
liegen dagegen im jeweiligen Projekt unter `docs/handoffs/`.
