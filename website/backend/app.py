import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# Import the modular API functions
from api_functions import (
    get_weather, get_deals, get_college_team_data, make_event,
    get_rentals, get_events, get_ai_response, get_default_tools, FUNCTION_MAP
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Mock data for college-specific responses
COLLEGE_DATA = {
    "sports": {
        "general": "Check your college athletics website for game schedules and team updates",
        "basketball": "Basketball season runs from November through March",
        "football": "Football season typically runs from August through December"
    },
    "food": {
        "dining": "Most colleges offer multiple dining halls with various meal plan options",
        "restaurants": "Popular college food spots often include pizza places, coffee shops, and casual dining"
    },
    "housing": {
        "on_campus": "On-campus housing typically includes residence halls and apartment-style living",
        "off_campus": "Off-campus options vary by location - consider proximity to campus and transportation"
    },
    "events": {
        "upcoming": "Check your student portal or campus events calendar for current activities"
    },
    "academics": {
        "general": "Use your student portal for course registration, grades, and academic resources",
        "support": "Most colleges offer tutoring centers, writing labs, and academic advising"
    }
}

def process_student_query_ai(message):
    """AI-powered response system using OpenRouter and modular APIs"""
    try:
        # Get the default tools and function mapping
        tools = get_default_tools()

        # Get AI response with access to all API functions
        result = get_ai_response(
            user_message=message,
            tools=tools,
            function_map=FUNCTION_MAP
        )

        return result

    except Exception as e:
        print(f"AI query error: {str(e)}")
        # Fallback to simple response
        return {"response": "I'm having trouble processing your request right now. Please try again later."}

def process_student_query_simple(message):
    """Simple keyword-based response system for fallback"""
    message_lower = message.lower()

    # Check for sports keywords
    if any(word in message_lower for word in ["sport", "football", "basketball", "game", "athletics"]):
        if "football" in message_lower:
            return {"response": COLLEGE_DATA["sports"]["football"]}
        elif "basketball" in message_lower:
            return {"response": COLLEGE_DATA["sports"]["basketball"]}
        else:
            return {"response": COLLEGE_DATA["sports"]["general"]}

    # Check for food keywords
    elif any(word in message_lower for word in ["food", "dining", "eat", "restaurant", "hungry", "meal"]):
        if "dining" in message_lower or "meal" in message_lower:
            return {"response": COLLEGE_DATA["food"]["dining"]}
        else:
            return {"response": COLLEGE_DATA["food"]["restaurants"]}

    # Check for housing keywords
    elif any(word in message_lower for word in ["apartment", "housing", "dorm", "residence", "live", "room"]):
        return {"response": COLLEGE_DATA["housing"]["on_campus"] + " " + COLLEGE_DATA["housing"]["off_campus"]}

    # Check for events
    elif any(word in message_lower for word in ["event", "activity", "happening", "club", "organization"]):
        return {"response": COLLEGE_DATA["events"]["upcoming"]}

    # Check for classes/academic
    elif any(word in message_lower for word in ["class", "course", "professor", "grade", "academic", "study", "tutor"]):
        return {"response": COLLEGE_DATA["academics"]["general"] + " " + COLLEGE_DATA["academics"]["support"]}

    # Check for calendar/schedule
    elif any(word in message_lower for word in ["calendar", "schedule", "time", "when", "date"]):
        return {"response": "I can help you manage your calendar. You can add events, set reminders, and track important dates."}

    # Check for email
    elif any(word in message_lower for word in ["email", "message", "contact", "professor", "send"]):
        return {"response": "I can assist with composing emails to professors, advisors, or student organizations."}

    # Default response
    else:
        return {"response": ("Hello! I'm your college assistant. I can help you with:\n"
                "• Sports and athletics information (including live scores!)\n"
                "• Weather updates for your area\n"
                "• Local deals and discounts\n"
                "• Dining and food options\n"
                "• Housing and rental property search\n"
                "• Campus and local events\n"
                "• Academic resources and support\n"
                "• Calendar management and event creation\n"
                "• Email assistance\n"
                "What would you like to know about?")}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "College Assistant Backend API",
        "status": "running",
        "endpoints": {
            "/api/chat": "POST - Send chat messages",
            "/api/health": "GET - Health check"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "College Assistant Backend"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                "error": "No message provided",
                "status": "error"
            }), 400

        user_message = data['message']

        # Try AI-powered response first, fallback to simple if needed
        try:
            result = process_student_query_ai(user_message)

            # Check if AI returned an error
            if "error" in result:
                print(f"AI error: {result['error']}")
                result = process_student_query_simple(user_message)

            response_data = {
                "response": result.get("response", "I couldn't process your request."),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }

            # Add calendar URL if present
            if result.get("calendar_url"):
                response_data["calendar_url"] = result["calendar_url"]

            return jsonify(response_data)

        except Exception as e:
            print(f"Chat error: {str(e)}")
            # Fallback to simple response
            result = process_student_query_simple(user_message)
            return jsonify({
                "response": result.get("response", "I'm having trouble right now. Please try again."),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/calendar', methods=['POST'])
def add_to_calendar():
    """Placeholder for Google Calendar integration"""
    try:
        data = request.get_json()
        event_title = data.get('title', '')
        event_date = data.get('date', '')

        # TODO: Integrate with Google Calendar API
        return jsonify({
            "message": f"Calendar feature coming soon! Would add: {event_title} on {event_date}",
            "status": "placeholder"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/email', methods=['POST'])
def send_email():
    """Placeholder for email functionality"""
    try:
        data = request.get_json()
        recipient = data.get('to', '')
        subject = data.get('subject', '')
        body = data.get('body', '')

        # TODO: Integrate with email service
        return jsonify({
            "message": f"Email feature coming soon! Would send to: {recipient}",
            "status": "placeholder"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("Starting College Assistant Backend...")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print(f"Running on port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
