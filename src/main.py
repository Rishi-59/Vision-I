"""
Vision I - Main Entry Point

This file serves as the central controller of the system.
It initializes all modules and manages the execution flow.
"""

from src.vision.camera import Camera
from src.vision.detector import ObjectDetector
from src.decision.rules import DecisionEngine
from src.audio.tts import VoiceAssistant


def main():
    """
    Main execution loop for Vision I.
    """

    # Initialize system components
    camera = Camera()
    detector = ObjectDetector()
    decision_engine = DecisionEngine(frame_width=640)
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
            voice.speak(decision)

    camera.release()
    print("[INFO] Vision I system stopped.")


if __name__ == "__main__":
    main()
