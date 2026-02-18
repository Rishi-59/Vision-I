import os

from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not set.")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-1.5-flash", contents="Write a story about a magic backpack."
)
print(response.text)
