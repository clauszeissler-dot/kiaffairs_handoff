#!/usr/bin/env python3
"""Prompt hook: request a full handoff; never claim the model already wrote one."""
import json
from pathlib import Path
import re
import subprocess
import sys

ENDING = re.compile(r'(?:ende f(?:ü|u|ue)r heute|f(?:ü|u|ue)r heute reicht(?: es)?|feierabend|gute nacht|bis morgen|wir machen morgen weiter)[.!…]*',re.I)

def main():
    event = json.load(sys.stdin)
    if not isinstance(event,dict): return
    prompt = ' '.join(str(event.get('prompt','')).split())
    if not ENDING.fullmatch(prompt): return
    script = Path(__file__).resolve().parents[1] / 'skills/handoff/scripts/snapshot.py'
    r = subprocess.run([sys.executable,str(script)],input=json.dumps(event),capture_output=True,text=True,timeout=20)
    status = 'Minimaler Snapshot: '+r.stdout.strip() if r.returncode==0 else 'Snapshot fehlgeschlagen; vollständiges Handoff trotzdem schreiben.'
    print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':status+' Vor der Abschlussantwort /handoff ausführen, vollständige Übergabe speichern und prüfen.'}},ensure_ascii=False))
if __name__=='__main__':
    try: main()
    except (ValueError,OSError,subprocess.TimeoutExpired) as e:
        print(f'Handoff-Hinweis fehlgeschlagen: {e}',file=sys.stderr);sys.exit(1)
