"""Default no-hardware simulator; real serial mode allows only STATUS and STOP.

Example: python3 bench_console.py
Diagnostics only: python3 bench_console.py --port /dev/serial/by-id/EXACT_DEVICE
pyserial is required only for the explicitly selected serial diagnostic mode.
"""
import argparse, json, time
from controller_core import DriveController

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',help='Exact local serial device; diagnostics only')
    parser.add_argument('--demo',action='store_true',help='Run a deterministic no-hardware timeout demonstration')
    args=parser.parse_args()
    if args.demo:
        if args.port:parser.error('--demo cannot be combined with --port')
        c=DriveController('simulated0000000',allow_arm=True)
        print('SIMULATED ONLY - no device opened')
        print(json.dumps(c.handle(dict(v=1,op='arm',session=c.session,seq=1,epoch=0),0)))
        print(json.dumps(c.handle(dict(v=1,op='drive',session=c.session,seq=2,epoch=0,left=100,right=100,lease_ms=200),0)))
        for t in [50,100,200]:c.tick(t);print(json.dumps(c.status()))
        return
    core=DriveController('simulated0000000',allow_arm=True) if not args.port else None
    link=None;seq=0;start=time.monotonic()
    if args.port:
        import serial
        link=serial.Serial(args.port,115200,timeout=.3,write_timeout=.2)
    print('SERIAL DIAGNOSTICS: status / stop / quit' if link else 'SIMULATED ONLY: status / arm / pulse LEFT RIGHT / stop / clear / quit')
    try:
        while True:
            try: words=input('herbie> ').strip().split()
            except EOFError:break
            if not words:continue
            if words[0]=='quit':break
            op=words[0];now=int((time.monotonic()-start)*1000)
            if link:
                if words!=['status'] and words!=['stop']:
                    print('Blocked: serial mode is read-only diagnostics plus STOP.');continue
                link.write((json.dumps({'v':1,'op':op})+'\n').encode('ascii'))
                reply=link.read_until(b'\n',257)
                if len(reply)>256:raise RuntimeError('Oversized controller response')
                print(reply.decode('ascii',errors='replace').strip() or 'No ACK; check cable/firmware. No reconnect or ARM is attempted.')
                continue
            seq+=1
            msg={'v':1,'op':op,'session':core.session,'seq':seq,'epoch':core.epoch}
            if op=='status':msg={'v':1,'op':'status'}
            elif op=='pulse':
                if len(words)!=3:print('Use pulse LEFT RIGHT, each -200..200');continue
                try:left,right=map(int,words[1:])
                except ValueError:print('Integer permille values required');continue
                msg.update(op='drive',left=left,right=right,lease_ms=200)
            result=core.handle(msg,now)
            print(json.dumps(result))
            if op=='pulse' and result['ok']:
                # Show the command expiring in simulation; no hardware imports occur.
                for dt in [20,50,100,200]:
                    core.tick(now+dt);print(json.dumps(core.status()))
                # Use one consistent simulated time origin after stepping ahead.
                start=time.monotonic()-(now+200)/1000
    finally:
        if link:
            try:link.write(b'{"v":1,"op":"stop"}\n')
            finally:link.close()
        elif core:core.handle({'op':'stop'},max(core.last_tick_ms,int((time.monotonic()-start)*1000)))
if __name__=='__main__':main()
