"""
Alert escalation manager for Vision I.

Determines severity and handling rules for alerts
based on decision content.
"""

LOW = 1
MEDIUM = 2
HIGH = 3
CRITICAL = 4


class AlertManager:
    def __init__(self):
        self.severity_map = {
            "Obstacle on left": LOW,
            "Obstacle on right": LOW,
            "Obstacle ahead": HIGH,
            "Warning": CRITICAL,
        }

    def classify(self, decision: str) -> int:
        """
        Determine severity level of a decision.
        """
        if not decision:
            return LOW

        for key, severity in self.severity_map.items():
            if key.lower() in decision.lower():
                return severity

        return MEDIUM

    def should_bypass_cooldown(self, severity: int) -> bool:
        """
        Determine whether cooldown should be bypassed.
        """
        return severity >= CRITICAL

    def should_repeat(self, severity: int) -> bool:
        """
        Determine whether alert should repeat aggressively.
        """
        return severity >= HIGH
