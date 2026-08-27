"""
CONFIG — put all your free API keys here in ONE place.
Nothing in this file costs money. Every key below has a free tier.
See README.md for exactly how to get each one (step by step).
"""

import os

# ── Google Gemini (free) — used to write video scripts & titles ──
# Get it free at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_GEMINI_KEY_HERE")

# ── Pexels (free) — used to pull free stock video clips ──
# Get it free at: https://www.pexels.com/api/
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "PASTE_YOUR_PEXELS_KEY_HERE")

# ── YouTube Data API (free) — used to auto-upload ──
# You'll download a file called client_secret.json from Google Cloud Console
# (steps in README) and place it in this folder. No key needed here.

# ── General settings ──
NICHE = "facts"
AUDIENCE = "USA"
UPLOADS_PER_RUN = 1          # how many videos to make each time the pipeline runs
EDGE_TTS_VOICE = "en-US-GuyNeural"   # free natural-sounding US voice
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920           # vertical, for Shorts
