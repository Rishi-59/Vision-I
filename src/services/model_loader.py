"""
Loads YOLO model once at startup.
"""

import os

from ultralytics import YOLO


_model = None


def load_model():

    global _model

    if _model is None:

        model_path = os.getenv(
            "YOLO_MODEL_PATH",
            "yolov8n.pt"
        )

        _model = YOLO(model_path)

        print(f"[INFO] YOLO model loaded: {model_path}")


def get_model():

    if _model is None:
        raise RuntimeError(
            "Model not loaded. Call load_model() first."
        )

    return _model