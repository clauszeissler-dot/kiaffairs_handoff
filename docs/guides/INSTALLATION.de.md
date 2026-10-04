# Installation · KI AffAIrs Handoff 1.2.0

[Download: ki-affairs-handoff-1.2.0.zip](../../codex/releases/ki-affairs-handoff-1.2.0.zip).
Python 3.11+, macOS/Linux. ZIP entpacken und `python3 install.py` ausführen.
Es wird ausschließlich Handoff installiert. Codex neu starten; `/hooks` prüfen und vertrauen.

Bei bestehenden abweichenden Dateien: Änderungen prüfen und bewusst `python3 install.py --overwrite`
verwenden. Vor der Ersetzung werden Sicherungen angelegt. Frühere manuelle Hooks gesondert prüfen.
Keine alten `--handoff --engineering`-Argumente verwenden.

[Ausführliche Anleitung, Schwelle und Funktionstest](../../codex/handoff-package/README.md).
Ein Snapshot ist kein vollständiges Handoff. Erst vollständige Übergabe speichern und prüfen,
dann neu starten. Alte 1.1.0 ist historisch und keine aktuelle Empfehlung.
