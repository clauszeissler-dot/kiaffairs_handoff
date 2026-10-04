# KI AffAIrs Handoff für Codex

Aktuelles kleines Paket: [ki-affairs-handoff-1.2.0.zip](releases/ki-affairs-handoff-1.2.0.zip).
Nur Handoff-Skill, lokaler Snapshot und Abschluss-Hinweis; Python 3.11+, macOS/Linux.
[Anleitung und Funktionstest](handoff-package/README.md).

ZIP entpacken, `python3 install.py` ausführen, Codex neu starten, Hooks über `/hooks`
prüfen und vertrauen. Bestehende abweichende Handoff-Dateien werden sicher abgelehnt.
Für ein bewusstes Upgrade erst die Änderungen prüfen, dann `python3 install.py --overwrite`.
Backups entstehen vor Ersetzung. Frühere selbst eingerichtete Hook-Einträge prüfen;
das Paket entfernt keine fremden Hooks.

Das frühere Consultant-Toolkit 1.1.0 ist historisch und nicht die aktuelle Empfehlung:
sein Installer enthält bekannte Fehler bei Pfaden mit Leerzeichen und TOML-Sektionen.
Die Zusatzmodule dieses alten Archivs gehören nicht zum neuen kleinen Handoff-Paket.

Ein automatischer Snapshot ist kein vollständiges Handoff. Die 20-Prozent-Einstellung
steuert automatische Compaction; sie leert nicht den Chat und garantiert keine
fehlerfreien Antworten. Vollständige Übergabe schreiben und prüfen, dann neu starten.

GPL v3. [Prüfnachweis](../tests/PRUEFBERICHT.md).
