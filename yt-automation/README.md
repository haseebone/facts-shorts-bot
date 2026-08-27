# Fully Automated YouTube Shorts Channel — "Facts" (USA audience)

Everything is in this one folder. Once set up, it runs **24/7, automatically,
completely free**, uploading ~2 Shorts/day, even when your computer is off.

**Pipeline:** Trending topic → Script → Voiceover → Video → Thumbnail → Upload

---

## PART 1 — Get your free accounts & keys (one-time, ~30-40 min)

You need 4 free things. None require a credit card.

### 1. GitHub account (this is what runs everything 24/7 for free)
- Go to https://github.com/signup, create a free account
- Create a **new repository** (name it e.g. `facts-shorts-bot`) — make it Public
  (public repos get *unlimited* free automation minutes)
- Upload ALL the files from this folder into that repository
  (easiest way: install GitHub Desktop app, or just drag-and-drop files
  on github.com using "Add file" → "Upload files")

### 2. Google Gemini API key (free — this writes your scripts)
- Go to https://aistudio.google.com/app/apikey
- Sign in with any Google account, click "Create API Key"
- Copy the key — you'll paste it into GitHub Secrets in Part 2

### 3. Pexels API key (free — this provides stock video clips)
- Go to https://www.pexels.com/api/
- Sign up free, copy your API key

### 4. YouTube Data API access (free — this lets it upload for you)
This is the only slightly longer one. Steps:
1. Go to https://console.cloud.google.com/
2. Create a new project (top left, free)
3. Search "YouTube Data API v3" in the search bar → click **Enable**
4. Go to "Credentials" (left menu) → "Create Credentials" → "OAuth client ID"
   - If asked, configure the consent screen first: choose "External," fill in
     basic app info (any name is fine), add your own email as a test user
   - Application type: **Desktop app**
5. Download the file it gives you, rename it to `client_secret.json`

Now, **on your own computer** (this part needs to happen once, on your PC,
not GitHub):
1. Put `client_secret.json` in the project folder
2. Run: `pip install -r requirements.txt`
3. Run: `python3 upload.py` — this opens a browser ONE TIME asking you to
   log in and approve access. Approve it.
4. This creates a file called `token.pickle` — **this is the key that lets
   it upload without you ever logging in again.**

---

## PART 2 — Add your keys to GitHub (so it can run without your PC)

In your GitHub repository:
1. Go to **Settings → Secrets and variables → Actions**
2. Click "New repository secret" and add these 4 secrets:

| Secret name | Value |
|---|---|
| `GEMINI_API_KEY` | your Gemini key from Part 1 |
| `PEXELS_API_KEY` | your Pexels key from Part 1 |
| `YT_CLIENT_SECRET_B64` | see below |
| `YT_TOKEN_PICKLE_B64` | see below |

For the last two, open a terminal in your project folder and run:
```
# Mac/Linux:
base64 -i client_secret.json
base64 -i token.pickle

# Windows (PowerShell):
[Convert]::ToBase64String([IO.File]::ReadAllBytes("client_secret.json"))
[Convert]::ToBase64String([IO.File]::ReadAllBytes("token.pickle"))
```
Copy each long output text and paste it as the secret value.

*(Why base64? GitHub Secrets only store text, and these are binary/JSON files —
this just safely converts them to text and back.)*

---

## PART 3 — Turn it on

That's it. The file `.github/workflows/pipeline.yml` is already set to run
**automatically twice a day, forever, for free**, using GitHub's free
Actions minutes (unlimited for public repos).

To test it right now instead of waiting:
1. Go to your repo on GitHub → "Actions" tab
2. Click "YouTube Shorts Auto Pipeline" → "Run workflow" → "Run workflow"
3. Watch it run live — topic → script → voiceover → video → upload

If a step fails, GitHub shows you the exact error — paste it to me and I'll fix it.

---

## Files in this project

| File | What it does |
|---|---|
| `config.py` | all your settings & key placeholders |
| `topic_finder.py` | finds trending fact topics from Reddit |
| `script_writer.py` | writes title/script/description (free Gemini) |
| `voiceover.py` | turns script into audio (free Edge TTS) |
| `video_assembly.py` | builds the final video with captions (free FFmpeg + Pexels) |
| `thumbnail.py` | generates the thumbnail image |
| `upload.py` | uploads to YouTube (free API) |
| `run_pipeline.py` | runs all of the above in order, one command |
| `.github/workflows/pipeline.yml` | the scheduler — runs it all 24/7 for free |

---

## Costs — the honest total

**$0.** Every single piece used here (GitHub Actions, Gemini free tier,
Pexels, Edge TTS, YouTube API, FFmpeg) has a genuinely free tier with no
credit card required. The only limits: ~2-6 uploads/day (YouTube quota),
and Gemini's free tier has a generous but real rate limit (fine for 2/day).

## Changing the schedule / upload count

- To change upload times: edit the two `cron:` lines in
  `.github/workflows/pipeline.yml` (times are in UTC)
- To go from 2/day to more: add more `cron:` lines (stay at or under 6/day
  total to stay within YouTube's free quota)

---

**Next step:** work through Part 1 above, and tell me where you get stuck —
I'll walk you through any error, step by step.
