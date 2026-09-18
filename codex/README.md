![KI AffAIrs](../docs/assets/ki-affairs-github-readme-banner.png)

# Codex-Handoff

Die Codex-Variante sichert wichtige Arbeitsinformationen vor einer
Context-Compaction und unterstützt vollständige Übergaben beim Session-Ende.
Sie ist für Codex CLI ab Version 0.155.0 gedacht.

[Deutsche Anleitung](README.md) · [English guide](README.en.md) ·
[Release-Dateien](releases/)

## Installieren

Lade die aktuelle ZIP-Datei aus [releases](releases/) herunter, entpacke sie
und starte im entpackten Ordner:

```sh
python3 install.py
```

Der Installer fragt dich vor jeder Änderung nach dem Umfang. Er installiert
nicht automatisch das gesamte Paket.

## Was du auswählen kannst

| Baustein | Nutzen |
| --- | --- |
| Handoff-Schutz | Handoff-Skill, Session-Ende-Hook und optionaler PreCompact-Snapshot |
| Engineering-Skills | Planung, Tests, Debugging, Verifikation und Code-Review |
| Security-Skills | Grundlagen und Threat Modeling |
| n8n-Skills | Unterstützung für n8n-Workflows |
| Rollenprofile | Scout, Researcher, Worker, Reviewer, Advisor und Orchestrator |
| Lokale Insights | Lokale Auswertung von Codex-Sessions; standardmäßig deaktiviert |

Vor einer Änderung von `hooks.json` oder `config.toml` erstellt der Installer
eine zeitgestempelte Sicherung. Bereits vorhandene Toolkit-Dateien werden ohne
`--overwrite` nicht ersetzt.

## Context-Snapshot bei wenig Restkontext

Wenn du den Handoff-Schutz auswählst, kann der Installer eine automatische
Compaction-Schwelle setzen. Er fragt dafür nach der Größe des Kontextfensters
deines Modells und dem gewünschten Restkontext. Bei einem 272.000-Token-Fenster
und 20 % Restkontext setzt er die Schwelle auf 217.600 Tokens.

Der `PreCompact`-Hook schreibt unmittelbar vor einer automatischen Compaction
einen Snapshot nach `docs/handoffs/AUTO_<Zeitstempel>.md` im aktuellen Projekt.
Nach der Installation musst du Codex neu starten und den neuen Hook über
`/hooks` einmal prüfen und vertrauen.

## Normal verwenden

Für eine bewusste Übergabe verwende `/handoff` oder beende die Arbeit mit einer
klaren Formulierung wie „Ende für heute“. Das vollständige Handoff enthält
Entscheidungen, geänderte Dateien, Verifikation und nächste Schritte. Der
automatische Snapshot dient als Sicherheitsnetz, nicht als Ersatz dafür.

## Lokale Daten und Grenzen

Das Handoff liegt im jeweiligen Projekt unter `docs/handoffs/`. Lokale Insights
werden erst nach Auswahl installiert und bleiben deaktiviert, bis Codex mit
`CODEX_TOOLKIT_ENABLE_INSIGHTS=1` gestartet wird. Öffentliche Recherche bleibt
separat deaktiviert.

Der Hook kann einen Arbeitsstand sichern, aber keine vollständige inhaltliche
Übergabe ohne einen Codex-Lauf formulieren. Prüfe daher Handoffs und Snapshots,
bevor du dich auf sie für kritische Arbeiten verlässt.

## Hilfe und Wiederherstellung

- Lies nach einer Installation die Ausgabe des Installers; sie nennt jede
  installierte oder übersprungene Datei.
- Falls ein Hook nicht läuft, öffne in Codex `/hooks` und prüfe dessen
  Vertrauensstatus.
- Die Sicherungen des Installers liegen neben der geänderten Konfigurationsdatei
  und tragen den Zusatz `.toolkit-backup-…`.
- Für eine vollständige Neuinstallation kannst du den Installer erneut mit den
  gewünschten Optionen starten; `--overwrite` ersetzt nur Toolkit-Dateien.

Das Paket wird ohne Gewähr bereitgestellt.
