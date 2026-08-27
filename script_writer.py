"""
Piece 2: Script Writer
------------------------------------------------------------
Reads topics.json (from topic_finder.py) and writes a full
Shorts script + title + description for the top unused topic,
using Google Gemini's FREE API tier.

Output: script.json
"""

import json
import requests
import config

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key=" + config.GEMINI_API_KEY
)

PROMPT_TEMPLATE = """You are writing a 30-45 second YouTube Shorts script for a "facts" \
channel targeting a USA audience. The topic is:

"{topic}"

Write:
1. A punchy, curiosity-driven TITLE (under 60 characters, no clickbait lies)
2. A VOICEOVER SCRIPT (spoken, first-person energetic tone, 60-90 words, \
starts with a strong hook in the first sentence, ends with a satisfying payoff)
3. A short YouTube DESCRIPTION (1-2 sentences + 3 relevant hashtags)

Respond ONLY in this exact JSON format, nothing else:
{{
  "title": "...",
  "script": "...",
  "description": "..."
}}
"""

def load_next_topic():
    with open("topics.json", "r") as f:
        data = json.load(f)
    if not data["topics"]:
        raise ValueError("No topics found. Run topic_finder.py first.")
    return data["topics"][0]  # take the top one

def call_gemini(prompt: str) -> str:
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    resp = requests.post(GEMINI_URL, json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def clean_json_response(text: str) -> dict:
    # Gemini sometimes wraps JSON in ```json fences — strip those
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        text = text.replace("json", "", 1).strip()
    return json.loads(text)

def main():
    topic = load_next_topic()
    print(f"Writing script for topic: {topic['topic']}")

    prompt = PROMPT_TEMPLATE.format(topic=topic["topic"])
    raw = call_gemini(prompt)
    result = clean_json_response(raw)

    result["source_topic"] = topic["topic"]
    result["source_url"] = topic.get("url", "")

    with open("script.json", "w") as f:
        json.dump(result, f, indent=2)

    print("\nTitle:", result["title"])
    print("\nScript:\n", result["script"])
    print("\nSaved to script.json")

if __name__ == "__main__":
    main()
