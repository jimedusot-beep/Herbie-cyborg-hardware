"""Validate evidence structure. Never equate this result with physical certification."""
import argparse,datetime,hashlib,json,math
from pathlib import Path
GATES={
 'parts_identified':{'display_sku':'text','driver_sku':'text','motor_sku':'text','cell_sku':'text'},
 'mechanical_fit':{'display_width_mm':'positive','display_height_mm':'positive','assembled_mass_kg':'positive','cables_clear':'true'},
 'electrical_review':{'review_note':'text','power_domains_checked':'true','fuse_selected':'true','battery_spec_checked':'true'},
 'stationary_bench':{'voice_cycles':'positive','speaker_heard':'true','camera_checked':'true','power_stable':'true'},
 'motion_fault_bench':{'stop_latency_ms':'positive','timeout_latency_ms':'positive','reset_no_motion':'true','cutoff_stops_motors':'true'},
 'load_thermal_bench':{'left_run_current_a':'positive','right_run_current_a':'positive','soak_minutes':'positive','temperatures_within_reviewed_limits':'true'},
 'recovery':{'backup_restored':'true','reboot_disarmed':'true','fault_requires_clear_then_arm':'true'}
}
def template():
 return {'schema_version':1,'option_id':'HERBIE-BACKUP-BMA-001','status':'backup-only','motion_enabled':False,
 'gates':{name:{'result':'pending','observations':{k:None for k in fields},'evidence_file':None,'sha256':None,'reviewer':None,'tested_at':None} for name,fields in GATES.items()}}
def evaluate(record,base):
    errors=[]
    if not isinstance(record,dict):return {'format_complete':False,'hardware_certified':False,'physical_output_enabled':False,'errors':['Record must be an object']}
    if record.get('schema_version')!=1 or record.get('option_id')!='HERBIE-BACKUP-BMA-001':errors.append('Wrong schema or option ID')
    if record.get('motion_enabled') is not False:errors.append('This backup register must keep motion_enabled=false')
    gates=record.get('gates',{})
    if not isinstance(gates,dict):gates={};errors.append('gates must be an object')
    for name,fields in GATES.items():
        gate=gates.get(name,{})
        if not isinstance(gate,dict):gate={}
        if gate.get('result')!='pass':errors.append(name+': no recorded pass');continue
        if not isinstance(gate.get('reviewer'),str) or not gate['reviewer'].strip():errors.append(name+': missing reviewer')
        try:datetime.date.fromisoformat(gate.get('tested_at',''))
        except (ValueError,TypeError):errors.append(name+': invalid test date')
        observations=gate.get('observations',{})
        if not isinstance(observations,dict):observations={}
        for key,kind in fields.items():
            v=observations.get(key)
            ok=(isinstance(v,str) and bool(v.strip())) if kind=='text' else v is True if kind=='true' else type(v) in (int,float) and 0<v<1e9 and math.isfinite(v)
            if not ok:errors.append(name+': missing/invalid observation '+key)
        if name=='mechanical_fit' and type(observations.get('assembled_mass_kg')) in (int,float) and observations['assembled_mass_kg']>1.5:errors.append(name+': above Rev A mass assumption; resize drive and structure')
        if name=='motion_fault_bench':
            for key in ['stop_latency_ms','timeout_latency_ms']:
                v=observations.get(key)
                if type(v) in (int,float) and v>300:errors.append(name+': '+key+' exceeds 300ms target')
        try:
            if not isinstance(gate.get('evidence_file'),str) or not gate['evidence_file']:raise ValueError('missing evidence path')
            path=(base/gate['evidence_file']).resolve();path.relative_to(base.resolve())
            if not path.is_file() or path.stat().st_size==0 or path.stat().st_size>10_000_000:raise ValueError('missing, empty or oversized evidence')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=gate.get('sha256'):raise ValueError('evidence hash mismatch')
        except (OSError,ValueError,TypeError) as e:errors.append(name+': '+str(e))
    return {'format_complete':not errors,'hardware_certified':False,'physical_output_enabled':False,'errors':errors}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path);a=p.parse_args()
    try:r=evaluate(json.loads(a.record.read_text()),a.record.parent)
    except (OSError,ValueError,TypeError) as e:raise SystemExit(str(e))
    print(json.dumps(r,indent=2));raise SystemExit(0 if r['format_complete'] else 2)
