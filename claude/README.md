![KI AffAIrs](../docs/assets/ki-affairs-github-readme-banner.png)

# Claude-Variante

Handoff-Skill plus `PreCompact`/`SessionEnd`-Hooks für Claude Code, damit ein
strukturiertes Übergabe-Dokument geschrieben wird, bevor Kontext durch
Compaction oder Session-Ende verloren geht.

[🇩🇪 Deutsche Startseite](../README.md) · [🇬🇧 English overview](../README.en.md)

## Schnellstart

```bash
bash install.sh
```

Das Skript fragt interaktiv den Umfang ab (welche Hooks, ob der optionale
Formulierungs-Nudge installiert werden soll) und merged sicher in die
bestehende `settings.json` — nichts wird überschrieben, ein zweiter Lauf
erzeugt keine doppelten Einträge. Voraussetzung: `jq`.

## Was installiert wird

- **`PreCompact`-Hook** — schreibt vor jeder Context-Compaction (manuell
  oder automatisch) einen minimalen Git-Snapshot.
- **`SessionEnd`-Hook** — dasselbe, ausgelöst wenn die Session endet
  (`/clear`, Logout, u.a.) — deckt den Fall ab, in dem nie compactet wird.
- **Formulierungs-Nudge** (optional, `UserPromptSubmit`) — erkennt eine
  Abschlussäußerung wie „Gute Nacht" oder „bis morgen" und erzwingt den
  vollständigen Handoff-Skill vor der nächsten Antwort.

Details, Struktur des Handoff-Dokuments und die Lärm-Schutz-Regeln stehen in
[`SKILL.md`](SKILL.md).

## Wichtige Grenzen

- Ein automatischer Snapshot ersetzt kein bewusst erstelltes, inhaltliches
  Handoff.
- Hooks müssen in Claude Code einmal geprüft und vertraut werden (`/hooks`).
- Der Formulierungs-Nudge ist bewusst streng: nur eine Nachricht, die selbst
  die Abschlussformulierung ist, löst aus.

## Lizenz

Dieses Repository steht unter der [GNU GPL v3](../LICENSE).
