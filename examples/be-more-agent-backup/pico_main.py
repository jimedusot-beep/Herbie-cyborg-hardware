"""Pico 2 MicroPython controller candidate. Physical output ships DISABLED.

Review COMMISSIONING.md before flashing. Copy this as main.py alongside
controller_core.py after disconnecting motor power. No browser/LLM transport.
"""
ALLOW_PHYSICAL_OUTPUT = False  # Requires hardware review + commissioning evidence; never set automatically.
USE_BUMPERS = False           # Only after actual switches are fitted and tested.

def run():
    import sys, time, select, json, os, binascii
    from machine import Pin, PWM, WDT
    from controller_core import DriveController, LineFramer

    pins = [Pin(n, Pin.OUT, value=0) for n in (2, 3, 4, 5)]
    pwms = []
    try:
        for pin in pins:
            pwm = PWM(pin); pwm.freq(20000); pwm.duty_u16(0); pwms.append(pwm)
        fault = Pin(7, Pin.IN, Pin.PULL_UP)
        bumpers = [Pin(n, Pin.IN, Pin.PULL_UP) for n in (10, 11)] if USE_BUMPERS else []
        session = binascii.hexlify(os.urandom(8)).decode()
        core = DriveController(session, allow_arm=ALLOW_PHYSICAL_OUTPUT)
        framer = LineFramer(); poll = select.poll(); poll.register(sys.stdin, select.POLLIN)
        wdt = WDT(timeout=250)
        previous = time.ticks_ms(); now = 0
        while True:
            actual = time.ticks_ms(); now += max(0, time.ticks_diff(actual, previous)); previous = actual
            core.tick(now, driver_ok=bool(fault.value()), bumper_clear=all(p.value() for p in bumpers))
            # Limit input work per loop; no unterminated line can block timeout service.
            for _ in range(64):
                events = poll.poll(0)
                if not events: break
                if any(event[1] & (select.POLLHUP | select.POLLERR) for event in events):
                    core.trip('USB_LINK'); break
                char = sys.stdin.read(1)
                if not char: core.trip('USB_LINK'); break
                kind, data = framer.feed(char)
                reply = None
                if kind == 'ERROR': core.trip(data); reply = core.status(False, data)
                elif kind == 'LINE':
                    try: packet = json.loads(data)
                    except (ValueError, TypeError): core.trip('BAD_JSON'); reply = core.status(False, 'BAD_JSON')
                    else: reply = core.handle(packet, now)
                # Apply zero immediately before a possibly blocking USB response.
                if core.state != 'ARMED' or not ALLOW_PHYSICAL_OUTPUT:
                    for pwm in pwms: pwm.duty_u16(0)
                if reply is not None:
                    for pwm in pwms: pwm.duty_u16(0)
                    sys.stdout.write(json.dumps(reply) + '\n')
            # Break-before-make signal update. This is PWM control, not a physical power disconnect.
            for pwm in pwms: pwm.duty_u16(0)
            if ALLOW_PHYSICAL_OUTPUT and core.state == 'ARMED':
                for start, value in ((0, core.left), (2, core.right)):
                    pwms[start if value >= 0 else start + 1].duty_u16(int(abs(value) * 65535 / 1000))
            wdt.feed()  # Feed only after parsing and applying the output state.
            time.sleep_ms(5)
    finally:
        for pwm in pwms:
            pwm.duty_u16(0); pwm.deinit()
        for pin in pins: pin.init(Pin.OUT, value=0)

if __name__ == '__main__': run()
