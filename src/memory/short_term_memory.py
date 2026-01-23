"""
Short-term memory for Vision I.

Remembers recently alerted objects to prevent
repeated alerts for the same obstacle.
"""

import time
import math


class ShortTermMemory:
    def __init__(self, ttl_seconds=3.0, distance_threshold=50):
        """
        :param ttl_seconds: How long to remember objects
        :param distance_threshold: Pixel distance to consider same object
        """
        self.ttl = ttl_seconds
        self.dist_thresh = distance_threshold
        self.memory = []

    def _center(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def _distance(self, c1, c2):
        return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    def is_recent(self, label, bbox):
        """
        Check if object was recently alerted.
        """
        now = time.time()
        center = self._center(bbox)

        for obj in self.memory:
            if obj["label"] == label:
                if self._distance(center, obj["center"]) < self.dist_thresh:
                    if now - obj["time"] < self.ttl:
                        return True
        return False

    def update(self, label, bbox):
        """
        Update memory with new alert.
        """
        now = time.time()
        center = self._center(bbox)

        # Remove expired memory
        self.memory = [
            obj for obj in self.memory
            if now - obj["time"] < self.ttl
        ]

        self.memory.append({
            "label": label,
            "center": center,
            "time": now
        })
