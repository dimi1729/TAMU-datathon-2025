import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json

load_dotenv()

OPENROUTERKEY = os.environ.get("key")

def get_weather(lat: float, lon: float) -> str:
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to get weather: {response.text}"
    data = response.json()
    return str(data)

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
            document.getElementById("output").innerText = data.response;
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
                    "name": "weather_tool",
                    "description": "Get current weather for a location given latitude and longitude",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lat": {
                                "type": "number",
                                "description": "Latitude of the location"
                            },
                            "lon": {
                                "type": "number",
                                "description": "Longitude of the location"
                            }
                        },
                        "required": ["lat", "lon"]
                    }
                }
            },
        ]
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant with access to weather data. When users ask about weather, use the weather_tool function with latitude and longitude."
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
        
        if message.get("tool_calls"):
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            if function_name == "weather_tool":
                function_response = get_weather(function_args["lat"], function_args["lon"])
                
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": function_response
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
                return jsonify({"response": ai_response})
        
        ai_response = message.get("content", "No response")
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)