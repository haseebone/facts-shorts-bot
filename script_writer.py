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
import time
import random
import config

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-latest:generateContent?key=" + config.GEMINI_API_KEY
)

FALLBACK_SCRIPTS = [
    {
        "title": "The Ocean Fact That Sounds Fake",
        "script": "Here's one that sounds made up but isn't. Sharks have been swimming on this planet for over 400 million years. Trees? Only about 350 million years old. That means sharks are older than trees, older than Saturn's rings, and older than most mountain ranges on Earth. They survived five mass extinctions. Trees weren't even invented yet.",
        "description": "Sharks are older than trees. Mind blown yet? #facts #shorts #didyouknow"
    },
    {
        "title": "Why Honey Never Goes Bad",
        "script": "Archaeologists once found a pot of honey in an ancient Egyptian tomb, over three thousand years old, and it was still perfectly edible. Honey has almost no water in it, and bees fill it with an acid that kills bacteria. Nothing can grow in it. Store it right, and honey basically lasts forever.",
        "description": "3000-year-old honey that's still edible. Nature is wild. #facts #shorts #didyouknow"
    },
    {
        "title": "The Planet Where It Rains Diamonds",
        "script": "On Jupiter and Saturn, scientists believe it actually rains diamonds. The extreme pressure and heat in their atmospheres compress carbon into diamond chunks, which then fall like hail toward the planet's core. Some estimates say millions of tons of diamonds form there every single year.",
        "description": "It rains diamonds on other planets. For real. #facts #shorts #space"
    }
]

def get_fallback_script(topic):
    chosen = random.choice(FALLBACK_SCRIPTS)
    result = dict(chosen)
    result["source_topic"] = topic
    result["source_url"] = ""
    result["used_fallback"] = True
    return result

PROMPT_TEMPLATE = """You are writing a 30-45 second YouTube Shorts script for a "facts" channel targeting a USA audience. The topic is:

"{topic}"

Write:
1. A punchy, curiosity-driven TITLE (under 60 characters, no clickbait lies)
2. A VOICEOVER SCRIPT (spoken, first-person energetic tone, 60-90 words, starts with a strong hook in the first sentence, ends with a satisfying payoff)
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
    return data["topics"][0]

def call_gemini(prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    last_error = None
    for attempt in range(4):
        try:
            resp = requests.post(GEMINI_URL, json=body, timeout=90)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            last_error = e
            print(f"  [!] Gemini attempt {attempt + 1} failed: {e}")
            if attempt < 3:
                wait = 10 * (attempt + 1)
                print(f"      Waiting {wait}s before retrying...")
                time.sleep(wait)
    raise last_error

def clean_json_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        text = text.replace("json", "", 1).strip()
    return json.loads(text)

def main():
    topic = load_next_topic()
    print(f"Writing script for topic: {topic['topic']}")

    prompt = PROMPT_TEMPLATE.format(topic=topic["topic"])
    try:
        raw = call_gemini(prompt)
        result = clean_json_response(raw)
        result["used_fallback"] = False
    except Exception as e:
        print(f"\n  [!] Gemini unavailable after all retries: {e}")
        print("  [!] Using a backup pre-written script instead.\n")
        result = get_fallback_script(topic["topic"])

    result["source_topic"] = topic["topic"]
    result["source_url"] = topic.get("url", "")

    with open("script.json", "w") as f:
        json.dump(result, f, indent=2)

    print("\nTitle:", result["title"])
    print("\nScript:\n", result["script"])
    print("\nSaved to script.json")

if __name__ == "__main__":
    main()
