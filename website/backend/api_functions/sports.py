import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_college_team_data(team_id):
    """
    Get college football team schedule, scores, and game data using ESPN API.

    Args:
        team_id (str): ESPN team ID (refer to the team reference table)

    Returns:
        dict: Team data including live game info or full schedule
    """
    # First check for live/current game
    scoreboard_url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    try:
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
    except Exception as e:
        print(f"Error fetching scoreboard: {e}")

    # If no live game found, get full schedule
    schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/schedule"
    try:
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
    except Exception as e:
        return {"error": f"Failed to get team schedule: {str(e)}"}

# Team reference data for easy lookup
TEAM_REFERENCE = """Format: School | Nickname | ESPN_ID | Abbreviation
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
