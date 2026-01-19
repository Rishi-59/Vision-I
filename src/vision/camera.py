"""
Camera module for Vision I.

Handles video capture and frame retrieval.
"""

import cv2


class Camera:
    def __init__(self, source: int = 0):
        """
        Initialize the camera.

        :param source: Camera source index (default is 0)
        """
        self.source = source
        self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to access the camera")

    def get_frame(self):
        """
        Capture a single frame from the camera.

        :return: Frame if successful, else None
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        """
        Release the camera resource.
        """
        self.cap.release()
