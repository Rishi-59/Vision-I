import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.scene.describer import SceneDescriber
from src.utils.env_loader import load_env


STUB_SAFETY = "Safety check complete. No immediate hazards detected."


def _write_test_png(path: Path) -> None:
    # 1x1 transparent PNG
    png_bytes = bytes(
        [
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
            0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
            0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
            0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
            0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
            0x42, 0x60, 0x82,
        ]
    )
    path.write_bytes(png_bytes)


class TestSceneDescriber(unittest.TestCase):
    def test_scene_description_single_request(self) -> None:
        load_env()
        provider = None
        model = ""
        if os.getenv("GEMINI_API_KEY"):
            provider = "gemini"
            model = os.getenv("GEMINI_TEST_MODEL", "gemini-2.0-flash")
            try:
                from google import genai  # noqa: F401
            except Exception:
                self.fail("google-genai is not installed. Run: python -m pip install google-genai")
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
            model = os.getenv("OPENAI_TEST_MODEL", "gpt-4o-mini")

        if not provider:
            self.skipTest("No API key set for GEMINI_API_KEY or OPENAI_API_KEY.")

        with tempfile.TemporaryDirectory() as tmpdir:
            image_path = Path(tmpdir) / "scene.png"
            _write_test_png(image_path)
            describer = SceneDescriber(
                provider=provider,
                model=model,
                temperature=0.2,
                max_tokens=120,
                debug=True,
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = describer.describe(str(image_path), "safety")

        self.assertTrue(result)
        if result == STUB_SAFETY:
            debug_output = stdout.getvalue().strip()
            message = "Got stub response. Check API key, quota, or provider settings."
            if debug_output:
                message = f"{message}\nDebug output:\n{debug_output}"
            self.fail(message)


if __name__ == "__main__":
    unittest.main()
