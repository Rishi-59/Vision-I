"""
Text-to-Speech module for Vision I.

Handles voice output for system decisions.
"""

import pyttsx3


class VoiceAssistant:
    def __init__(self):
        """
        Initialize text-to-speech engine.
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)

    def speak(self, message: str):
        """
        Convert text message to speech.

        :param message: Text to be spoken
        """
        if not message:
            return

        print(f"[VOICE] {message}")
        self.engine.say(message)
        self.engine.runAndWait()
