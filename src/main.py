"""
Vision I - Main Entry Point

This file serves as the central controller of the system.
It initializes all modules and manages the execution flow.
"""

from src.vision.camera import Camera
from src.vision.detector import ObjectDetector
from src.decision.rules import DecisionEngine
from src.audio.tts import VoiceAssistant
from src.scene.capture import SceneCapture
from src.scene.describer import SceneDescriber
from src.utils.config_loader import Config
import cv2 
from pathlib import Path
import time


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
    scene_cooldown = config.get("scene_description", "cooldown_seconds", default=10.0)
    scene_cache_dir = config.get("scene_description", "cache_dir", default="cache")

    # Initialize system components
    camera = Camera()
    detector = ObjectDetector(confidence_threshold=confidence) # type: ignore
    decision_engine = DecisionEngine(
        frame_width=frame_width, # type: ignore
        cooldown_seconds=cooldown # type: ignore
    )
    voice = VoiceAssistant()
    scene_capture = SceneCapture(cache_dir=Path(scene_cache_dir))
    scene_describer = SceneDescriber()
    last_scene_time = 0.0

    print("[INFO] Vision I system started.")

    print("=" * 50)
    print("Vision I - AI-Based Intelligent Visual Guidance System")
    print(f"Mode          : {mode.upper()}") # type: ignore
    print(f"Frame Width   : {frame_width}")
    print(f"Cooldown (s)  : {cooldown}")
    print(f"Scene Cooldown (s): {scene_cooldown}")
    print(f"Confidence    : {confidence}")
    print("Press 'q' to safely exit")
    print("Press 'd' for safety description, 'a' for awareness, 'c' for companion mode")
    print("=" * 50)

    # Main loop
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        key = cv2.waitKey(1) & 0xFF
        # Press 'd' to capture scene
        if key == ord('d'):
            path = scene_capture.capture(frame)
            print(f"[INFO] Scene captured: {path}")


        # SHOW frame (required for key events)
        cv2.imshow("Vision I - Live Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[INFO] Exit key pressed. Shutting down...")
            break
        if key in (ord('d'), ord('a'), ord('c')):
            now = time.time()
            if now - last_scene_time < scene_cooldown:
                remaining = scene_cooldown - (now - last_scene_time)
                print(f"[SCENE] Cooldown active. Try again in {remaining:.1f}s.")
            else:
                mode_map = {
                    ord('d'): "safety",
                    ord('a'): "awareness",
                    ord('c'): "companion",
                }
                scene_mode = mode_map[key]
                image_path = scene_capture.capture(frame)
                if image_path is None:
                    print("[SCENE] Failed to capture scene.")
                else:
                    description = scene_describer.describe(str(image_path), scene_mode)
                    voice.speak(description)
                    last_scene_time = now

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

    decision_engine.final_report()

    camera.release()
    cv2.destroyAllWindows()
    print("[INFO] Vision I system stopped safely.")



if __name__ == "__main__":
    main()
