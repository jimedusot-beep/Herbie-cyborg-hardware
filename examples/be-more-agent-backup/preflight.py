"""Read-only local software diagnostics. No install, download, sudo or flashing."""
import argparse,importlib.util,json,platform,shutil,subprocess,urllib.request,urllib.error
def run(check_ollama=False):
    checks=[]
    for cmd in ['python3','arecord','aplay']:
        checks.append({'check':cmd,'available':shutil.which(cmd) is not None})
    checks.append({'check':'pyserial (optional diagnostic mode)','available':importlib.util.find_spec('serial') is not None})
    for cmd in [['arecord','-l'],['aplay','-l']]:
        if not shutil.which(cmd[0]):continue
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=3)
            checks.append({'check':' '.join(cmd),'returncode':p.returncode,'devices':p.stdout[:3000],'error':p.stderr[:500]})
        except subprocess.TimeoutExpired:checks.append({'check':' '.join(cmd),'error':'Timed out'})
    if check_ollama:
        # Fixed loopback-only GET; never follows a redirect or downloads a model.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args):return None
        try:
            req=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
            with req.open('http://127.0.0.1:11434/api/tags',timeout=2) as r:
                payload=r.read(65537)
                if len(payload)>65536:raise ValueError('Oversized response')
                tags=json.loads(payload)
            checks.append({'check':'local Ollama','models':[m.get('name') for m in tags.get('models',[])]})
        except (OSError,ValueError,urllib.error.URLError) as e:checks.append({'check':'local Ollama','error':str(e)[:200]})
    return {'mode':'read-only diagnostics','platform':platform.platform(),'physical_fit_verified':False,'physical_output_enabled':False,'checks':checks}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check-local-ollama',action='store_true');a=p.parse_args()
    print(json.dumps(run(a.check_local_ollama),indent=2))
