import os
import requests
from dotenv import load_dotenv

# .env फ़ाइल लोड करें
load_dotenv()

# API Key प्राप्त करें
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_trailer(movie_id):
    if not API_KEY:
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    videos = data.get("results", [])

    for video in videos:
        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
            and video.get("official", False)
        ):
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None