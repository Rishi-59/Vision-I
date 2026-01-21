"""
Direction estimation module for Vision I.

Determines whether a detected object lies on the
left, center, or right region of the frame.
"""


class DirectionEstimator:
    def __init__(self, frame_width: int):
        """
        Initialize direction estimator.

        :param frame_width: Width of the video frame in pixels
        """
        self.frame_width = frame_width

    def estimate(self, bbox):
        """
        Estimate direction based on bounding box center.

        :param bbox: Tuple (x1, y1, x2, y2)
        :return: Direction as 'LEFT', 'CENTER', or 'RIGHT'
        """
        if not bbox or len(bbox) != 4:
            return None

        x1, _, x2, _ = bbox
        object_center_x = (x1 + x2) / 2

        left_boundary = self.frame_width / 3
        right_boundary = 2 * self.frame_width / 3

        if object_center_x < left_boundary:
            return "LEFT"
        elif object_center_x > right_boundary:
            return "RIGHT"
        else:
            return "CENTER"
