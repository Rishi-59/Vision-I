"""
Detection service.
"""

from src.context.scene_context import SceneContext
from src.features.direction import DirectionEstimator
from src.features.distance import DistanceEstimator
from src.features.motion import MotionEstimator
from src.services.model_loader import get_model


distance_estimator = DistanceEstimator()

motion_estimator = MotionEstimator()

scene_context = SceneContext()


def run_detection(
    frame,
    frame_width: int = 640,
    confidence_threshold: float = 0.5
):

    model = get_model()

    direction_estimator = DirectionEstimator(
        frame_width
    )

    results = model(
        frame,
        verbose=False
    )

    detections = []

    for result in results:

        boxes = result.boxes

        if boxes is None:
            continue

        for idx, box in enumerate(boxes):

            x1, y1, x2, y2 = (
                box.xyxy[0].tolist()
            )

            confidence = float(box.conf[0])

            if confidence < confidence_threshold:
                continue

            class_id = int(box.cls[0])

            label = model.names[class_id]

            bbox = (
                x1,
                y1,
                x2,
                y2
            )

            distance = distance_estimator.estimate(
                bbox
            )

            direction = direction_estimator.estimate(
                bbox
            )

            motion = motion_estimator.estimate(
                str(idx),
                bbox
            )

            detections.append({
                "label": label,
                "confidence": round(confidence, 3),
                "bbox": bbox,
                "distance": distance,
                "direction": direction,
                "motion": motion,
            })

    context = scene_context.infer(
        detections
    )

    return {
        "detections": detections,
        "scene_context": context,
    }