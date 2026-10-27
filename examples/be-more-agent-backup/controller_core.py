"""Pure, bounded wheel supervisor. MicroPython/CPython; no hardware imports.

Protocol is isolated from Herbie's pan/tilt simulations. Duty is permille,
not a physical speed. Boot is disarmed; faults require explicit clear + arm.
"""
VERSION = 1
MAX_FRAME_BYTES = 256

class DriveController:
    def __init__(self, session, allow_arm=False, max_duty=200, slew_per_s=500):
        if not isinstance(session, str) or len(session) != 16:
            raise ValueError('16-character boot session required')
        if type(max_duty) is not int or not 0 < max_duty <= 200:
            raise ValueError('max_duty must be 1..200 permille')
        if type(slew_per_s) is not int or not 1 <= slew_per_s <= 500:
            raise ValueError('slew_per_s must be 1..500')
        self.session = session
        self.allow_arm = allow_arm is True
        self.limit = max_duty
        self.slew = slew_per_s
        self.state = 'DISARMED'
        self.fault = None
        self.last_seq = -1
        self.epoch = 0
        self.last_valid_ms = 0
        self.lease_ms = 250
        self.last_tick_ms = 0
        self.left = self.right = 0
        self.target_left = self.target_right = 0
        self.driver_ok = True
        self.bumper_clear = True

    def zero(self):
        self.left = self.right = 0
        self.target_left = self.target_right = 0

    def trip(self, reason):
        self.zero()
        if self.state != 'FAULT_LATCHED':
            self.fault = reason
            self.epoch += 1  # Invalidate commands queued before the stop/fault.
        self.state = 'FAULT_LATCHED'

    def status(self, ok=True, error=None, command_seq=None):
        return dict(v=VERSION, session=self.session, state=self.state,
                    fault=self.fault, ok=ok, error=error, command_seq=command_seq,
                    last_seq=self.last_seq, epoch=self.epoch, left=self.left, right=self.right,
                    arm_allowed=self.allow_arm)

    @staticmethod
    def _approach(current, target, step):
        # A direction reversal always has a zero-output loop before the new sign.
        if current * target < 0:
            target = 0
        if current < target:
            return min(current + step, target)
        return max(current - step, target)

    def tick(self, now_ms, driver_ok=True, bumper_clear=True):
        self.driver_ok = driver_ok is True
        self.bumper_clear = bumper_clear is True
        if type(now_ms) is not int or now_ms < self.last_tick_ms:
            self.trip('CLOCK'); return
        dt = min(now_ms - self.last_tick_ms, 50)
        self.last_tick_ms = now_ms
        if not self.driver_ok:
            self.trip('DRIVER_FAULT')
        elif not self.bumper_clear:
            self.trip('BUMPER')
        elif self.state == 'ARMED' and now_ms - self.last_valid_ms >= self.lease_ms:
            self.trip('COMMAND_TIMEOUT')
        if self.state != 'ARMED':
            self.zero(); return
        step = self.slew * dt / 1000
        self.left = self._approach(self.left, self.target_left, step)
        self.right = self._approach(self.right, self.target_right, step)

    def handle(self, msg, now_ms):
        self.tick(now_ms, self.driver_ok, self.bumper_clear)
        # A recognizable STOP can only remove motion; accept even a stale session.
        if isinstance(msg, dict) and msg.get('op') == 'stop':
            self.zero()
            self.epoch += 1
            if self.state != 'FAULT_LATCHED': self.state = 'DISARMED'
            return self.status(command_seq=msg.get('seq'))
        seq = msg.get('seq') if isinstance(msg, dict) else None
        if not isinstance(msg, dict) or type(msg.get('v')) is not int or msg['v'] != VERSION:
            self.trip('BAD_VERSION'); return self.status(False, 'BAD_VERSION', seq)
        op = msg.get('op')
        if op == 'status' and set(msg) == {'v', 'op'}:
            return self.status()
        fields = {'v', 'op', 'session', 'seq', 'epoch'}
        if op == 'drive': fields |= {'left', 'right', 'lease_ms'}
        if op not in ('arm', 'drive', 'clear') or set(msg) != fields:
            self.trip('BAD_COMMAND'); return self.status(False, 'BAD_COMMAND', seq)
        if msg['session'] != self.session:
            self.trip('SESSION'); return self.status(False, 'SESSION', seq)
        if type(msg['epoch']) is not int or msg['epoch'] != self.epoch:
            self.trip('STALE_EPOCH'); return self.status(False, 'STALE_EPOCH', seq)
        if type(seq) is not int or not 0 <= seq <= 2147483647 or seq <= self.last_seq:
            self.trip('SEQUENCE'); return self.status(False, 'SEQUENCE', seq)
        if op == 'drive':
            if (any(type(msg[k]) is not int for k in ('left', 'right', 'lease_ms'))
                or any(abs(msg[k]) > self.limit for k in ('left', 'right'))
                or not 20 <= msg['lease_ms'] <= 200):
                self.trip('RANGE'); return self.status(False, 'RANGE', seq)
        # Only structurally valid commands advance sequence; rejected commands never renew a lease.
        self.last_seq = seq
        if op == 'clear':
            if not self.driver_ok or not self.bumper_clear:
                return self.status(False, 'FAULT_PRESENT', seq)
            self.zero(); self.state = 'DISARMED'; self.fault = None
        elif op == 'arm':
            if self.state != 'DISARMED': return self.status(False, 'NOT_DISARMED', seq)
            if not self.allow_arm: return self.status(False, 'OUTPUT_DISABLED', seq)
            self.zero(); self.state = 'ARMED'; self.last_valid_ms = now_ms; self.lease_ms = 250
        elif op == 'drive':
            if self.state != 'ARMED': return self.status(False, 'NOT_ARMED', seq)
            self.target_left = msg['left']; self.target_right = msg['right']
            self.last_valid_ms = now_ms; self.lease_ms = msg['lease_ms']
        return self.status(command_seq=seq)

class LineFramer:
    """No readline blocking or unbounded accumulation on a partial/flooded USB frame."""
    def __init__(self): self.buffer = ''; self.discard = False
    def feed(self, char):
        if char == '\n':
            if self.discard:
                self.discard = False; self.buffer = ''; return 'ERROR', 'FRAME_TOO_LONG'
            line = self.buffer; self.buffer = ''
            return ('LINE', line.rstrip('\r')) if line else (None, None)
        if self.discard: return None, None
        if len(self.buffer) >= MAX_FRAME_BYTES:
            self.discard = True; self.buffer = ''; return 'ERROR', 'FRAME_TOO_LONG'
        if ord(char) > 127 or ord(char) < 32 and char != '\r':
            self.discard = True; self.buffer = ''; return 'ERROR', 'BAD_CHARACTER'
        self.buffer += char
        return None, None
