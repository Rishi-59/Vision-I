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
import cv2 


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

    print("=" * 50)
    print("Vision I - AI-Based Intelligent Visual Guidance System")
    print(f"Mode          : {mode.upper()}") # type: ignore
    print(f"Frame Width   : {frame_width}")
    print(f"Cooldown (s)  : {cooldown}")
    print(f"Confidence    : {confidence}")
    print("Press 'q' to safely exit")
    print("=" * 50)

    # Main loop
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # SHOW frame (required for key events)
        cv2.imshow("Vision I - Live Feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Exit key pressed. Shutting down...")
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
    cv2.destroyAllWindows()
    print("[INFO] Vision I system stopped safely.")



if __name__ == "__main__":
    main()
