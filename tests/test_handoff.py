import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest
import zipfile
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'codex/handoff-package'
s=importlib.util.spec_from_file_location('installer',PKG/'install.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class HandoffTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name).resolve();self.target=self.base/'agent home with spaces';self.project=self.base/'project with spaces';self.project.mkdir()
 def installed(self,config=''):
  self.target.mkdir();(self.target/'config.toml').write_text(config)
  m.install(self.target,True,272000,20)
  return json.loads((self.target/'hooks.json').read_text())
 def hook(self,command,event):
  return subprocess.run(command,shell=True,cwd=self.base,input=json.dumps(event),text=True,capture_output=True)
 def test_root_threshold_and_profile_preserved(self):
  self.installed('[profiles.test]\nmodel="fixture"\nmodel_auto_compact_token_limit=500\n');d=tomllib.loads((self.target/'config.toml').read_text());self.assertEqual(d['model_auto_compact_token_limit'],217600);self.assertEqual(d['profiles']['test']['model_auto_compact_token_limit'],500)
 def test_idempotent_no_duplicate_hooks(self):
  self.installed();first=(self.target/'hooks.json').read_bytes();m.install(self.target,True,272000,20);self.assertEqual(first,(self.target/'hooks.json').read_bytes())
 def test_preserve_other_hooks(self):
  self.target.mkdir();(self.target/'hooks.json').write_text(json.dumps({'custom':'keep','hooks':{'PreCompact':[{'hooks':[{'type':'command','command':'echo harmless'}]}]}}));m.install(self.target);d=json.loads((self.target/'hooks.json').read_text());self.assertEqual(d['custom'],'keep');self.assertEqual(len(d['hooks']['PreCompact']),2)
 def test_existing_threshold_preserved(self):
  self.installed('model_auto_compact_token_limit = 12345\n');self.assertEqual(tomllib.loads((self.target/'config.toml').read_text())['model_auto_compact_token_limit'],12345)
 def test_explicit_overwrite_backup(self):
  self.installed('model_auto_compact_token_limit = 12345\n');m.configure_compaction(self.target/'config.toml',272000,20,True);self.assertTrue(list(self.target.glob('config.toml.handoff-backup-*')));self.assertEqual(tomllib.loads((self.target/'config.toml').read_text())['model_auto_compact_token_limit'],217600)
 def test_spaces_and_event_cwd(self):
  d=self.installed();r=self.hook(d['hooks']['PreCompact'][0]['hooks'][0]['command'],{'cwd':str(self.project)});self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(Path(r.stdout.strip()).is_file());self.assertEqual(Path(r.stdout.strip()).parent,self.project/'docs/handoffs')
 def test_rapid_calls_unique_snapshots(self):
  d=self.installed();c=d['hooks']['PreCompact'][0]['hooks'][0]['command'];paths=[self.hook(c,{'cwd':str(self.project)}).stdout.strip() for _ in range(3)];self.assertEqual(len(set(paths)),3);self.assertTrue(all(Path(p).is_file() for p in paths))
 def test_git_subdirectory_root(self):
  subprocess.run(['git','init','-q',str(self.project)],check=True);sub=self.project/'nested';sub.mkdir();d=self.installed();r=self.hook(d['hooks']['PreCompact'][0]['hooks'][0]['command'],{'cwd':str(sub)});self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(Path(r.stdout.strip()).parent,self.project/'docs/handoffs')
 def test_full_handoff_reference(self):
  p=self.project/'docs/handoffs';p.mkdir(parents=True);(p/'20261004_01_fixture.md').write_text('# Fixture\nDecision: use blue.');d=self.installed();r=self.hook(d['hooks']['PreCompact'][0]['hooks'][0]['command'],{'cwd':str(self.project)});self.assertIn('20261004_01_fixture.md',Path(r.stdout.strip()).read_text())
 def test_session_end_nudge(self):
  d=self.installed();r=self.hook(d['hooks']['UserPromptSubmit'][0]['hooks'][0]['command'],{'cwd':str(self.project),'prompt':'Ende für heute'});self.assertEqual(r.returncode,0,r.stderr);self.assertIn('/handoff',json.loads(r.stdout)['hookSpecificOutput']['additionalContext'])
 def test_quoted_ending_does_not_trigger(self):
  d=self.installed();r=self.hook(d['hooks']['UserPromptSubmit'][0]['hooks'][0]['command'],{'cwd':str(self.project),'prompt':'Schreibe einen Text über Gute Nacht'});self.assertEqual(r.stdout,'')
 def test_invalid_json_no_installation(self):
  self.target.mkdir();p=self.target/'hooks.json';p.write_text('not JSON')
  with self.assertRaises(ValueError):m.install(self.target)
  self.assertFalse((self.target/'skills').exists());self.assertEqual(p.read_text(),'not JSON')
 def test_invalid_toml_no_installation(self):
  self.target.mkdir();p=self.target/'config.toml';p.write_text('[invalid')
  with self.assertRaises(ValueError):m.install(self.target)
  self.assertFalse((self.target/'skills').exists())
 def test_invalid_window_no_installation(self):
  with self.assertRaises(ValueError):m.install(self.target,True,0,20)
  self.assertFalse(self.target.exists())
 def test_missing_cwd_reports_failure(self):
  d=self.installed();r=self.hook(d['hooks']['PreCompact'][0]['hooks'][0]['command'],{'cwd':str(self.project/'missing')});self.assertNotEqual(r.returncode,0);self.assertIn('fehlgeschlagen',r.stderr)

 def test_parallel_snapshots(self):
  d=self.installed();c=d['hooks']['PreCompact'][0]['hooks'][0]['command']
  with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(lambda _:self.hook(c,{'cwd':str(self.project)}),range(16)))
  self.assertTrue(all(r.returncode==0 for r in results));self.assertEqual(len({r.stdout for r in results}),16)
 def test_release_archive_install(self):
  archive=ROOT/'codex/releases/ki-affairs-handoff-1.2.0.zip'
  with zipfile.ZipFile(archive) as z:z.extractall(self.base/'release')
  installer=self.base/'release/ki-affairs-handoff-1.2.0/install.py'
  r=subprocess.run(['python3',str(installer),'--yes','--codex-home',str(self.target),'--configure-compaction','--context-window','272000'],capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr)
  d=json.loads((self.target/'hooks.json').read_text());r=self.hook(d['hooks']['PreCompact'][0]['hooks'][0]['command'],{'cwd':str(self.project)});self.assertEqual(r.returncode,0,r.stderr)

if __name__=='__main__':unittest.main()
