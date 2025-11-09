import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTERKEY = os.environ.get("key")

def get_ai_response(user_message: str, tools: list = None, function_map: dict = None) -> dict:
    """
    Get AI response from OpenRouter using Claude model with optional function calling.

    Args:
        user_message (str): User's message/query
        tools (list, optional): List of available tools/functions
        function_map (dict, optional): Dictionary mapping function names to actual functions

    Returns:
        dict: Response containing AI message and any function results
    """
    if not OPENROUTERKEY:
        return {"error": "Missing OpenRouter API key"}

    headers = {
        "Authorization": f"Bearer {OPENROUTERKEY}",
        "Content-Type": "application/json"
    }

    # Team reference data for sports queries
    team_reference = """Format: School | Nickname | ESPN_ID | Abbreviation
Ohio State        | Buckeyes       | 194  | OSU
Indiana           | Hoosiers       | 84   | IND
Texas A&M         | Aggies         | 245  | TAMU
Alabama           | Crimson Tide   | 333  | ALA
Georgia           | Bulldogs       | 61   | UGA
Ole Miss          | Rebels         | 145  | MISS
BYU               | Cougars        | 252  | BYU
Texas Tech        | Red Raiders    | 2641 | TTU
Oregon            | Ducks          | 2483 | ORE
Notre Dame        | Fighting Irish | 87   | ND
Tennessee         | Volunteers     | 2633 | TENN
Miami             | Hurricanes     | 2390 | MIA
Texas             | Longhorns      | 251  | TEX
Virginia          | Cavaliers      | 258  | UVA
Penn State        | Nittany Lions  | 213  | PSU
Clemson           | Tigers         | 228  | CLEM
Boise State       | Broncos        | 68   | BSU
LSU               | Tigers         | 99   | LSU
SMU               | Mustangs       | 2567 | SMU
Iowa              | Hawkeyes       | 2294 | IOWA
South Carolina    | Gamecocks      | 2579 | SC
Missouri          | Tigers         | 142  | MIZZOU
Kansas State      | Wildcats       | 2306 | KSU
Louisville        | Cardinals      | 97   | LOU
Colorado          | Buffaloes      | 38   | COLO
## OTHER MAJOR PROGRAMS
Michigan          | Wolverines     | 130  | MICH
USC               | Trojans        | 30   | USC
Oklahoma          | Sooners        | 201  | OU
Nebraska          | Cornhuskers    | 158  | NEB
Florida           | Gators         | 57   | FLA
Florida State     | Seminoles      | 52   | FSU
Auburn            | Tigers         | 2    | AUB
Wisconsin         | Badgers        | 275  | WISC
UCLA              | Bruins         | 26   | UCLA
Michigan State    | Spartans       | 127  | MSU
Washington        | Huskies        | 264  | WASH
Stanford          | Cardinal       | 24   | STAN
Arkansas          | Razorbacks     | 8    | ARK
Oklahoma State    | Cowboys        | 197  | OKST
TCU               | Horned Frogs   | 2628 | TCU
Baylor            | Bears          | 239  | BAY
Utah              | Utes           | 254  | UTAH
Oregon State      | Beavers        | 204  | ORST
Arizona State     | Sun Devils     | 9    | ASU
Arizona           | Wildcats       | 12   | ARIZ
West Virginia     | Mountaineers   | 277  | WVU
Iowa State        | Cyclones       | 66   | ISU
Pittsburgh        | Panthers       | 221  | PITT
NC State          | Wolfpack       | 152  | NCST
North Carolina    | Tar Heels      | 153  | UNC
Duke              | Blue Devils    | 150  | DUKE
Virginia Tech     | Hokies         | 259  | VT
Georgia Tech      | Yellow Jackets | 59   | GT
Kentucky          | Wildcats       | 96   | UK
Vanderbilt        | Commodores     | 238  | VANDY
Mississippi State | Bulldogs       | 344  | MSST
Texas State       | Bobcats        | 326  | TXST
UCF               | Knights        | 2116 | UCF
Houston           | Cougars        | 248  | HOU
Cincinnati        | Bearcats       | 2132 | CIN"""

    messages = [
        {
            "role": "system",
            "content": f"You are a helpful college assistant with access to weather data, deals, college football information, calendar event creation, rental property search, and local events via Ticketmaster. When users ask about college football teams, use the get_college_team_data function with the ESPN_ID from this reference:\n{team_reference}\n\nWhen creating calendar events, use ISO datetime format (YYYY-MM-DDTHH:MM:SS). Current date is 2025-11-08. For event searches, you may need to first get coordinates for a location. Always provide helpful, student-focused responses."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": messages
    }

    # Add tools if provided
    if tools:
        payload["tools"] = tools

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()

        message = result["choices"][0]["message"]
        calendar_url = None

        # Handle function calls if present
        if message.get("tool_calls") and function_map:
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])

            if function_name in function_map:
                print(f"Calling {function_name} with args: {function_args}")
                function_response = function_map[function_name](**function_args)

                # Special handling for calendar events
                if function_name == "make_event" and function_response.startswith("https://"):
                    calendar_url = function_response
                    function_response = "Calendar event created successfully!"

                # Add function call and response to conversation
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(function_response)
                })

                # Get final AI response
                payload["messages"] = messages
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()

                ai_response = result["choices"][0]["message"]["content"]

                return {
                    "response": ai_response,
                    "calendar_url": calendar_url,
                    "function_called": function_name,
                    "function_args": function_args
                }

        # Return direct AI response if no function calls
        ai_response = message.get("content", "No response")
        return {"response": ai_response}

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse API response: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_default_tools():
    """
    Get the default set of tools available to the AI assistant.

    Returns:
        list: List of tool definitions for the AI model
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a location by name (e.g., 'New York', 'London', 'Tokyo')",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Name of the location (city, address, or place name)"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_deals",
                "description": "Get deals and discounts for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location to search for deals"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_college_team_data",
                "description": "Get college football team schedule, scores, and game data. Use the ESPN_ID from the team reference table.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_id": {
                            "type": "string",
                            "description": "ESPN team ID (refer to the team reference table)"
                        }
                    },
                    "required": ["team_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "make_event",
                "description": "Create a calendar event that can be added to Google Calendar. Dates should be in ISO format (YYYY-MM-DDTHH:MM:SS)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Event title"
                        },
                        "start_datetime": {
                            "type": "string",
                            "description": "Start date and time in ISO format (e.g., '2025-11-15T14:00:00')"
                        },
                        "end_datetime": {
                            "type": "string",
                            "description": "End date and time in ISO format (e.g., '2025-11-15T16:00:00')"
                        },
                        "description": {
                            "type": "string",
                            "description": "Event description (optional)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Event location (optional)"
                        }
                    },
                    "required": ["title", "start_datetime", "end_datetime"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_rentals",
                "description": "Search for rental properties in a specific location using Zillow data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location to search for rentals (e.g., 'college station, tx', 'new york, ny')"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_events",
                "description": "Get nearby events from Ticketmaster based on latitude and longitude coordinates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lat": {
                            "type": "number",
                            "description": "Latitude coordinate"
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude coordinate"
                        },
                        "radius": {
                            "type": "integer",
                            "description": "Search radius (default: 10)"
                        },
                        "unit": {
                            "type": "string",
                            "description": "Distance unit: 'miles' or 'km' (default: 'miles')"
                        },
                        "keyword": {
                            "type": "string",
                            "description": "Optional keyword to filter events"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Optional start date in ISO format"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "Optional end date in ISO format"
                        },
                        "size": {
                            "type": "integer",
                            "description": "Number of results to return (default: 20)"
                        }
                    },
                    "required": ["lat", "lon"]
                }
            }
        }
    ]
