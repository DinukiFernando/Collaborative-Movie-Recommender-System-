import requests

OMDB_API_KEY = "your_omdb_api_key"

def fetch_poster(title):
    """Fetch movie poster from OMDB."""
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
    return "https://via.placeholder.com/300x450?text=No+Image"
