tools = [{"type":"function","function":{"name":"ticketmaster_discovery_tool","description":"Search for events, attractions, or venues using the Ticketmaster Discovery API.","parameters":{"type":"object","properties":{"keyword":{"type":"string","description":"Search term used to find events, attractions, or venues."},"countryCode":{"type":"string","description":"Filter events by country code (e.g., 'US', 'CA')."},"city":{"type":"string","description":"Filter events by city name."},"stateCode":{"type":"string","description":"Filter events by state code."},"postalCode":{"type":"string","description":"Filter events by postal/ZIP code."},"startDateTime":{"type":"string","description":"ISO 8601 date-time string to filter events starting after this time."},"endDateTime":{"type":"string","description":"ISO 8601 date-time string to filter events starting before this time."},"size":{"type":"integer","description":"Number of results to return per page (default: 20, max: 200)."},"page":{"type":"integer","description":"Page number of results to return (default: 0)."},"sort":{"type":"string","description":"Sort order of results (e.g., 'date,asc', 'relevance,desc')."}},"required":["keyword"]}}}]

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ticketmaster_search_events(
    keyword: str,
    countryCode: str = None,
    city: str = None,
    stateCode: str = None,
    postalCode: str = None,
    startDateTime: str = None,
    endDateTime: str = None,
    size: int = None,
    page: int = None,
    sort: str = None
) -> dict:
    """
    Search for events via Ticketmaster Discovery API v2.

    Parameters:
      keyword (str): Search term to find events (required).
      countryCode (str): ISO country code (e.g., 'US', 'CA').
      city (str): City name to filter events.
      stateCode (str): State/province code to filter events.
      postalCode (str): ZIP/postal code to filter.
      startDateTime (str): ISO8601 start date-time (e.g., '2025-11-08T00:00:00Z').
      endDateTime (str): ISO8601 end date-time.
      size (int): Number of results per page (max 200).
      page (int): Page number (0-based).
      sort (str): Sort order, e.g., 'date,asc' or 'relevance,desc'.

    Returns:
      dict: Parsed JSON response from Ticketmaster API.
    """
    api_key = os.getenv("TICKETMASTER_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable TICKETMASTER_API_KEY not set")

    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "keyword": keyword
    }

    # optional filters
    if countryCode:
        params["countryCode"] = countryCode
    if city:
        params["city"] = city
    if stateCode:
        params["stateCode"] = stateCode
    if postalCode:
        params["postalCode"] = postalCode
    if startDateTime:
        params["startDateTime"] = startDateTime
    if endDateTime:
        params["endDateTime"] = endDateTime
    if size is not None:
        params["size"] = size
    if page is not None:
        params["page"] = page
    if sort:
        params["sort"] = sort

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

from pymongo import MongoClient
from typing import Any, Dict, List, Optional
import os

# You’d normally load these from environment variables or a config
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME      = os.getenv("DB_NAME")

client     = MongoClient(MONGODB_URI)
db         = client[DB_NAME]
collection = db["DegreePlanners"]

def find_degree_planners(
    filters: Dict[str, Any],
    projection: Optional[Dict[str, int]] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Fetches documents from the 'DegreePlanners' collection with multiple filter fields.

    :param filters: A dict mapping field names to the values (or sub‑queries) you want to filter on.
    :param projection: Optional dict specifying which fields to include (1) or exclude (0).
    :param limit: Optional maximum number of documents to return.
    :param skip: Optional number of documents to skip (for pagination).
    :return: A list of matching documents.
    """
    # Build the query filter directly from the provided dict
    query = filters  # e.g., { "status": "active", "year": 3 }

    cursor = collection.find(query, projection) if projection else collection.find(query)

    if skip is not None:
        cursor = cursor.skip(skip)
    if limit is not None:
        cursor = cursor.limit(limit)

    results = list(cursor)
    return results

# Example usage:
# if __name__ == "__main__":
    # try:
    #     result = ticketmaster_search_events(
    #         keyword="rock concert",
    #         countryCode="US",
    #         city="Los Angeles",
    #         startDateTime="2025-11-10T00:00:00Z",
    #         size=10,
    #         page=0,
    #         sort="date,asc"
    #     )
    #     print(result)
    # except Exception as e:
    #     print("Error calling Ticketmaster API:", e)

# Example usage:
if __name__ == "__main__":
    # Example: find all planners where status="active" and year=3
    my_filters = {"Year": "First Year", "Semester": "Fall"}
    # my_projection = {"_id": 0, "name": 1, "year": 1, "status": 1} # include / exclude fields
    docs = find_degree_planners(my_filters, projection={}, limit=10, skip=0)
    print(f"Found {len(docs)} documents:")
    for d in docs:
        print(d)

"""
    How to use MongoDB
    - Query based on paramters e.g. {"Year": "First Year"}
    - will return the classes or courses needed for those

    Check out TAMU_CS_BS_DEGREEPLAN.csv to see what you can search (your basically searching through that)

"""