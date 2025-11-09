"""
API Functions Package

This package contains modular API functions for the college assistant application.
Each module handles a specific type of functionality:

- weather: Weather data from OpenWeatherMap
- deals: Local deals and discounts
- sports: College football data from ESPN
- events: Event information from Ticketmaster
- calendar: Google Calendar event creation
- rentals: Rental property search via Zillow
- ai_handler: AI response handling with OpenRouter
"""

from .weather import get_weather
from .deals import get_deals
from .sports import get_college_team_data, TEAM_REFERENCE
from .events import get_events, get_events_by_city, get_music_events, get_sports_events
from .calendar import make_event, create_recurring_event, create_class_schedule
from .rentals import get_rentals, get_filtered_rentals, parse_rental_data
from .ai_handler import get_ai_response, get_default_tools

# Export all main functions
__all__ = [
    # Weather
    'get_weather',

    # Deals
    'get_deals',

    # Sports
    'get_college_team_data',
    'TEAM_REFERENCE',

    # Events
    'get_events',
    'get_events_by_city',
    'get_music_events',
    'get_sports_events',

    # Calendar
    'make_event',
    'create_recurring_event',
    'create_class_schedule',

    # Rentals
    'get_rentals',
    'get_filtered_rentals',
    'parse_rental_data',

    # AI Handler
    'get_ai_response',
    'get_default_tools'
]

# Function mapping for easy AI integration
FUNCTION_MAP = {
    "get_weather": get_weather,
    "get_deals": get_deals,
    "get_college_team_data": get_college_team_data,
    "make_event": make_event,
    "get_rentals": get_rentals,
    "get_events": get_events
}

# Package metadata
__version__ = "1.0.0"
__author__ = "TAMU Datathon Team"
__description__ = "Modular API functions for college assistant application"
