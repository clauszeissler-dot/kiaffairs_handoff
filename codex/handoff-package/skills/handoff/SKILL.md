---
name: handoff
description: Sichert vor einem Session-Ende oder einer bevorstehenden Context-Compaction den Arbeitsstand in einem strukturierten Handoff-Dokument. Verwenden bei "/handoff", "Kontext sichern", "Session-Übergabe" oder bei Abschlussformulierungen wie „wir machen morgen weiter“, „Ende für heute“ und „Gute Nacht“.
---

# Handoff

## Zweck

Erstelle vor einer Context-Compaction, `/clear` oder dem Ende einer Arbeits-Session ein belastbares, knappes Briefing auf der Festplatte. Das Handoff hält Entscheidungen, tatsächliche Änderungen, Verifikation und konkrete nächste Schritte fest; es ersetzt keinen Chat-Mitschnitt.

Schließe zuerst eine laufende atomare Aufgabe ab, soweit das sicher möglich ist. Beginne das Handoff früh genug, dass die wesentlichen Ergebnisse noch verfügbar sind.

## Erkennung eines Session-Endes

Führe den vollständigen Handoff-Ablauf aus, bevor du die abschließende Antwort sendest, wenn der User erkennbar die Arbeit für jetzt beendet oder auf einen späteren Zeitpunkt verschiebt. Das gilt auch ohne explizites `/handoff`, etwa bei:

- „wir machen morgen weiter“, „bis morgen“ oder „wir setzen später fort“
- „Ende für heute“, „für heute reicht es“ oder „Feierabend“
- „Gute Nacht“, „ich gehe schlafen“ oder vergleichbaren Verabschiedungen im Arbeitskontext

Entscheidend ist die erkennbare Absicht, die Session zu beenden oder zu pausieren, nicht die exakte Wortwahl. Bei einer bloßen Begrüßung oder beiläufigen Erwähnung ohne Abschlussabsicht kein Handoff erstellen.

## Ablage und Benennung

1. Bestimme den Projekt-Root mit `git rev-parse --show-toplevel`; außerhalb eines Git-Repositories verwende das aktuelle Arbeitsverzeichnis.
2. Lege das Dokument unter `docs/handoffs/` ab.
3. Verwende `YYYYMMDD_NN_kurzer-slug.md`. Ermittle `NN` aus den am selben Tag vorhandenen Dateien und erhöhe es. Beginne mit `01`.
4. Existiert im Projekt bereits eine eindeutig etablierte Handoff-Konvention, halte diese ein statt eine parallele Reihe zu eröffnen.

## Inhalt

Destilliere die gesamte relevante Session. Nimm Ergebnisse und begründete Entscheidungen auf, nicht Exploration, Fehlstarts oder einen Nachrichtentranskript.

```markdown
# Handoff — <Projekt oder Feature> — <YYYY-MM-DD>

## Was ist passiert
- Entscheidung und kurze Begründung
- Erreichte Ergebnisse

## Wo liegen die Dinge
- Geänderte oder angelegte Dateien mit Pfad und Zweck
- Relevante bestehende Dateien für die Fortsetzung
- Verweise auf bestehende CHANGELOG.md, TEST-LOG.md oder Projektdokumentation, falls zutreffend

## Verifikation
- Durchgeführte Prüfungen und Ergebnisse
- Ausdrücklich nicht geprüft oder noch unklar

## Git-Status
- Branch, letzter Commit-Hash, Push-Status (falls bekannt) und offene Änderungen

## Offene Folgeschritte
1. Konkreter, unmittelbar ausführbarer nächster Schritt
2. …

## Übergabe-Prompt für die nächste Session
> Lies docs/handoffs/<datei>.md und setze bei „Offene Folgeschritte“ fort.
```

## Qualitätsregeln

- Die Sektion **Verifikation** ist verpflichtend. Benenne Unsicherheiten und nicht ausgeführte Tests explizit.
- Verwende absolute Daten statt relativer Zeitangaben.
- Keine vertraulichen Sicherheitsdetails, Zugangsdaten oder Angriffswege aufnehmen. An vorhandene Projektstandards für Sanitization halten.
- Prüfe einmal kurz auf Vollständigkeit: Entscheidungen, betroffene Dateien und nächster Schritt müssen auffindbar sein. Danach abschließen, nicht polieren.

## Automatisches Sicherheitsnetz

`python3 scripts/snapshot.py` schreibt einen minimalen lokalen Git-Snapshot und verweist
auf eine vorhandene inhaltliche Übergabe. Kein Ersatz für diesen vollständigen Skill.
Ein vertrauter PreCompact-Hook kann ihn vor automatischer Compaction ausführen. Der
Installer kann bei bekannter tatsächlicher Kontextfenstergröße eine Schwelle bei 20 %
Restkontext setzen. Diese Schwelle ist keine wissenschaftliche Grenze für Context Rot.
Compaction ist kein automatisches Clear. Vor bewusstem Neustart die vollständige
Übergabe erfolgreich speichern und prüfen, danach in der neuen Session einlesen.
