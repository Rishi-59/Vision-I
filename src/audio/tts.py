"""
Text-to-Speech module for Vision I.

Handles voice output safely in a real-time loop.
"""

import pyttsx3


class VoiceAssistant:
    def __init__(self):
        """
        Initialize voice assistant.
        """
        self.engine = None

    def speak(self, message: str):
        """
        Convert text message to speech safely.

        :param message: Text to be spoken
        """
        if not message:
            return

        try:
            if self.engine is None:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 160)

            print(f"[VOICE] {message}")
            self.engine.say(message)
            self.engine.runAndWait()

            # IMPORTANT: reset engine for next cycle
            self.engine.stop()
            self.engine = None

        except Exception as e:
            print(f"[TTS ERROR] {e}")
