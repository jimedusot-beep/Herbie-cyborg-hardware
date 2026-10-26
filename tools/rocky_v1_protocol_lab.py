"""Simulation-only host/controller boundary; not Rocky wire protocol or motor code.

Architecture inspired by cgro00/desk-robot v1.0 (MIT). No upstream code copied.
No hardware, servo pins, network, or motor control.
"""
from dataclasses import dataclass
from typing import Any

VERSION = "herbie.hardware.lab/0"
ACTIONS = {"MOVE", "STOP", "CLEAR_FAULT", "ARM", "DISCONNECT", "STATUS"}


@dataclass
class LabController:
    """Fail-closed lab state machine. Physical actuation is impossible."""
    state: str = "DISARMED"
    last_sequence: int = -1
    connected: bool = False

    def reply(self, ok: bool, reason: str = "") -> dict:
        result = {"ok": ok, "state": self.state, "simulated": True}
        if reason:
            result["reason"] = reason
        return result

    def handle(self, message: Any) -> dict:
        if not isinstance(message, dict):
            return self.reply(False, "invalid-message")
        action = message.get("action")
        # Emergency STOP is unconditional, including on bad/replayed frames.
        # This is a software lab property, NOT a physical emergency stop.
        if action == "STOP":
            self.state = "FAULT_LATCHED"
            self.connected = False
            return self.reply(True)
        if message.get("version") != VERSION:
            return self.reply(False, "version-mismatch")
        seq = message.get("seq")
        if action not in ACTIONS or type(seq) is not int or seq < 0:
            return self.reply(False, "invalid-command")
        if seq <= self.last_sequence:
            return self.reply(False, "stale-sequence")
        self.last_sequence = seq
        if action == "DISCONNECT":
            self.state = "FAULT_LATCHED"
            self.connected = False
            return self.reply(True)
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
            return self.reply(True)
        return self.reply(False, "invalid-command")
