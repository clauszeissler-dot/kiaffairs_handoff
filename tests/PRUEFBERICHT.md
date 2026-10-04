# Prüfnachweis · 04.10.2026

Altstand 1.1.0 reproduziert: TOML-Schwelle nach einer Profiltabelle falsch einsortiert;
Hook-Pfad mit Leerzeichen scheitert mit Exit 127. Neue fokussierte Codex-Fassung 1.2.0:
17 automatisierte Tests grün. Installation/Reinstallation, Backup, vorhandene Hooks,
TOML-Root und Profile, Pfade mit Leerzeichen, Hook-Eingabe-cwd, Git-Unterordner,
ohne Git, schnelle wiederholte Snapshots, Handoff-Verweis, Abschluss-Hinweis,
falsche Abschlussphrase, kaputtes JSON/TOML, ungültige Fenstergröße, fehlendes cwd, 16 parallele Aufrufe, Installation aus dem Release-ZIP.

Offizielles Schema `openai/codex/codex-rs/core/config.schema.json`: Parameter
`model_auto_compact_token_limit` und `model_auto_compact_token_limit_scope` vorhanden.
Installed CLI: 0.160.0. Diese Pakettests führen die installierten Hook-Kommandos aus;
sie simulieren keine vollständige echte Context-Compaction im Modell.

Kein garantierter Ausschluss von Context Rot oder Drift. Kein automatischer vollständiger
semantischer Handoff und kein automatisches Clear behauptet. Claude-Altvariante wird mit
dieser Prüfung nicht als getestet freigegeben.
