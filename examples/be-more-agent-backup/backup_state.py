"""Local config backup with hash checks. Memory requires an explicit opt-in.

Restores only into a NEW directory; never overwrites a live robot or auto-starts it.
Hashes detect accidental damage; they do not authenticate an untrusted archive.
"""
import argparse,hashlib,json,os,stat,tempfile,zipfile
from pathlib import Path
LIMIT=10_000_000
ALLOWED={'config.json','chat_memory.json'}
def create(root,out,include_memory=False):
    root=Path(root).resolve();out=Path(out)
    if out.exists():raise ValueError('Backup path already exists')
    names=['config.json']+(['chat_memory.json'] if include_memory else [])
    files={}
    for name in names:
        p=root/name
        if p.is_symlink() or not p.is_file() or not 0<p.stat().st_size<=LIMIT:raise ValueError('Missing or invalid '+name)
        raw=p.read_bytes();json.loads(raw);files[name]=raw
    manifest={'schema':1,'files':{n:hashlib.sha256(v).hexdigest() for n,v in files.items()},'memory_included':include_memory}
    out.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.herbie-backup-',dir=out.parent);os.close(fd)
    try:
        with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
            for n,data in files.items():z.writestr(n,data)
            z.writestr('manifest.json',json.dumps(manifest,indent=2))
        # Atomic no-replace publish on the same filesystem, retaining the 0600 mode.
        os.link(tmp,out)
    finally:Path(tmp).unlink(missing_ok=True)
    return manifest
def restore(archive,dest):
    dest=Path(dest)
    if dest.exists():raise ValueError('Restore destination must be a new directory')
    files={}
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        if len(names)!=len(set(names)) or set(names)-ALLOWED-{'manifest.json'}:raise ValueError('Unexpected/duplicate backup entries')
        if 'manifest.json' not in names or any(i.file_size>LIMIT or stat.S_ISLNK(i.external_attr>>16) for i in infos):raise ValueError('Invalid backup entry')
        manifest=json.loads(z.read('manifest.json'))
        if not isinstance(manifest,dict) or manifest.get('schema')!=1 or not isinstance(manifest.get('files'),dict):raise ValueError('Bad backup manifest')
        if set(names)!=(set(manifest['files'])|{'manifest.json'}) or 'config.json' not in manifest['files']:raise ValueError('Manifest entries differ')
        for name,digest in manifest['files'].items():
            raw=z.read(name)
            if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Hash mismatch: '+name)
            json.loads(raw);files[name]=raw
    # All content has been validated before creating the new destination.
    dest.mkdir(parents=False,mode=0o700)
    for name,raw in files.items():
        p=dest/name
        with p.open('xb') as f:f.write(raw)
        p.chmod(0o600)
    return sorted(files)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='op',required=True)
    c=sub.add_parser('create');c.add_argument('--root',type=Path,required=True);c.add_argument('--out',type=Path,required=True);c.add_argument('--include-memory',action='store_true')
    r=sub.add_parser('restore');r.add_argument('--archive',type=Path,required=True);r.add_argument('--dest',type=Path,required=True)
    a=p.parse_args()
    try:result=create(a.root,a.out,a.include_memory) if a.op=='create' else restore(a.archive,a.dest)
    except (OSError,ValueError,zipfile.BadZipFile) as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))
