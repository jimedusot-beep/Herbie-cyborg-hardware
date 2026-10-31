"""Deterministic tests for the isolated, non-actuating protocol lab."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rocky_v1_protocol_lab import LabController, VERSION


def cmd(seq, action, **extra):
    return {"version": VERSION, "seq": seq, "action": action, **extra}


class RockyV1AdaptationTests(unittest.TestCase):
    def test_starts_disarmed_and_rejects_motion(self):
        c = LabController()
        self.assertEqual(c.state, "DISARMED")
        self.assertEqual(c.handle(cmd(1, "MOVE", degrees=10))["reason"], "actuation-disabled")

    def test_arm_never_authorized(self):
        self.assertEqual(LabController().handle(cmd(1, "ARM"))["reason"], "hardware-not-verified")

    def test_stop_latches_and_clear_does_not_move(self):
        c = LabController()
        self.assertEqual(c.handle(cmd(1, "STOP"))["state"], "FAULT_LATCHED")
        self.assertEqual(c.handle(cmd(2, "MOVE", degrees=30))["reason"], "actuation-disabled")
        self.assertEqual(c.handle(cmd(3, "CLEAR_FAULT"))["state"], "DISARMED")
        self.assertEqual(c.handle(cmd(4, "MOVE", degrees=30))["reason"], "actuation-disabled")

    def test_disconnect_latches(self):
        self.assertEqual(LabController().handle(cmd(1, "DISCONNECT"))["state"], "FAULT_LATCHED")

    def test_stale_stop_always_latches(self):
        c = LabController()
        c.handle(cmd(10, "STATUS"))
        self.assertEqual(c.handle(cmd(1, "STOP"))["state"], "FAULT_LATCHED")
        self.assertEqual(c.handle({"action": "STOP"})["state"], "FAULT_LATCHED")

    def test_replay_and_malformed_rejected(self):
        c = LabController()
        c.handle(cmd(3, "STATUS"))
        self.assertEqual(c.handle(cmd(3, "CLEAR_FAULT"))["reason"], "stale-sequence")
        self.assertEqual(c.handle(cmd(2, "CLEAR_FAULT"))["reason"], "stale-sequence")
        self.assertEqual(c.handle({"version": VERSION, "seq": True, "action": "ARM"})["reason"], "invalid-command")
        self.assertEqual(c.handle("MOVE")["reason"], "invalid-message")

    def test_invalid_moves(self):
        for value in (None, "15", True, 999, float("nan")):
            self.assertEqual(LabController().handle(cmd(1, "MOVE", degrees=value))["reason"], "invalid-move")

    def test_version_mismatch(self):
        self.assertEqual(LabController().handle({"version": "1", "seq": 1, "action": "MOVE"})["reason"], "version-mismatch")

    def test_status_reports_state(self):
        c = LabController()
        self.assertEqual(c.handle(cmd(1, "STATUS")), {"ok": True, "state": "DISARMED", "simulated": True})


if __name__ == "__main__":
    unittest.main()
