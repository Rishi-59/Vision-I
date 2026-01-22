"""
Logging utility for Vision I.

Stores decision events for adaptive learning and evaluation.
"""

import time
import json
from pathlib import Path


class DecisionLogger:
    def __init__(self, log_file="logs/decisions.jsonl"):
        self.log_path = Path(log_file)
        self.log_path.parent.mkdir(exist_ok=True)

    def log(self, label, distance, direction, motion, decision):
        event = {
            "timestamp": time.time(),
            "label": label,
            "distance": distance,
            "direction": direction,
            "motion": motion,
            "decision": decision
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
