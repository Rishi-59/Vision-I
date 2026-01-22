"""
Decision engine for Vision I.

Combines feature extraction results (distance, direction, motion)
and applies rule-based logic to generate navigation guidance.
"""

import time

from src.features.distance import DistanceEstimator
from src.features.direction import DirectionEstimator
from src.features.motion import MotionEstimator

CRITICAL = 3
HIGH = 2
LOW = 1

class DecisionEngine:
    def __init__(self, frame_width: int = 640, cooldown_seconds: float = 3.0):
        """
        Initialize the decision engine and feature estimators.

        :param frame_width: Width of video frame in pixels
        """
        self.distance_estimator = DistanceEstimator()
        self.direction_estimator = DirectionEstimator(frame_width)
        self.motion_estimator = MotionEstimator()

        self.cooldown_seconds = cooldown_seconds
        self.last_spoken_time = 0


    def evaluate(self, detections):
        """
        Evaluate detected objects and return a prioritized navigation decision.

        :param detections: List of detected objects
        :return: Decision message (str) or None
        """

        if not detections:
            return None

        best_decision = None
        best_priority = 0
        current_time = time.time()

        for idx, obj in enumerate(detections):
            label = obj.get("label")
            bbox = obj.get("bbox")

            # Feature extraction
            distance = self.distance_estimator.estimate(bbox)
            direction = self.direction_estimator.estimate(bbox)
            motion = self.motion_estimator.estimate(str(idx), bbox)

            # --- PRIORITY RULES ---

            # CRITICAL: Approaching object in center
            if motion == "APPROACHING" and direction == "CENTER":
                best_decision = f"Warning. {label} approaching ahead."
                best_priority = CRITICAL
                break  # Nothing beats this

            # HIGH: Close obstacle in center
            if distance is not None and distance < 1.5 and direction == "CENTER":
                if HIGH > best_priority:
                    best_decision = "Obstacle ahead. Please stop."
                    best_priority = HIGH

            # LOW: Side obstacles
            if direction == "LEFT" and distance is not None and distance < 2.0:
                if LOW > best_priority:
                    best_decision = "Obstacle on left. Move right."
                    best_priority = LOW

            elif direction == "RIGHT" and distance is not None and distance < 2.0:
                if LOW > best_priority:
                    best_decision = "Obstacle on right. Move left."
                    best_priority = LOW

        if best_decision:
            # Allow critical alerts to bypass cooldown
            if best_priority == CRITICAL:
                self.last_spoken_time = time.time()
                return best_decision

            # Enforce cooldown for non-critical alerts
            if current_time - self.last_spoken_time >= self.cooldown_seconds:
                self.last_spoken_time = time.time()
                return best_decision

        return None

