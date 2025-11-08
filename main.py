import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json
import apis

load_dotenv()

OPENROUTERKEY = os.environ.get("key")

if not OPENROUTERKEY:
    raise ValueError("No openrouter key")

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

function_map = {
    "get_weather": apis.get_weather,
    "get_deals": apis.get_deals,
    "get_college_team_data": apis.get_college_team_data,
    "make_event": apis.make_event
}

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <html><body>
      <h2>MCP Chat</h2>
      <input type="text" id="msg" placeholder="Type a message" style="width:400px">
      <button onclick="send()">Send</button>
      <div id="output" style="margin-top:20px; white-space:pre-wrap;"></div>
      <script>
        async function send(){
          const msg = document.getElementById("msg").value;
          document.getElementById("output").innerText = "Loading...";
          try {
            const res = await fetch("/send", {
              method:"POST",
              headers:{"Content-Type":"application/json"},
              body: JSON.stringify({message: msg})
            });
            const data = await res.json();
            
            if(data.calendar_url) {
              document.getElementById("output").innerHTML = data.response + 
                '<br><br><a href="' + data.calendar_url + '" target="_blank" style="background:#4285f4;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:10px;">Add to Google Calendar</a>';
            } else {
              document.getElementById("output").innerText = data.response;
            }
          } catch(e) {
            document.getElementById("output").innerText = "Error: " + e.message;
          }
        }
      </script>
    </body></html>
    """

@app.route("/send", methods=["POST"])
def send():
    try:
        user_msg = request.json["message"]
        
        headers = {
            "Authorization": f"Bearer {OPENROUTERKEY}",
            "Content-Type": "application/json"
        }
        
        tools = [
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
                    "description": f"Get college football team schedule, scores, and game data. Use the ESPN_ID from this reference:\n{TEAM_REFERENCE}",
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
            }
        ]
        
        messages = [
            {
                "role": "system",
                "content": f"You are a helpful assistant with access to weather data, deals, college football information, and calendar event creation. When users ask about college football teams, use the get_college_team_data function with the ESPN_ID from this reference:\n{TEAM_REFERENCE}\n\nWhen creating calendar events, use ISO datetime format (YYYY-MM-DDTHH:MM:SS). Current date is 2025-11-08."
            },
            {
                "role": "user",
                "content": user_msg
            }
        ]
        
        payload = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": messages,
            "tools": tools
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        
        message = result["choices"][0]["message"]
        calendar_url = None
        
        if message.get("tool_calls"):
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            if function_name in function_map:
                print(f"Calling {function_name} with args: {function_args}")
                function_response = function_map[function_name](**function_args)
                
                if function_name == "make_event" and function_response.startswith("https://"):
                    calendar_url = function_response
                    function_response = "Calendar event created successfully!"
                
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(function_response)
                })
                
                payload["messages"] = messages
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                ai_response = result["choices"][0]["message"]["content"]
                
                if calendar_url:
                    return jsonify({"response": ai_response, "calendar_url": calendar_url})
                return jsonify({"response": ai_response})
        
        ai_response = message.get("content", "No response")
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)