"""Fault-injection checks without hardware; do not certify the physical build."""
import ast,copy,hashlib,importlib.util,json,random,tempfile,unittest,zipfile
from pathlib import Path
CASE=Path(__file__).resolve().parents[1]/'examples/be-more-agent-backup'
def load(name):
 spec=importlib.util.spec_from_file_location('bma_'+name,CASE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
core=load('controller_core');ready=load('readiness')
backup=load('backup_state')
class DriveTests(unittest.TestCase):
 def setUp(self):self.c=core.DriveController('0123456789abcdef',allow_arm=True);self.seq=0
 def send(self,op,now=0,**fields):
  self.seq+=1;return self.c.handle(dict(v=1,op=op,session=self.c.session,seq=self.seq,epoch=self.c.epoch,**fields),now)
 def drive(self,now=0,left=150,right=150):return self.send('drive',now,left=left,right=right,lease_ms=200)
 def active(self):self.send('arm');self.drive();self.c.tick(50);self.assertGreater(self.c.left,0)
 def assertStopped(self):self.assertEqual((self.c.left,self.c.right,self.c.target_left,self.c.target_right),(0,0,0,0))
 def test_boot_disarmed(self):self.assertEqual(self.c.state,'DISARMED');self.assertStopped()
 def test_default_disables_arm(self):self.assertEqual(core.DriveController('0123456789abcdef').handle(dict(v=1,op='arm',session='0123456789abcdef',seq=1,epoch=0),0)['error'],'OUTPUT_DISABLED')
 def test_drive_before_arm(self):self.assertEqual(self.drive()['error'],'NOT_ARMED');self.assertStopped()
 def test_ramp_bounded(self):self.active();self.assertEqual(self.c.left,25)
 def test_stop_disarms(self):self.active();self.send('stop',60);self.assertEqual(self.c.state,'DISARMED');self.assertStopped()
 def test_stale_stop_still_stops(self):self.active();self.c.handle({'op':'stop','seq':-1,'session':'old'},60);self.assertStopped()
 def test_timeout_latches_at_boundary(self):self.active();self.c.tick(199);self.assertEqual(self.c.state,'ARMED');self.c.tick(200);self.assertEqual(self.c.fault,'COMMAND_TIMEOUT');self.assertStopped()
 def test_status_does_not_extend_lease(self):self.active();self.c.handle({'v':1,'op':'status'},190);self.c.tick(200);self.assertEqual(self.c.state,'FAULT_LATCHED')
 def test_no_implicit_rearm(self):self.active();self.c.tick(200);self.assertFalse(self.send('arm',201)['ok']);self.assertStopped()
 def test_clear_does_not_move(self):self.active();self.c.tick(200);self.send('clear',201);self.assertEqual(self.c.state,'DISARMED');self.assertStopped()
 def test_stop_does_not_clear_fault(self):self.c.trip('TEST');self.send('stop');self.assertEqual(self.c.state,'FAULT_LATCHED')
 def test_sequence_replay(self):self.active();self.c.handle(dict(v=1,op='arm',session=self.c.session,seq=1,epoch=self.c.epoch),60);self.assertEqual(self.c.fault,'SEQUENCE');self.assertStopped()
 def test_wrong_boot_session(self):self.active();self.c.handle(dict(v=1,op='drive',session='aaaaaaaaaaaaaaaa',seq=5,epoch=self.c.epoch,left=100,right=100,lease_ms=100),60);self.assertEqual(self.c.fault,'SESSION');self.assertStopped()
 def test_pre_stop_queued_arm_cannot_resume(self):
  packet=dict(v=1,op='arm',session=self.c.session,seq=100,epoch=0)
  self.send('stop');self.assertEqual(self.c.handle(packet,1)['error'],'STALE_EPOCH');self.assertStopped()
 def test_pre_fault_queued_clear_cannot_resume(self):
  packet=dict(v=1,op='clear',session=self.c.session,seq=100,epoch=0)
  self.c.trip('TEST');self.assertEqual(self.c.handle(packet,1)['error'],'STALE_EPOCH');self.assertEqual(self.c.state,'FAULT_LATCHED')
 def test_fault_input_stops(self):self.active();self.c.tick(60,driver_ok=False);self.assertEqual(self.c.fault,'DRIVER_FAULT');self.assertStopped()
 def test_fault_cannot_clear_while_present(self):self.c.tick(0,driver_ok=False);self.assertFalse(self.send('clear')['ok'])
 def test_bumper_stops(self):self.active();self.c.tick(60,bumper_clear=False);self.assertEqual(self.c.fault,'BUMPER');self.assertStopped()
 def test_reverse_has_zero_step(self):
  self.active();self.drive(60,left=-150,right=-150);self.c.tick(110);self.c.tick(120);self.assertEqual(self.c.left,0);self.c.tick(130);self.assertLess(self.c.left,0)
 def test_backward_clock_stops(self):self.active();self.c.tick(40);self.assertEqual(self.c.fault,'CLOCK');self.assertStopped()
 def test_bad_commands_fail_closed(self):
  packets=[[],None,{},dict(v=True,op='status'),dict(v=2,op='arm'),dict(v=1,op='dance'),dict(v=1,op='arm',session=self.c.session,seq=True)]
  for packet in packets:
   with self.subTest(packet=packet):self.setUp();self.active();self.assertFalse(self.c.handle(packet,60)['ok']);self.assertStopped()
 def test_bad_values_never_reach_outputs(self):
  for key in ['left','right','lease_ms']:
   for value in [True,None,'50',1.2,float('nan'),float('inf'),-10000,10000]:
    with self.subTest(key=key,value=value):
     self.setUp();self.send('arm');packet=dict(v=1,op='drive',session=self.c.session,seq=2,epoch=0,left=100,right=100,lease_ms=100);packet[key]=value
     self.assertFalse(self.c.handle(packet,1)['ok']);self.assertStopped()
 def test_extra_field_rejected(self):self.send('arm');self.assertFalse(self.send('drive',1,left=0,right=0,lease_ms=100,untrusted='x')['ok'])
 def test_oversized_frame_stops_before_newline(self):
  f=core.LineFramer();errors=[]
  for ch in 'x'*10000:
   event,_=f.feed(ch)
   if event:errors.append(event)
   self.assertLessEqual(len(f.buffer),core.MAX_FRAME_BYTES)
  self.assertIn('ERROR',errors)
 def test_framer_recovers_after_overflow(self):
  f=core.LineFramer()
  for ch in 'x'*300+'\n':f.feed(ch)
  result=None
  for ch in '{"v":1,"op":"status"}\n':result=f.feed(ch)
  self.assertEqual(result,('LINE','{"v":1,"op":"status"}'))
 def test_seeded_fault_storm_never_moves_disarmed(self):
  rng=random.Random(17)
  for t in range(500):
   self.c.handle(rng.choice([{},None,[],{'op':'stop'},{'v':1,'op':'status'}]),t)
   self.assertStopped()
 def test_firmware_output_disabled_in_source(self):
  tree=ast.parse((CASE/'pico_main.py').read_text());flag=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ALLOW_PHYSICAL_OUTPUT' for t in n.targets))
  self.assertIs(flag,False)

class EvidenceTests(unittest.TestCase):
 def setUp(self):self.r=ready.template();self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name)
 def tearDown(self):self.temp.cleanup()
 def fill(self):
  (self.base/'bench.txt').write_text('Test fixture only; not actual hardware evidence.')
  digest=hashlib.sha256((self.base/'bench.txt').read_bytes()).hexdigest()
  for name,fields in ready.GATES.items():
   self.r['gates'][name].update(result='pass',reviewer='Unit test fixture',tested_at='2026-10-27',evidence_file='bench.txt',sha256=digest,
    observations={key:('fixture' if kind=='text' else True if kind=='true' else 1.0) for key,kind in fields.items()})
 def test_blank_is_not_pass(self):self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_checkbox_alone_is_not_pass(self):
  for g in self.r['gates'].values():g['result']='pass'
  self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_complete_fixture_is_format_only(self):self.fill();r=ready.evaluate(self.r,self.base);self.assertTrue(r['format_complete']);self.assertFalse(r['hardware_certified']);self.assertFalse(r['physical_output_enabled'])
 def test_corrupted_evidence_rejected(self):self.fill();(self.base/'bench.txt').write_text('changed');self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_path_escape_rejected(self):self.fill();self.r['gates']['parts_identified']['evidence_file']='../outside';self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_bad_numeric_observation_rejected(self):
  self.fill();self.r['gates']['mechanical_fit']['observations']['assembled_mass_kg']=True;self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_overweight_requires_redesign(self):self.fill();self.r['gates']['mechanical_fit']['observations']['assembled_mass_kg']=2;self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_late_stop_rejected(self):self.fill();self.r['gates']['motion_fault_bench']['observations']['stop_latency_ms']=301;self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_cannot_promote_backup_with_flag(self):self.fill();self.r['motion_enabled']=True;self.assertFalse(ready.evaluate(self.r,self.base)['format_complete'])
 def test_malformed_records(self):
  for value in [None,[],{'gates':[]},{'gates':{'parts_identified':'pass'}}]:self.assertFalse(ready.evaluate(value,self.base)['format_complete'])

class BackupTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.app=self.root/'app';self.app.mkdir()
  (self.app/'config.json').write_text('{"text_model":"fixture"}')
  (self.app/'chat_memory.json').write_text('["private fixture"]');self.out=self.root/'backup.zip'
 def tearDown(self):self.temp.cleanup()
 def test_default_excludes_memory(self):
  backup.create(self.app,self.out)
  with zipfile.ZipFile(self.out) as z:self.assertNotIn('chat_memory.json',z.namelist())
 def test_opt_in_memory_roundtrip(self):
  backup.create(self.app,self.out,True);dest=self.root/'restore';backup.restore(self.out,dest)
  self.assertEqual((dest/'chat_memory.json').read_bytes(),(self.app/'chat_memory.json').read_bytes())
 def test_never_overwrites_live_destination(self):
  backup.create(self.app,self.out)
  with self.assertRaises(ValueError):backup.restore(self.out,self.app)
  self.assertEqual(json.loads((self.app/'config.json').read_text())['text_model'],'fixture')
 def test_refuses_existing_archive(self):
  backup.create(self.app,self.out)
  with self.assertRaises(ValueError):backup.create(self.app,self.out)
 def test_bad_hash_creates_no_destination(self):
  with zipfile.ZipFile(self.out,'w') as z:
   z.writestr('config.json','{}');z.writestr('manifest.json',json.dumps({'schema':1,'files':{'config.json':'bad'}}))
  dest=self.root/'restore'
  with self.assertRaises(ValueError):backup.restore(self.out,dest)
  self.assertFalse(dest.exists())
 def test_traversal_archive_rejected(self):
  with zipfile.ZipFile(self.out,'w') as z:z.writestr('../evil','x')
  with self.assertRaises(ValueError):backup.restore(self.out,self.root/'restore')

class RegistrationTests(unittest.TestCase):
 def test_backup_is_not_primary_inventory_or_enabled_motion(self):
  option=json.loads((CASE/'option.json').read_text());self.assertEqual(option['status'],'backup-only');self.assertFalse(option['motion_enabled'])
  canonical=CASE.parents[1]/'integration/system-manifest.json';self.assertFalse(json.loads(canonical.read_text())['motion_enabled'])
  catalog=json.loads((CASE/'candidate_catalog.json').read_text());ids=[p['backup_id'] for p in catalog['candidates']]
  self.assertEqual(len(ids),len(set(ids)));self.assertTrue(all(i.startswith('BMA-') for i in ids))
  self.assertTrue(all(p['confirmed_owned'] is False for p in catalog['candidates']))
  self.assertNotIn('BMA-',(CASE.parents[1]/'bom/components.csv').read_text())

if __name__=='__main__':unittest.main()
