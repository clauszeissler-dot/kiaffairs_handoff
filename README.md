![KI AffAIrs](docs/assets/ki-affairs-github-readme-banner.png)

# KI AffAIrs Handoff

Praktische Installationspakete für saubere Arbeitsübergaben in Coding-Agenten.
Sie helfen dabei, den Arbeitsstand vor einem Session-Ende oder einer
Context-Compaction nachvollziehbar zu sichern.

[Deutsche Anleitung](docs/guides/INSTALLATION.de.md) · [English guide](README.en.md)

## Für wen ist das?

Für Menschen und Teams, die länger mit Codex arbeiten und Entscheidungen,
Dateiänderungen, Prüfungen und nächste Schritte nicht im Chat verlieren wollen.
Die Pakete sind bewusst agentenspezifisch: Hooks und Installationsschritte von
Codex und Claude werden getrennt gepflegt.

## Schnellstart für Codex

1. Lade das aktuelle ZIP aus [codex/releases](codex/releases/) herunter.
2. Entpacke es und führe `python3 install.py` aus.
3. Wähle nur die Bausteine aus, die du verwenden möchtest.
4. Starte Codex neu und vertraue neue Hooks einmal über `/hooks`.

Die ausführliche Codex-Anleitung findest du in [Deutsch](codex/README.md) und
[Englisch](codex/README.en.md).

## Varianten

| Variante | Status | Zweck |
| --- | --- | --- |
| [Codex](codex/) | verfügbar | Interaktiver Installer, Handoff-Skill und optionaler Context-Snapshot |
| [Claude](claude/) | in Vorbereitung | Eigene Claude-Implementierung mit separater Anleitung und Releases |

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

Installationspakete für strukturierte Übergaben und Context-Schutz in
verschiedenen Coding-Agenten.

- [`codex/`](codex/) enthält die Codex-Variante mit interaktivem Installer.
- [`claude/`](claude/) ist für die gleichwertige Claude-Variante reserviert.

Jede Variante wird separat versioniert, damit die agentenspezifischen Hooks und
Installationsschritte klar voneinander getrennt bleiben.
