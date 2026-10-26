"""Isolated H.E.R.B.I.E. host/controller protocol experiment.

Inspired by the host/controller separation of cgro00/desk-robot v1.0
(MIT license; no upstream source code copied). This is NOT Rocky's wire
protocol and is NOT a physical motor driver.
"""
from dataclasses import dataclass
from typing import Any

VERSION = "herbie.hardware.lab/0"
MOVEMENT = {"MOVE"}
ACTIONS = MOVEMENT | {"STOP", "CLEAR_FAULT", "ARM", "DISCONNECT", "STATUS"}


@dataclass
class LabController:
    """Simulation only. All movement commands return acceptance, not motion."""
    state: str = "DISARMED"
    last_sequence: int = -1
    connected: bool = False

    def handle(self, message: Any) -> dict:
        if not isinstance(message, dict):
            return {"ok": False, "reason": "invalid-message", "state": self.state}
        if message.get("version") != VERSION:
            return {"ok": False, "reason": "version-mismatch", "state": self.state}
        action = message.get("action")
        seq = message.get("seq")
        if action not in ACTIONS or type(seq) is not int or seq < 0:
            return {"ok": False, "reason": "invalid-command", "state": self.state}
        if seq <= self.last_sequence:
            return {"ok": False, "reason": "stale-sequence", "state": self.state}
        self.last_sequence = seq
        if action in {"STOP", "DISCONNECT"}:
            self.state = "FAULT_LATCHED"
            self.connected = False
        elif action == "CLEAR_FAULT":
            if self.state != "FAULT_LATCHED":
                return {"ok": False, "reason": "no-fault", "state": self.state}
            self.state = "DISARMED"
        elif action == "ARM":
            # No ARM permission in this lab: hardware readiness is unknown.
            return {"ok": False, "reason": "hardware-not-verified", "state": self.state}
        elif action == "MOVE":
            return {"ok": False, "reason": "actuation-disabled", "state": self.state}
        return {"ok": True, "state": self.state, "simulated": True}
