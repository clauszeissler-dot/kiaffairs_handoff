![KI AffAIrs](docs/assets/ki-affairs-github-readme-banner.png)

# KI AffAIrs Handoff

Praktische Installationspakete für saubere Arbeitsübergaben in Coding-Agenten.
Sie helfen dabei, den Arbeitsstand vor einem Session-Ende oder einer
Context-Compaction nachvollziehbar zu sichern.

[🇩🇪 Deutsche Anleitung](docs/guides/INSTALLATION.de.md) · [🇬🇧 English guide](README.en.md)

## Für wen ist das?

Für Menschen und Teams, die länger mit Codex arbeiten und Entscheidungen,
Dateiänderungen, Prüfungen und nächste Schritte nicht im Chat verlieren wollen.
Die Pakete sind bewusst agentenspezifisch: Hooks und Installationsschritte von
Codex und Claude werden getrennt gepflegt.

## Schnellstart für Codex

1. Lade [ki-affairs-handoff-1.2.0.zip](codex/releases/ki-affairs-handoff-1.2.0.zip).
2. Entpacke es und führe `python3 install.py` aus (Python 3.11 oder neuer).
3. Starte Codex neu und prüfe/vertraue die Hooks über `/hooks`.
4. Führe den [Funktionstest](codex/handoff-package/README.md) in einem harmlosen Projekt aus.

Nur Handoff wird installiert. [Anleitung und Upgrade](codex/README.md).
Die alte 1.1.0-Datei bleibt als historischer Stand erhalten, ist aber keine aktuelle Empfehlung.

## Varianten

| Variante | Status | Zweck |
| --- | --- | --- |
| [Codex](codex/) | verfügbar | Kleiner Installer, Handoff-Skill und lokaler Context-Snapshot |
| [Claude](claude/) | verfügbar | Handoff-Skill, `PreCompact`/`SessionEnd`-Hooks und optionaler Formulierungs-Nudge, installierbar über `bash claude/install.sh` |

## Was gesichert wird

Der Codex-Handoff beschreibt Entscheidungen, geänderte Dateien, Verifikation
und konkrete nächste Schritte. Der optionale `PreCompact`-Hook schreibt vor
einer automatischen Context-Compaction zusätzlich einen minimalen lokalen
Zustands-Snapshot in `docs/handoffs/` des aktuellen Projekts.

## Wichtige Grenzen

- Ein Snapshot ersetzt kein bewusst erstelltes, inhaltliches Handoff.
- Hooks müssen in Codex einmal geprüft und vertraut werden.
- Lokale Insights und öffentliche Recherche bleiben deaktiviert, bis du sie
  ausdrücklich einschaltest.
- Das Paket wird ohne Gewähr bereitgestellt; prüfe die Auswahl vor dem Einsatz
  in produktiven oder regulierten Umgebungen.

## Lizenz

Dieses Repository steht unter der [GNU GPL v3](LICENSE).
