import requests
import os
from dotenv import load_dotenv

load_dotenv()

deals_key = os.environ.get("deals_key")

def get_deals(location: str) -> str:
    """
    Get deals and discounts for a specific location.

    Args:
        location (str): Location to search for deals

    Returns:
        str: Deals data as a string, or error message if failed
    """
    if not deals_key:
        return "Error: Missing deals_key in environment variables"

    url = f'https://api.discountapi.com/v2/deals?api_key={deals_key}&location={location}'
    response = requests.get(url)

    if response.status_code != 200:
        return f"Failed to get deals: {response.text}"

    data = response.json()
    return str(data)
