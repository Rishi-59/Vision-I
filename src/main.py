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
from src.utils.env_loader import load_env
from src.utils.config_loader import Config
import cv2 
from collections import deque
from pathlib import Path
import time


def main():
    """
    Main execution loop for Vision I.
    """

    # Load environment variables from .env if present
    load_env(verbose=True)

    # Load configuration
    config = Config()

    frame_width = config.get("system", "frame_width", default=640)
    cooldown = config.get("system", "cooldown_seconds", default=3.0)
    confidence = config.get("detection", "confidence_threshold", default=0.5)
    mode = config.get("modes", "mode", default="voice")
    scene_cooldown = config.get("scene_description", "cooldown_seconds", default=10.0)
    scene_cache_dir = config.get("scene_description", "cache_dir", default="cache")
    scene_provider = config.get("scene_description", "provider", default="stub")
    scene_model = config.get("scene_description", "model", default="")
    scene_temperature = config.get("scene_description", "temperature", default=0.3)
    scene_max_tokens = config.get("scene_description", "max_tokens", default=160)
    scene_debug = config.get("scene_description", "debug", default=False)
    scene_min_interval = config.get(
        "scene_description", "rate_limit", "min_interval_seconds", default=5.0
    )
    scene_max_per_minute = config.get(
        "scene_description", "rate_limit", "max_per_minute", default=6
    )

    # Initialize system components
    camera = Camera()
    detector = ObjectDetector(confidence_threshold=confidence) # type: ignore
    decision_engine = DecisionEngine(
        frame_width=frame_width, # type: ignore
        cooldown_seconds=cooldown # type: ignore
    )
    voice = VoiceAssistant()
    scene_capture = SceneCapture(cache_dir=Path(scene_cache_dir)) # type: ignore
    scene_describer = SceneDescriber(
        provider=scene_provider, # type: ignore
        model=scene_model, # type: ignore
        temperature=scene_temperature, # type: ignore
        max_tokens=scene_max_tokens, # type: ignore
        debug=scene_debug, # type: ignore
    )
    last_scene_time = 0.0
    last_scene_key_time = 0.0
    scene_key_debounce = 0.5
    scene_request_times = deque()

    print("[INFO] Vision I system started.")

    print("=" * 50)
    print("Vision I - AI-Based Intelligent Visual Guidance System")
    print(f"Mode          : {mode.upper()}") # type: ignore
    print(f"Frame Width   : {frame_width}")
    print(f"Cooldown (s)  : {cooldown}")
    print(f"Scene Cooldown (s): {scene_cooldown}")
    print(f"Scene Provider: {scene_provider} | Model: {scene_model}")
    print(f"Confidence    : {confidence}")
    print("Press 'q' to safely exit")
    print("Press 'd' for safety description, 'a' for awareness, 'c' for companion mode")
    print("=" * 50)

    # Main loop
    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # SHOW frame (required for key events)
        cv2.imshow("Vision I - Live Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[INFO] Exit key pressed. Shutting down...")
            break
        if key in (ord('d'), ord('a'), ord('c')):
            now = time.time()
            if now - last_scene_key_time < scene_key_debounce:
                continue
            last_scene_key_time = now
            if now - last_scene_time < scene_min_interval: # type: ignore
                remaining = scene_min_interval - (now - last_scene_time) # type: ignore
                print(f"[SCENE] Rate limit active. Try again in {remaining:.1f}s.")
                continue
            window_start = now - 60.0
            while scene_request_times and scene_request_times[0] < window_start:
                scene_request_times.popleft()
            if scene_max_per_minute and len(scene_request_times) >= scene_max_per_minute: # type: ignore
                print("[SCENE] Rate limit active. Max per minute reached.")
                continue
            if now - last_scene_time < scene_cooldown: # type: ignore
                remaining = scene_cooldown - (now - last_scene_time) # type: ignore
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
                    scene_request_times.append(now)

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
