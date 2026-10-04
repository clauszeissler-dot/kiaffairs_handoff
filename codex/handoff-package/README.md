# KI AffAIrs Handoff · kleines Codex-Paket

Version 1.2.0 · Python 3.11 oder neuer · macOS/Linux · Codex CLI ab 0.155.0.
Der Quellstand wurde mit Codex CLI 0.160.0 und dem offiziellen Konfigurationsschema geprüft.

## Installation

Im entpackten Paket `python3 install.py` ausführen. Es werden ausschließlich der
Handoff-Skill, der Snapshot und der Abschluss-Hinweis installiert. Codex danach neu
starten und die beiden Hooks über `/hooks` prüfen und vertrauen.

Optional eine Schwelle konfigurieren, wenn die tatsächliche Fenstergröße bekannt ist:

```sh
python3 install.py --configure-compaction --context-window 272000 --remaining-context-percent 20
```

272000 ist ein Rechenbeispiel, keine Vorgabe für jedes Modell. Bestehende root- und
profilbezogene Einstellungen prüfen; explizite Profil- oder CLI-Werte können die
Root-Schwelle übersteuern. Bestehende Root-Schwellen bleiben ohne `--overwrite` erhalten.
Vorhandene abweichende Skill-/Hook-Dateien werden ohne `--overwrite` nicht ersetzt.
Vor Ersetzung wird eine datierte Sicherung angelegt.

## Bewusste Übergabe

1. `/handoff` ausführen und die gespeicherte Datei prüfen: Ziel, gültige Entscheidungen,
   Dateien und Belege, tatsächlich durchgeführte Prüfungen, offene Schritte.
2. Erst nach erfolgreicher Speicherung und Prüfung eine frische Session öffnen.
3. Ihr den Pfad geben: „Lies docs/handoffs/<Datei>.md und setze bei den offenen Schritten fort.“
4. Die erste Fortsetzung an der gültigen Entscheidung und dem nächsten Schritt prüfen.

Keine Datei geschrieben? Kein Neustart. Eine Übergabe ist nur so gut wie ihr geprüfter Inhalt.
Der Abschluss-Hook erinnert bei einer eindeutigen Abschlussnachricht an das vollständige Handoff;
er kann die Ausführung durch das Modell nicht erzwingen.

## Was automatisch passiert

Vor einer automatischen Compaction schreibt der vertrauenswürdige PreCompact-Hook einen
lokalen Snapshot mit Git-Status, Branch, letztem Commit und Verweis auf die neueste
inhaltliche Übergabe. Er nutzt das Projekt aus der Hook-Eingabe. Ohne Git bleibt er
im angegebenen Arbeitsverzeichnis. Er lädt keine Transkripte hoch und ruft kein Modell auf.

Die optionale 20-Prozent-Einstellung konfiguriert Compaction, keine automatische `/clear`-Kette.
Die Schwelle ist ein Arbeitsparameter, keine Forschungsgrenze für Context Rot. Der Snapshot
ersetzt kein vollständiges Handoff. Kein Versprechen fehlerfreier Modellantworten.

## Eigener Funktionstest

Nach Installation und Hook-Freigabe:

1. Ein harmloses Testprojekt anlegen; Entscheidung „Ausgabe blau, Vorschlag rot ersetzt“ festhalten.
2. `/handoff` schreiben lassen und die Entscheidung in der Datei kontrollieren.
3. Neue Session mit genau dieser Übergabe starten; Farbe und offenen Schritt abfragen.
4. Snapshot separat prüfen: `printf '%s' '{"cwd":"/absoluter/testprojekt-pfad"}' | python3 ~/.codex/skills/handoff/scripts/snapshot.py`.
5. Bei der ersten tatsächlichen automatischen Compaction prüfen, ob eine `AUTO_*.md` entstanden ist.

Die automatisierten Pakettests prüfen Installer und Hook-Skripte. Die reale Hook-Dispatch-
Freigabe und Modellantworten in der eigenen Agenteninstallation bleiben ein eigener Abnahmeschritt.

## Wiederherstellung und Lizenz

Backups liegen neben der ersetzten Datei mit `.handoff-backup-<Zeitstempel>`.
Nur die installierten Handoff-Dateien und die dazugehörigen Hook-Einträge entfernen;
fremde Hooks erhalten. GNU GPL v3; siehe LICENSE.
