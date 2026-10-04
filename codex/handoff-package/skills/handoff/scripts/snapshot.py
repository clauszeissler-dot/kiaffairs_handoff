#!/usr/bin/env python3
"""Atomic local snapshot. No model call, transcript upload or automatic clear."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone

def git(cwd, *args):
    r = subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True, timeout=10)
    return r.stdout.strip() if r.returncode == 0 else '(nicht verfügbar)'

def snapshot(cwd, reason='precompact'):
    cwd = Path(cwd).resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError('cwd ist kein Verzeichnis')
    root = git(cwd, 'rev-parse', '--show-toplevel')
    root = cwd if root == '(nicht verfügbar)' else Path(root)
    folder = root / 'docs/handoffs'
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    # Unique filename, atomic publication. Existing snapshots are never replaced.
    dest = folder / f'AUTO_{stamp}_{uuid.uuid4().hex}.md'
    sections = [f'# Auto-Snapshot · {stamp}', '> Sicherheitsnetz; kein vollständiges inhaltliches Handoff.',
                f'## Anlass\n{reason}', f'## Projekt\n{root}']
    for heading, args in [('Git-Status', ['status','--short']), ('Branch',['branch','--show-current']), ('Letzter Commit',['log','-1','--oneline'])]:
        sections.append(f'## {heading}\n```text\n{git(root,*args)}\n```')
    handoffs = sorted((p for p in folder.glob('*.md') if not p.name.startswith('AUTO_')), key=lambda p:p.stat().st_mtime, reverse=True)
    sections.append('## Inhaltliche Übergabe\n' + (f'Zuletzt vorhanden: {handoffs[0].name}. Inhalt vor Wiederaufnahme prüfen.' if handoffs else 'Noch keine. Vor einem bewussten Neustart /handoff ausführen und prüfen.'))
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=folder,delete=False) as f:
        f.write('\n\n'.join(sections)+'\n'); tmp=Path(f.name)
    try:
        os.link(tmp,dest)
    finally:
        tmp.unlink(missing_ok=True)
    return dest

def main():
    payload = sys.stdin.read() if not sys.stdin.isatty() else ''
    event = json.loads(payload) if payload.strip() else {}
    if not isinstance(event,dict):
        raise ValueError('Hook-Eingabe muss ein Objekt sein')
    print(snapshot(event.get('cwd') or Path.cwd(), str(event.get('hook_event_name','precompact'))))
if __name__ == '__main__':
    try: main()
    except (ValueError,OSError,subprocess.TimeoutExpired) as e:
        print(f'Snapshot fehlgeschlagen: {e}',file=sys.stderr);sys.exit(1)
