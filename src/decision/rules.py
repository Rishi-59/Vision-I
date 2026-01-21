"""
Decision engine for Vision I.

Combines feature extraction results (distance, direction, motion)
and applies rule-based logic to generate navigation guidance.
"""

import time

from src.features.distance import DistanceEstimator
from src.features.direction import DirectionEstimator
from src.features.motion import MotionEstimator


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
        Evaluate detected objects and return a navigation decision.

        :param detections: List of detected objects
        :return: Decision message (str) or None
        """

        current_time = time.time()
        if current_time - self.last_spoken_time < self.cooldown_seconds:
            return None

        if not detections:
            return None

        for idx, obj in enumerate(detections):
            label = obj.get("label")
            bbox = obj.get("bbox")

            # Feature extraction
            distance = self.distance_estimator.estimate(bbox)
            direction = self.direction_estimator.estimate(bbox)
            motion = self.motion_estimator.estimate(str(idx), bbox)

            # --- RULES (simple & explainable) ---

            # Rule 1: Approaching object in front
            if motion == "APPROACHING" and direction == "CENTER":
                self.last_spoken_time = time.time()
                return f"Warning. {label} approaching ahead."

            # Rule 2: Close obstacle in center
            if distance is not None and distance < 1.5 and direction == "CENTER":
                self.last_spoken_time = time.time()
                return f"Obstacle ahead. Please stop."

            # Rule 3: Obstacle on sides
            if direction == "LEFT" and distance is not None and distance < 2.0:
                self.last_spoken_time = time.time()
                return "Obstacle on left. Move right."

            elif direction == "RIGHT" and distance is not None and distance < 2.0:
                self.last_spoken_time = time.time()
                return "Obstacle on right. Move left."


        return None
