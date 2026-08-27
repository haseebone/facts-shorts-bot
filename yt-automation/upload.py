"""
Piece 6: YouTube Uploader
------------------------------------------------------------
Uploads final_video.mp4 + thumbnail.jpg + title/description to
YouTube using the free YouTube Data API (v3).

IMPORTANT — one-time manual step required:
YouTube requires you to personally approve access ONCE (Google's
security rule, can't be skipped). After that one-time approval,
this runs fully unattended forever using a saved "refresh token."

See README.md section "YouTube API setup" for exact steps.
"""

import json
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.pickle"
CLIENT_SECRET_FILE = "client_secret.json"

def get_authenticated_service():
    creds = None

    # Reuse saved login if we have one (this is what makes it "unattended")
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # ONE-TIME ONLY: opens a browser for you to approve access
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, video_path, thumbnail_path, title, description):
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": ["facts", "shorts", "didyouknow"],
            "categoryId": "27",  # Education
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print("Uploading video...")
    response = request.execute()
    video_id = response["id"]
    print(f"Uploaded! https://youtube.com/shorts/{video_id}")

    # Set custom thumbnail
    youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()
    print("Thumbnail set.")

    return video_id

def main():
    with open("script.json", "r") as f:
        script_data = json.load(f)

    youtube = get_authenticated_service()
    upload_video(
        youtube,
        video_path="final_video.mp4",
        thumbnail_path="thumbnail.jpg",
        title=script_data["title"],
        description=script_data["description"],
    )

if __name__ == "__main__":
    main()
