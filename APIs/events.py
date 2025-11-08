import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_nearby_events(lat, lon, radius=10, unit="miles", keyword=None, start_date=None, end_date=None, size=20):
    """
    Fetch nearby events from the Ticketmaster Discovery API.
    """
    api_key = os.getenv("TICKETMASTER_API_KEY")
    if not api_key:
        raise ValueError("Missing TICKETMASTER_API_KEY in .env file")

    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "latlong": f"{lat},{lon}",
        "radius": radius,
        "unit": unit,
        "size": size
    }

    if keyword:
        params["keyword"] = keyword
    if start_date and end_date:
        params["startDateTime"] = start_date
        params["endDateTime"] = end_date

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return []

    data = response.json()
    print(data)
    events = data.get("_embedded", {}).get("events", [])
    results = [
        {
            "name": e["name"] if "name" in e else None,
            "url": e["url"] if "url" in e else None,
            "start_date": e["startDateTime"] if "startDateTime" in e else None,
            "venue": e["name"] if "_embedded" in e else None,
            "city": e["_embedded"]["venues"][0]["city"]["name"] if "_embedded" in e else None
        }
        for e in events
    ]
    return results


# Example usage
if __name__ == "__main__":
    events = get_nearby_events(lat=34.0522, lon=-118.2437, radius=25, keyword="music")
    for e in events:
        print(f"{e['name']} — {e['city']} — {e['start_date']}")
