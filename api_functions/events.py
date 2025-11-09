import requests
import os
from dotenv import load_dotenv

load_dotenv()

ticketmaster_key = os.environ.get("TICKETMASTER_API_KEY")

def get_events(lat: float, lon: float, radius: int = 10, unit: str = "miles",
               keyword: str = None, start_date: str = None, end_date: str = None,
               size: int = 20) -> str:
    """
    Get nearby events from Ticketmaster based on latitude and longitude coordinates.

    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        radius (int, optional): Search radius (default: 10)
        unit (str, optional): Distance unit: 'miles' or 'km' (default: 'miles')
        keyword (str, optional): Optional keyword to filter events
        start_date (str, optional): Optional start date in ISO format
        end_date (str, optional): Optional end date in ISO format
        size (int, optional): Number of results to return (default: 20)

    Returns:
        str: Events data as a string, or error message if failed
    """
    if not ticketmaster_key:
        return "Error: Missing TICKETMASTER_API_KEY in environment variables"

    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": ticketmaster_key,
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

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

        results = []
        for e in events:
            event_data = {
                "name": e.get("name"),
                "url": e.get("url"),
                "start_date": e.get("dates", {}).get("start", {}).get("localDate")
            }

            if "_embedded" in e and "venues" in e["_embedded"] and len(e["_embedded"]["venues"]) > 0:
                venue = e["_embedded"]["venues"][0]
                event_data["venue"] = venue.get("name")
                event_data["city"] = venue.get("city", {}).get("name")

            results.append(event_data)

        return str(results)

    except Exception as e:
        return f"Error fetching events: {str(e)}"

def get_events_by_city(city: str, state: str = None, country: str = "US",
                       keyword: str = None, size: int = 20) -> str:
    """
    Get events by city name instead of coordinates.

    Args:
        city (str): City name
        state (str, optional): State abbreviation (for US cities)
        country (str, optional): Country code (default: 'US')
        keyword (str, optional): Optional keyword to filter events
        size (int, optional): Number of results to return (default: 20)

    Returns:
        str: Events data as a string, or error message if failed
    """
    if not ticketmaster_key:
        return "Error: Missing TICKETMASTER_API_KEY in environment variables"

    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": ticketmaster_key,
        "city": city,
        "countryCode": country,
        "size": size
    }

    if state:
        params["stateCode"] = state
    if keyword:
        params["keyword"] = keyword

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

        results = []
        for e in events:
            event_data = {
                "name": e.get("name"),
                "url": e.get("url"),
                "start_date": e.get("dates", {}).get("start", {}).get("localDate"),
                "start_time": e.get("dates", {}).get("start", {}).get("localTime"),
                "price_range": None
            }

            # Get venue information
            if "_embedded" in e and "venues" in e["_embedded"] and len(e["_embedded"]["venues"]) > 0:
                venue = e["_embedded"]["venues"][0]
                event_data["venue"] = venue.get("name")
                event_data["city"] = venue.get("city", {}).get("name")
                event_data["state"] = venue.get("state", {}).get("stateCode")

            # Get price information
            if "priceRanges" in e and len(e["priceRanges"]) > 0:
                price_range = e["priceRanges"][0]
                min_price = price_range.get("min")
                max_price = price_range.get("max")
                currency = price_range.get("currency", "USD")
                if min_price and max_price:
                    event_data["price_range"] = f"{currency} {min_price} - {max_price}"

            # Get classification/genre
            if "classifications" in e and len(e["classifications"]) > 0:
                classification = e["classifications"][0]
                event_data["genre"] = classification.get("genre", {}).get("name")
                event_data["segment"] = classification.get("segment", {}).get("name")

            results.append(event_data)

        return str(results)

    except Exception as e:
        return f"Error fetching events by city: {str(e)}"

def get_music_events(lat: float, lon: float, radius: int = 25, size: int = 20) -> str:
    """
    Get music events specifically in a given area.

    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        radius (int, optional): Search radius (default: 25)
        size (int, optional): Number of results to return (default: 20)

    Returns:
        str: Music events data as a string, or error message if failed
    """
    return get_events(lat=lat, lon=lon, radius=radius, keyword="music", size=size)

def get_sports_events(lat: float, lon: float, radius: int = 50, size: int = 20) -> str:
    """
    Get sports events specifically in a given area.

    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        radius (int, optional): Search radius (default: 50)
        size (int, optional): Number of results to return (default: 20)

    Returns:
        str: Sports events data as a string, or error message if failed
    """
    return get_events(lat=lat, lon=lon, radius=radius, keyword="sports", size=size)
