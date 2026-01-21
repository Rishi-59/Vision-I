"""
Distance estimation module for Vision I.

Estimates relative distance of detected objects using
bounding box dimensions from a monocular camera.
"""

class DistanceEstimator:
    def __init__(self, reference_height: float = 170.0):
        """
        Initialize the distance estimator.

        :param reference_height: Average object height in cm
                                 (default assumes a human)
        """
        self.reference_height = reference_height

    def estimate(self, bbox):
        """
        Estimate relative distance based on bounding box height.

        :param bbox: Tuple (x1, y1, x2, y2)
        :return: Relative distance value (float) or None
        """
        if not bbox or len(bbox) != 4:
            return None

        x1, y1, x2, y2 = bbox
        box_height = y2 - y1

        if box_height <= 0:
            return None

        # Simple inverse relationship for relative distance
        distance = self.reference_height / box_height
        return distance
