import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


def get_private_videos_from_channel():
    # Autoryzacja do API YouTube
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
    youtube = build("youtube", "v3", credentials=credentials)

    # Pytanie o link do kanału
    channel_url = input("Podaj link do kanału: ")
    channel_id = channel_url.split("/")[-1]

    # Pobranie listy filmów niepublicznych dla danego kanału
    try:
        videos = []
        next_page_token = None
        while True:
            request = youtube.search().list(
                part="id,snippet",
                channelId=channel_id,
                type="video",
                videoDefinition="high",
                videoSyndicated="true",
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                if item["id"]["kind"] == "youtube#video":
                    video_id = item["id"]["videoId"]
                    video_title = item["snippet"]["title"]
                    videos.append((video_title, video_id))

            next_page_token = response.get("nextPageToken")
            if next_page_token is None:
                break

        return videos

    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
