"""
YouTube Shorts Topic Finder — "Facts" Niche (USA audience)
------------------------------------------------------------
What this does:
1. Pulls hot/trending posts from fact-related subreddits (free, no login needed)
2. Cleans them up into short, punchy "fact topic" ideas
3. Saves them to topics.json so the next script (script writer) can use them

How to run:
    python3 topic_finder.py

Output:
    topics.json  -> a list of topic ideas ready for scripting
"""

import requests
import json
import re
from datetime import datetime, timezone

SUBREDDITS = [
    "todayilearned",
    "interestingasfuck",
    "Damnthatsinteresting",
    "facts",
    "coolguides",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

FALLBACK_TOPICS = [
    "The shortest war in history lasted only 38 minutes",
    "Octopuses have three hearts and blue blood",
    "A day on Venus is longer than a year on Venus",
    "Honey never spoils, even after thousands of years",
    "Bananas are naturally slightly radioactive",
    "The Eiffel Tower grows taller in summer heat",
    "Wombat poop is cube-shaped",
    "A single bolt of lightning is hotter than the sun's surface",
    "Sharks existed before trees appeared on Earth",
    "Your stomach gets an entirely new lining every few days",
    "There are more stars in the universe than grains of sand on Earth",
    "The inventor of the frisbee was turned into a frisbee after he died",
    "Cows have best friends and get stressed when separated",
    "It rains diamonds on Jupiter and Saturn",
    "The unicorn is Scotland's national animal",
]

def clean_title(title: str) -> str:
    title = re.sub(r'^\s*TIL\s+(that\s+)?', '', title, flags=re.IGNORECASE)
    return title.strip()

def fetch_subreddit_hot(subreddit: str, limit: int = 10):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [!] Could not fetch r/{subreddit}: {e}")
        return []

    posts = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        title = post.get("title", "")
        score = post.get("score", 0)
        if post.get("stickied"):
            continue
        if len(title) < 15:
            continue
        posts.append({
            "topic": clean_title(title),
            "source": f"r/{subreddit}",
            "upvotes": score,
            "url": f"https://reddit.com{post.get('permalink', '')}"
        })
    return posts

def main():
    print("Fetching trending fact topics for US audience...\n")
    all_topics = []

    for sub in SUBREDDITS:
        print(f"  -> Checking r/{sub} ...")
        posts = fetch_subreddit_hot(sub, limit=10)
        all_topics.extend(posts)

    all_topics.sort(key=lambda x: x["upvotes"], reverse=True)

    seen = set()
    final_topics = []
    for t in all_topics:
        key = t["topic"].lower()
        if key in seen:
            continue
        seen.add(key)
        final_topics.append(t)
        if len(final_topics) >= 20:
            break

    if not final_topics:
        print("\n  [!] Reddit blocked all requests — using backup topic list instead.\n")
        import random
        chosen = random.choice(FALLBACK_TOPICS)
        final_topics = [{
            "topic": chosen,
            "source": "fallback list",
            "upvotes": 0,
            "url": ""
        }]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "audience": "USA",
        "niche": "facts",
        "topics": final_topics
    }

    with open("topics.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone! Saved {len(final_topics)} topics to topics.json\n")
    print("Top 5 picks:")
    for i, t in enumerate(final_topics[:5], 1):
        print(f"  {i}. {t['topic']}  (from {t['source']}, {t['upvotes']} upvotes)")

if __name__ == "__main__":
    main()
