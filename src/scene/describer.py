"""
Scene description for Vision I.

Integrates with a vision-capable LLM when configured, otherwise falls back to
simple canned responses.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SceneDescriber:
    provider: str = "stub"
    model: str = ""
    temperature: float = 0.3
    max_tokens: int = 160
    timeout_seconds: float = 20.0
    debug: bool = False

    def describe(self, image_path: str, mode: str) -> str:
        mode = mode.lower()
        prompt = self._build_prompt(mode)
        if prompt is None:
            return "Scene description mode not recognized."

        provider = (self.provider or "stub").lower()
        if provider == "openai":
            return self._describe_openai(image_path, prompt, mode)
        if provider == "gemini":
            return self._describe_gemini(image_path, prompt, mode)

        return self._describe_stub(mode)

    def _build_prompt(self, mode: str) -> Optional[str]:
        if mode == "safety":
            return (
                "Describe the scene for a visually impaired user with a safety focus. "
                "Call out immediate hazards, obstacles, and moving objects first. "
                "Mention distances and directions when possible. Keep it to 2-4 short sentences. "
                "If uncertain, say so."
            )
        if mode == "awareness":
            return (
                "Provide a concise scene overview for situational awareness. "
                "Mention key objects, layout, and open paths. Include distance and direction when possible. "
                "Keep it to 2-4 short sentences. If uncertain, say so."
            )
        if mode == "companion":
            return (
                "Give a calm, human-friendly description of the scene. "
                "Focus on ambience and notable objects without alarmist language. "
                "Keep it to 2-4 short sentences. If uncertain, say so."
            )
        return None

    def _describe_stub(self, mode: str) -> str:
        if mode == "safety":
            return "Safety check complete. No immediate hazards detected."
        if mode == "awareness":
            return "You are in an open area with clear space ahead."
        if mode == "companion":
            return "It feels calm and open around you, with a quiet atmosphere."

        return "Scene description mode not recognized."

    def _describe_openai(self, image_path: str, prompt: str, mode: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            if self.debug:
                print("[SCENE] OPENAI_API_KEY not set. Falling back to stub.")
            return self._describe_stub(mode)

        image_b64, mime_type = self._read_image_b64(image_path)
        if image_b64 is None:
            return "Failed to read the captured scene image."

        model = self.model or "gpt-4o-mini"
        payload = {
            "model": model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:{mime_type};base64,{image_b64}",
                        },
                    ],
                }
            ],
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens,
        }

        return self._post_json(
            url="https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
            extractor=self._extract_openai_text,
            fallback=self._describe_stub(mode),
        )

    def _describe_gemini(self, image_path: str, prompt: str, mode: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            if self.debug:
                print("[SCENE] GEMINI_API_KEY not set. Falling back to stub.")
            return self._describe_stub(mode)

        # Prefer google-genai client if available
        try:
            from google import genai  # type: ignore
        except Exception:
            genai = None

        if genai:
            return self._describe_gemini_sdk(image_path, prompt, mode, genai)

        # Fallback to direct HTTP if SDK isn't installed
        image_b64, mime_type = self._read_image_b64(image_path)
        if image_b64 is None:
            return "Failed to read the captured scene image."

        model = self.model or "gemini-2.0-flash"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": mime_type, "data": image_b64}},
                    ],
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            },
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        return self._post_json(
            url=url,
            headers={"Content-Type": "application/json"},
            payload=payload,
            extractor=self._extract_gemini_text,
            fallback=self._describe_stub(mode),
        )

    def _describe_gemini_sdk(self, image_path: str, prompt: str, mode: str, genai) -> str:
        image_bytes = Path(image_path).read_bytes() if Path(image_path).exists() else None
        if not image_bytes:
            return "Failed to read the captured scene image."

        model = self.model or "gemini-2.0-flash"
        try:
            from google.genai import types  # type: ignore

            client = genai.Client()
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=self._mime_type_for_path(Path(image_path)),
                    ),
                ],
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                ),
            )
            text = getattr(response, "text", None)
            if isinstance(text, str) and text.strip():
                return text.strip()
            return self._describe_stub(mode)
        except Exception as err:
            if self.debug:
                print(f"[SCENE] Gemini SDK request failed: {err}")
            return self._describe_stub(mode)

    def _post_json(
        self,
        url: str,
        headers: dict,
        payload: dict,
        extractor,
        fallback: str,
    ) -> str:
        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
            parsed = json.loads(body)
            text = extractor(parsed)
            return text or fallback
        except urllib.error.HTTPError as err:
            if self.debug:
                try:
                    detail = err.read().decode("utf-8")
                except Exception:
                    detail = "<unable to read error body>"
                print(f"[SCENE] Request failed: HTTP {err.code} {err.reason}")
                print(f"[SCENE] Error body: {detail}")
            return fallback
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as err:
            if self.debug:
                print(f"[SCENE] Request failed: {err}")
            return fallback

    def _extract_openai_text(self, payload: dict) -> Optional[str]:
        if isinstance(payload.get("output_text"), str):
            return payload["output_text"].strip()

        for item in payload.get("output", []):
            for part in item.get("content", []):
                if isinstance(part, dict) and isinstance(part.get("text"), str):
                    return part["text"].strip()
        return None

    def _extract_gemini_text(self, payload: dict) -> Optional[str]:
        candidates = payload.get("candidates", [])
        if not candidates:
            return None
        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            text = part.get("text")
            if isinstance(text, str):
                return text.strip()
        return None

    def _read_image_b64(self, image_path: str) -> tuple[Optional[str], str]:
        path = Path(image_path)
        if not path.exists():
            return None, "image/jpeg"
        mime_type = self._mime_type_for_path(path)
        image_bytes = path.read_bytes()
        return base64.b64encode(image_bytes).decode("ascii"), mime_type

    def _mime_type_for_path(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".png":
            return "image/png"
        if suffix in (".jpg", ".jpeg"):
            return "image/jpeg"
        return "application/octet-stream"
