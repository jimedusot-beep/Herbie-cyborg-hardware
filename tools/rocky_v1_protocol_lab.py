"""Simulation-only host/controller boundary; not Rocky wire protocol or motor code.

Architecture inspired by cgro00/desk-robot v1.0 (MIT). No upstream code copied.
No hardware, servo pins, network, or motor control.
"""
from dataclasses import dataclass
from typing import Any

VERSION = "herbie.hardware.lab/0"
MAX_SEQUENCE = 2_147_483_647  # Exhaustion requires an explicitly new lab session.
ACTIONS = {"MOVE", "STOP", "CLEAR_FAULT", "ARM", "DISCONNECT", "STATUS"}


@dataclass
class LabController:
    """Fail-closed lab state machine. Physical actuation is impossible."""
    state: str = "DISARMED"
    last_sequence: int = -1
    connected: bool = False

    def reply(self, ok: bool, reason: str = "", *, kind: str = "ack") -> dict:
        result = {
            "version": VERSION, "kind": kind, "ok": ok,
            "state": self.state, "simulated": True,
            "last_sequence": self.last_sequence,
        }
        if reason:
            result["reason"] = reason
        return result

    def handle(self, message: Any) -> dict:
        if not isinstance(message, dict):
            return self.reply(False, "invalid-message")
        action = message.get("action")
        # Reject unhashable or non-string actions before set membership checks.
        if type(action) is not str:
            return self.reply(False, "invalid-command")
        # A recognizable STOP or trusted disconnect event always latches,
        # even with stale/absent sequence and version. Simulation only:
        # this is NOT a physical emergency stop or a network transport.
        if action in ("STOP", "DISCONNECT"):
            self.state = "FAULT_LATCHED"
            self.connected = False
            return self.reply(True)
        if message.get("version") != VERSION:
            return self.reply(False, "version-mismatch")
        seq = message.get("seq")
        if action not in ACTIONS or type(seq) is not int or not 0 <= seq <= MAX_SEQUENCE:
            return self.reply(False, "invalid-command")
        if seq <= self.last_sequence:
            return self.reply(False, "stale-sequence")
        self.last_sequence = seq
        if action == "CLEAR_FAULT":
            if self.state != "FAULT_LATCHED":
                return self.reply(False, "no-fault")
            self.state = "DISARMED"
            return self.reply(True)
        if action == "ARM":
            return self.reply(False, "hardware-not-verified")
        if action == "MOVE":
            if (type(message.get("degrees")) not in (int, float)
                    or not -180 <= message["degrees"] <= 180):
                return self.reply(False, "invalid-move")
            return self.reply(False, "actuation-disabled")
        if action == "STATUS":
            return self.reply(True, kind="status")
        return self.reply(False, "invalid-command")
