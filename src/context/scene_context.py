"""
Scene context inference for Vision I.

Infers environment context based on detected objects
and motion patterns.
"""


class SceneContext:
    def __init__(self):
        self.current_context = "CLEAR"

    def infer(self, detections, motions=None):
        """
        Infer scene context.

        :param detections: List of detection dicts
        :param motions: Optional list of motion states
        :return: Context string
        """

        if not detections:
            self.current_context = "CLEAR"
            return self.current_context

        labels = [obj.get("label", "") for obj in detections]
        num_objects = len(labels)

        # Vehicle presence → OUTDOOR
        if any(label in ["car", "bus", "truck", "motorcycle"] for label in labels):
            self.current_context = "OUTDOOR"
            return self.current_context

        # Many people → CROWDED
        if labels.count("person") >= 4:
            self.current_context = "CROWDED"
            return self.current_context

        # Default fallback
        self.current_context = "INDOOR"
        return self.current_context

    def get(self):
        return self.current_context
