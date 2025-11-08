import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import quote_plus

load_dotenv()

deals_key = os.environ.get("deals_key")

def get_weather(location: str) -> str:
    query = quote_plus(location)
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    response = requests.get(url, headers={"User-Agent": "geo-coord-fetcher"})
    data = response.json()
    
    if not data:
        return "Error: Location not found"
    
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    
    print(f"Fetching weather for {location} (lat={lat}, lon={lon})")
    weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    weather_response = requests.get(weather_url)
    
    if weather_response.status_code != 200:
        return f"Failed to get weather: {weather_response.text}"
    
    weather_data = weather_response.json()
    return str(weather_data)

def get_deals(location: str) -> str:
    url = f'https://api.discountapi.com/v2/deals?api_key={deals_key}&location={location}'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to get deals: {response.text}"
    data = response.json()
    return str(data)

def get_college_team_data(team_id):
    scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    resp = requests.get(scoreboard_url)
    resp.raise_for_status()
    scoreboard = resp.json()
    
    for event in scoreboard.get("events", []):
        comp = event.get("competitions", [])[0]
        competitors = comp.get("competitors", [])
        status = comp.get("status", {}).get("type", {}).get("description", "Unknown")
        
        for competitor in competitors:
            if competitor["team"]["id"] == str(team_id):
                opp = [c for c in competitors if c["team"]["id"] != str(team_id)][0]
                return {
                    "type": "live_game",
                    "team": competitor["team"]["displayName"],
                    "opponent": opp["team"]["displayName"],
                    "team_score": competitor.get("score", "0"),
                    "opponent_score": opp.get("score", "0"),
                    "status": status,
                    "game_date": comp.get("date"),
                    "venue": comp.get("venue", {}).get("fullName", "")
                }
    
    schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/schedule"
    sched_resp = requests.get(schedule_url)
    sched_resp.raise_for_status()
    schedule = sched_resp.json()
    
    events = schedule.get("events", [])
    if not events:
        return {"error": "No schedule data found for this team."}
    
    full_schedule = []
    for event in events:
        comp = event.get("competitions", [])[0]
        competitors = comp.get("competitors", [])
        status = comp.get("status", {}).get("type", {}).get("description", "")
        date_str = event.get("date", "")
        
        try:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except Exception:
            date = date_str
        
        team_data = None
        opp_data = None
        for c in competitors:
            if c["team"]["id"] == str(team_id):
                team_data = c
            else:
                opp_data = c
        
        full_schedule.append({
            "date": date,
            "opponent": opp_data["team"]["displayName"] if opp_data else "Unknown",
            "team_score": team_data.get("score", ""),
            "opponent_score": opp_data.get("score", ""),
            "status": status
        })
    
    return {
        "type": "full_schedule",
        "team": schedule.get("team", {}).get("displayName", ""),
        "games": full_schedule
    }

def make_event(title: str, start_datetime: str, end_datetime: str, description: str = "", location: str = "") -> str:
    try:
        start_dt = datetime.fromisoformat(start_datetime.replace("Z", ""))
        end_dt = datetime.fromisoformat(end_datetime.replace("Z", ""))
        
        start_formatted = start_dt.strftime("%Y%m%dT%H%M%S")
        end_formatted = end_dt.strftime("%Y%m%dT%H%M%S")
        
        google_calendar_url = (
            f"https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text={quote_plus(title)}"
            f"&dates={start_formatted}/{end_formatted}"
            f"&details={quote_plus(description)}"
            f"&location={quote_plus(location)}"
        )
        
        return google_calendar_url
    except Exception as e:
        return f"Error creating event: {str(e)}"