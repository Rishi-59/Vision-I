"""
Vision I - Main Entry Point

This file serves as the central controller of the system.
It initializes all modules and manages the execution flow.
"""

from src.vision.camera import Camera
from src.vision.detector import ObjectDetector
from src.decision.rules import DecisionEngine
from src.audio.tts import VoiceAssistant
from src.utils.config_loader import Config


def main():
    """
    Main execution loop for Vision I.
    """

    # Load configuration
    config = Config()

    frame_width = config.get("system", "frame_width", default=640)
    cooldown = config.get("system", "cooldown_seconds", default=3.0)
    confidence = config.get("detection", "confidence_threshold", default=0.5)
    mode = config.get("modes", "mode", default="voice")

    # Initialize system components
    camera = Camera()
    detector = ObjectDetector(confidence_threshold=confidence) # type: ignore
    decision_engine = DecisionEngine(
        frame_width=frame_width, # type: ignore
        cooldown_seconds=cooldown # type: ignore
    )
    voice = VoiceAssistant()

    print("[INFO] Vision I system started.")

    # Main loop
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        detections = detector.detect(frame)
        decision = decision_engine.evaluate(detections)

        if decision:
            if mode == "voice":
                voice.speak(decision)

            elif mode == "silent":
                print(f"[DECISION] {decision}")

            elif mode == "debug":
                print(f"[DEBUG] Decision: {decision}")
                print(f"[DEBUG] Detections: {detections}")


    camera.release()
    print("[INFO] Vision I system stopped.")


if __name__ == "__main__":
    main()
