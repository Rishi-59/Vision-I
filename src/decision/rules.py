"""
Decision engine for Vision I.

Combines feature extraction results (distance, direction, motion),
adaptive thresholds, metrics, logging, and scene context
to generate prioritized navigation guidance.
"""

import time

from src.learning.adaptive_rules import AdaptiveThresholds
from src.features.distance import DistanceEstimator
from src.features.direction import DirectionEstimator
from src.features.motion import MotionEstimator
from src.utils.logger import DecisionLogger
from src.utils.metrics import MetricsCollector
from src.context.scene_context import SceneContext

CRITICAL = 3
HIGH = 2
LOW = 1


class DecisionEngine:
    def __init__(self, frame_width: int = 640, cooldown_seconds: float = 3.0):
        """
        Initialize the decision engine and feature estimators.
        """

        self.distance_estimator = DistanceEstimator()
        self.direction_estimator = DirectionEstimator(frame_width)
        self.motion_estimator = MotionEstimator()

        self.cooldown_seconds = cooldown_seconds
        self.last_spoken_time = 0

        # Phase 3
        self.adaptive = AdaptiveThresholds()
        self.metrics = MetricsCollector()
        self.logger = DecisionLogger()

        # Phase 5
        self.context = SceneContext()

    # --------------------------------------------------

    def final_report(self):
        """
        Print final evaluation metrics.
        """
        print("\n========== FINAL SYSTEM REPORT ==========")
        print(f"Total alerts           : {len(self.metrics.alert_times)}")
        print(f"Alerts/min (last 60s)  : {self.metrics.alerts_per_minute():.2f}")
        print(f"Avg response time (s)  : {self.metrics.average_response_time():.2f}")

        most_common = self.metrics.most_common_object()
        if most_common:
            print(f"Most common object     : {most_common[0]} ({most_common[1]} alerts)")
        else:
            print("Most common object     : None")

        print("========================================\n")

    # --------------------------------------------------

    def evaluate(self, detections):
        """
        Evaluate detected objects and return a prioritized navigation decision.
        """

        if not detections:
            return None

        # ---------- Phase 5.1: Context inference ----------
        context = self.context.infer(detections)

        # ---------- Adaptive thresholds ----------
        center_threshold = self.adaptive.get_center_threshold()
        side_threshold = self.adaptive.get_side_threshold()

        # Context-based modulation
        if context == "CROWDED":
            center_threshold += 0.5
            side_threshold += 0.5
        elif context == "OUTDOOR":
            center_threshold -= 0.3

        # Safety clamp
        center_threshold = max(center_threshold, 0.5)
        side_threshold = max(side_threshold, 0.5)

        best_decision = None
        best_priority = 0
        best_context = {}

        current_time = time.time()

        # ---------- Rule evaluation ----------
        for idx, obj in enumerate(detections):
            label = obj.get("label")
            bbox = obj.get("bbox")

            distance = self.distance_estimator.estimate(bbox)
            direction = self.direction_estimator.estimate(bbox)
            motion = self.motion_estimator.estimate(str(idx), bbox)

            # CRITICAL: Approaching object ahead
            if motion == "APPROACHING" and direction == "CENTER":
                best_decision = f"Warning. {label} approaching ahead."
                best_priority = CRITICAL
                best_context = {
                    "label": label,
                    "distance": distance,
                    "direction": direction,
                    "motion": motion,
                }
                break  # highest priority possible

            # HIGH: Close obstacle in center
            if (
                distance is not None
                and distance < center_threshold
                and direction == "CENTER"
            ):
                if HIGH > best_priority:
                    best_decision = "Obstacle ahead. Please stop."
                    best_priority = HIGH
                    best_context = {
                        "label": label,
                        "distance": distance,
                        "direction": direction,
                        "motion": motion,
                    }

            # LOW: Side obstacles
            if (
                direction == "LEFT"
                and distance is not None
                and distance < side_threshold
            ):
                if LOW > best_priority:
                    best_decision = "Obstacle on left. Move right."
                    best_priority = LOW
                    best_context = {
                        "label": label,
                        "distance": distance,
                        "direction": direction,
                        "motion": motion,
                    }

            elif (
                direction == "RIGHT"
                and distance is not None
                and distance < side_threshold
            ):
                if LOW > best_priority:
                    best_decision = "Obstacle on right. Move left."
                    best_priority = LOW
                    best_context = {
                        "label": label,
                        "distance": distance,
                        "direction": direction,
                        "motion": motion,
                    }

        # ---------- Final decision handling ----------
        if best_decision:
            # Adaptive learning
            self.adaptive.update(best_decision)

            # Metrics
            self.metrics.record(best_context.get("label"))

            # Logging
            self.logger.log(
                label=best_context.get("label"),
                distance=best_context.get("distance"),
                direction=best_context.get("direction"),
                motion=best_context.get("motion"),
                decision=best_decision,
            )

            # Cooldown logic
            if best_priority == CRITICAL:
                self.last_spoken_time = time.time()
                return best_decision

            if current_time - self.last_spoken_time >= self.cooldown_seconds:
                self.last_spoken_time = time.time()
                return best_decision

        return None
