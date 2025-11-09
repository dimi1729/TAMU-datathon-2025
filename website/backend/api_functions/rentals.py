import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

rental_key = os.environ.get("rental_key")

def get_rentals(location: str) -> str:
    """
    Search for rental properties in a specific location using Zillow data.

    Args:
        location (str): Location to search for rentals (e.g., 'college station, tx', 'new york, ny')

    Returns:
        str: Rental properties data as a string, or error message if failed
    """
    if not rental_key:
        return "Error: Missing rental_key in environment variables"

    url = "https://zillow56.p.rapidapi.com/search"
    querystring = {
        "location": location,
        "output": "json",
        "status": "forRent",
        "sortSelection": "priorityscore",
        "listing_type": "by_agent",
        "doz": "any"
    }

    headers = {
        'x-rapidapi-key': rental_key,
        'x-rapidapi-host': "zillow56.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            return f"Failed to get rentals: {response.text}"

        return response.text

    except Exception as e:
        return f"Error fetching rentals: {str(e)}"

def get_filtered_rentals(location: str, min_price: int = None, max_price: int = None,
                        bedrooms: int = None, bathrooms: int = None) -> str:
    """
    Search for rental properties with additional filtering options.

    Args:
        location (str): Location to search for rentals
        min_price (int, optional): Minimum monthly rent
        max_price (int, optional): Maximum monthly rent
        bedrooms (int, optional): Number of bedrooms
        bathrooms (int, optional): Number of bathrooms

    Returns:
        str: Filtered rental properties data as a string, or error message if failed
    """
    if not rental_key:
        return "Error: Missing rental_key in environment variables"

    url = "https://zillow56.p.rapidapi.com/search"
    querystring = {
        "location": location,
        "output": "json",
        "status": "forRent",
        "sortSelection": "priorityscore",
        "listing_type": "by_agent",
        "doz": "any"
    }

    # Add filtering parameters if provided
    if min_price:
        querystring["minPrice"] = min_price
    if max_price:
        querystring["maxPrice"] = max_price
    if bedrooms:
        querystring["bedrooms"] = bedrooms
    if bathrooms:
        querystring["bathrooms"] = bathrooms

    headers = {
        'x-rapidapi-key': rental_key,
        'x-rapidapi-host': "zillow56.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code != 200:
            return f"Failed to get filtered rentals: {response.text}"

        return response.text

    except Exception as e:
        return f"Error fetching filtered rentals: {str(e)}"

def parse_rental_data(rental_response: str) -> dict:
    """
    Parse the raw rental API response into a more readable format.

    Args:
        rental_response (str): Raw response from rental API

    Returns:
        dict: Parsed rental data with key information extracted
    """
    try:
        data = json.loads(rental_response)

        if "results" not in data:
            return {"error": "No results found in rental data"}

        parsed_rentals = []
        for property_data in data.get("results", []):
            rental_info = {
                "address": property_data.get("address", "Address not available"),
                "price": property_data.get("price", "Price not available"),
                "bedrooms": property_data.get("bedrooms", "N/A"),
                "bathrooms": property_data.get("bathrooms", "N/A"),
                "square_feet": property_data.get("livingArea", "N/A"),
                "property_type": property_data.get("homeType", "N/A"),
                "listing_url": property_data.get("detailUrl", ""),
                "image_url": property_data.get("imgSrc", ""),
                "description": property_data.get("statusText", "")
            }
            parsed_rentals.append(rental_info)

        return {
            "total_results": len(parsed_rentals),
            "properties": parsed_rentals
        }

    except json.JSONDecodeError:
        return {"error": "Failed to parse rental data"}
    except Exception as e:
        return {"error": f"Error parsing rental data: {str(e)}"}
