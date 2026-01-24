import os
import cv2
from datetime import datetime


class SceneCapture:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def capture(self, frame) -> str:
        """
        Capture a frame and save it to cache.
        Returns the saved file path.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scene_{timestamp}.jpg"
        path = os.path.join(self.cache_dir, filename)

        cv2.imwrite(path, frame)
        return path
