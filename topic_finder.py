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

# Subreddits that reliably produce good "fact" style content for US audiences
SUBREDDITS = [
    "todayilearned",
    "interestingasfuck",
    "Damnthatsinteresting",
    "facts",
    "coolguides",
]

# Reddit requires a User-Agent header or it will block the request.
# Use a specific, descriptive one (Reddit blocks generic/default ones).
HEADERS = {
    "User-Agent": "python:fact-shorts-topic-finder:v1.0 (by /u/yourredditusername)"
}

def clean_title(title: str) -> str:
    """Remove Reddit-specific junk like 'TIL' prefixes so it reads as a clean fact hook."""
    title = re.sub(r'^\s*TIL\s+(that\s+)?', '', title, flags=re.IGNORECASE)
    title = title.strip()
    return title

def fetch_subreddit_hot(subreddit: str, limit: int = 10):
    """Fetch hot posts from a subreddit's public JSON feed (no API key required)."""
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
        # Skip stickied/mod posts and low-effort ones
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

    # Sort by upvotes (proxy for "how interesting / trending" it is)
    all_topics.sort(key=lambda x: x["upvotes"], reverse=True)

    # Keep top 20 unique topics
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
