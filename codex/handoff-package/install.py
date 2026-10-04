#!/usr/bin/env python3
"""Install only KI AffAIrs Handoff, preserving existing settings and hooks."""
import argparse
import json
from pathlib import Path
import re
import shlex
import shutil
import sys
import tempfile
import tomllib
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
        stream.write(text)
        temp = Path(stream.name)
    temp.replace(path)

def backup(path):
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(path, path.with_name(path.name + '.handoff-backup-' + stamp))

def configure_compaction(path, context_window, remaining_percent, overwrite=False):
    if context_window < 100 or not 1 <= remaining_percent <= 99:
        raise ValueError('Kontextfenster mindestens 100 Tokens; Restkontext 1–99 Prozent.')
    threshold = context_window * (100 - remaining_percent) // 100
    text = path.read_text() if path.exists() else ''
    data = tomllib.loads(text)
    key = 'model_auto_compact_token_limit'
    if key in data and not overwrite:
        return False
    # Root keys belong before the first table. Preserve profile-specific settings.
    first_table = re.search(r'^\s*\[', text, re.M)
    boundary = first_table.start() if first_table else len(text)
    root, tables = text[:boundary], text[boundary:]
    for name in (key, 'model_auto_compact_token_limit_scope'):
        root = re.sub(r'^\s*' + name + r'\s*=.*\n?', '', root, flags=re.M)
    root = f'model_auto_compact_token_limit = {threshold}\nmodel_auto_compact_token_limit_scope = "total"\n' + root
    updated = root + tables
    assert tomllib.loads(updated)[key] == threshold
    backup(path)
    atomic_write(path, updated)
    return True

def install(target, configure=False, context_window=None, remaining=20, overwrite=False):
    target = target.expanduser().resolve()
    config = target / 'config.toml'
    # Validate every input before writing anything.
    if configure:
        if context_window is None or context_window < 100 or not 1 <= remaining <= 99:
            raise ValueError('Gültiges Kontextfenster und Restkontext erforderlich.')
    if config.exists():
        tomllib.loads(config.read_text())
    path = target / 'hooks.json'
    data = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(data, dict) or not isinstance(data.get('hooks', {}), dict):
        raise ValueError('hooks.json benötigt ein JSON-Objekt mit hooks-Objekt.')
    hooks = data.setdefault('hooks', {})
    for event in ('PreCompact', 'UserPromptSubmit'):
        groups = hooks.get(event, [])
        if not isinstance(groups, list) or any(not isinstance(g, dict) or not isinstance(g.get('hooks', []), list) for g in groups):
            raise ValueError('Ungültige Hook-Gruppen: ' + event)
    for relative in ('skills/handoff/SKILL.md', 'skills/handoff/scripts/snapshot.py', 'hooks/codex_session_hook.py'):
        dest = target / relative
        if dest.exists() and not overwrite:
            if dest.read_bytes() != (ROOT / relative).read_bytes():
                raise ValueError(f'Abweichende vorhandene Datei: {dest}. Prüfen und ggf. --overwrite wählen.')
    for relative in ('skills/handoff/SKILL.md', 'skills/handoff/scripts/snapshot.py', 'hooks/codex_session_hook.py'):
        dest = target / relative
        if dest.exists() and dest.read_bytes() == (ROOT / relative).read_bytes():
            continue
        backup(dest)
        atomic_write(dest, (ROOT / relative).read_text())
    commands = {
        'PreCompact': {'matcher': '^auto$', 'hooks': [{'type': 'command', 'command': shlex.join([sys.executable, str(target / 'skills/handoff/scripts/snapshot.py')]), 'timeout': 30}]},
        'UserPromptSubmit': {'hooks': [{'type': 'command', 'command': shlex.join([sys.executable, str(target / 'hooks/codex_session_hook.py')]), 'timeout': 30}]},
    }
    for event, group in commands.items():
        groups = hooks.setdefault(event, [])
        command = group['hooks'][0]['command']
        if not any(h.get('command') == command for g in groups for h in g.get('hooks', []) if isinstance(h, dict)):
            groups.append(group)
    updated = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if not path.exists() or path.read_text() != updated:
        backup(path)
        atomic_write(path, updated)
    if configure:
        configure_compaction(config, context_window, remaining, overwrite)
    return target

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--codex-home', type=Path, default=Path.home() / '.codex')
    p.add_argument('--configure-compaction', action='store_true')
    p.add_argument('--context-window', type=int)
    p.add_argument('--remaining-context-percent', type=int, default=20)
    p.add_argument('--overwrite', action='store_true')
    p.add_argument('--yes', action='store_true')
    a = p.parse_args()
    if not a.yes:
        if input('Nur Handoff-Skill und zwei Hooks installieren? [j/N] ').strip().lower() not in ('j','ja','y','yes'):
            return
    try:
        target = install(a.codex_home, a.configure_compaction, a.context_window, a.remaining_context_percent, a.overwrite)
    except (ValueError, OSError) as error:
        p.exit(1, f'Installation abgebrochen: {error}\n')
    print(f'Installiert: {target}. Codex neu starten und Hooks über /hooks prüfen und vertrauen.')
    print('Der automatische Hook schreibt einen Snapshot. Vollständiges Handoff: /handoff, Datei prüfen, dann neue Session.')
if __name__ == '__main__':
    main()
