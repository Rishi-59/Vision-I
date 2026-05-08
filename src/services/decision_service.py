"""
Decision service wrapper.
"""

from src.decision.rules import DecisionEngine


decision_engine = DecisionEngine()


def run_decision(
    detections,
    frame_width: int = 640,
    user_mode: str = "normal"
):

    guidance = decision_engine.evaluate(
        detections
    )

    severity = "LOW"

    if guidance:

        text = guidance.lower()

        if "warning" in text:
            severity = "CRITICAL"

        elif "stop" in text:
            severity = "HIGH"

        else:
            severity = "MEDIUM"

    return {
        "guidance": guidance,
        "severity": severity,
        "speak": guidance is not None,
    }