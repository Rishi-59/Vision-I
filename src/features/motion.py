"""
Motion estimation module for Vision I.

Determines whether a detected object is approaching,
moving away, or stationary based on bounding box size
changes across frames.
"""


class MotionEstimator:
    def __init__(self, threshold: float = 0.05):
        """
        Initialize motion estimator.

        :param threshold: Minimum relative change to detect motion
        """
        self.previous_sizes = {}
        self.threshold = threshold

    def estimate(self, object_id, bbox):
        """
        Estimate motion state of an object.

        :param object_id: Unique identifier for the object
        :param bbox: Tuple (x1, y1, x2, y2)
        :return: 'APPROACHING', 'MOVING_AWAY', or 'STATIONARY'
        """
        if not bbox or len(bbox) != 4:
            return None

        x1, y1, x2, y2 = bbox
        current_size = (x2 - x1) * (y2 - y1)

        if current_size <= 0:
            return None

        if object_id not in self.previous_sizes:
            self.previous_sizes[object_id] = current_size
            return "STATIONARY"

        previous_size = self.previous_sizes[object_id]
        self.previous_sizes[object_id] = current_size

        change_ratio = (current_size - previous_size) / previous_size

        if change_ratio > self.threshold:
            return "APPROACHING"
        elif change_ratio < -self.threshold:
            return "MOVING_AWAY"
