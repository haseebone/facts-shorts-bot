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

# Used ONLY if Gemini is down/overloaded for all retry attempts. Keeps the
# pipeline from ever fully stopping, so uploads never get skipped.
FALLBACK_SCRIPTS = [
    {
        "title": "The Ocean Fact That Sounds Fake",
        "script": "Here's one that sounds made up but isn't. Sharks have been "
                   "swimming on this planet for over 400 million years. Trees? "
                   "Only about 350 million years old. That means sharks are "
                   "older than trees, older than Saturn's rings, and older "
                   "than most mountain ranges on Earth. They survived five "
                   "mass extinctions. Trees weren't even invented yet.",
        "description": "Sharks are older than trees. Mind blown yet? "
                        "#facts #shorts #didyouknow"
    },
    {
        "title": "Why Honey Never Goes Bad",
        "script": "Archaeologists once found a pot of honey in an ancient "
                   "Egyptian tomb, over three thousand years old, and it was "
                   "still perfectly edible. Honey has almost no water in it, "
                   "and bees fill it with an acid that kills bacteria. Nothing "
                   "can grow in it. Store it right, and honey basically lasts "
                   "forever.",
        "description": "3000-year-old honey that's still edible. Nature is wild. "
                        "#facts #shorts #didyouknow"
    },
    {
        "title": "The Planet Where It Rains Diamonds",
        "script": "On Jupiter and Saturn, scientists believe it actually rains "
                   "diamonds. The extreme pressure and heat in their "
                   "atmospheres compress carbon into diamond chunks, which "
                   "then fall like hail toward the planet's core. Some "
                   "estimates say millions of tons of diamonds form there "
