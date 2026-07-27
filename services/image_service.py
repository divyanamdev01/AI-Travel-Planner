import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")


def get_place_image(query):

    url = (
        f"https://api.unsplash.com/search/photos"
        f"?query={query}"
        f"&client_id={UNSPLASH_API_KEY}"
        f"&per_page=1"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("results"):
            return data["results"][0]["urls"]["regular"]

        return None

    except Exception:
        return None