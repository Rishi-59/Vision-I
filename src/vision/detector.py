"""
Object detection module for Vision I.

Uses YOLOv8 for real-time object detection.
"""

from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, model_path: str = "yolov8n.pt"):
        """
        Initialize YOLO object detector.

        :param model_path: Path to YOLO model
        """
        self.model = YOLO(model_path)

    def detect(self, frame):
        """
        Perform object detection on a given frame.

        :param frame: Input video frame
        :return: List of detected objects
        """
        results = self.model(frame, verbose=False)

        detections = []

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                detections.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2)
                })

        return detections
