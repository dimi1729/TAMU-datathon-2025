import os
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import quote_plus

load_dotenv()

def make_event(title: str, start_datetime: str, end_datetime: str, description: str = "", location: str = "") -> str:
    """
    Create a calendar event that can be added to Google Calendar.

    Args:
        title (str): Event title
        start_datetime (str): Start date and time in ISO format (e.g., '2025-11-15T14:00:00')
        end_datetime (str): End date and time in ISO format (e.g., '2025-11-15T16:00:00')
        description (str, optional): Event description
        location (str, optional): Event location

    Returns:
        str: Google Calendar URL for adding the event, or error message if failed
    """
    try:
        # Parse ISO datetime strings
        start_dt = datetime.fromisoformat(start_datetime.replace("Z", ""))
        end_dt = datetime.fromisoformat(end_datetime.replace("Z", ""))

        # Format for Google Calendar (YYYYMMDDTHHMMSS)
        start_formatted = start_dt.strftime("%Y%m%dT%H%M%S")
        end_formatted = end_dt.strftime("%Y%m%dT%H%M%S")

        # Build Google Calendar URL
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

def create_recurring_event(title: str, start_datetime: str, end_datetime: str,
                         recurrence_rule: str, description: str = "", location: str = "") -> str:
    """
    Create a recurring calendar event.

    Args:
        title (str): Event title
        start_datetime (str): Start date and time in ISO format
        end_datetime (str): End date and time in ISO format
        recurrence_rule (str): RRULE string (e.g., 'FREQ=WEEKLY;BYDAY=MO,WE,FR')
        description (str, optional): Event description
        location (str, optional): Event location

    Returns:
        str: Google Calendar URL for adding the recurring event, or error message if failed
    """
    try:
        # Parse ISO datetime strings
        start_dt = datetime.fromisoformat(start_datetime.replace("Z", ""))
        end_dt = datetime.fromisoformat(end_datetime.replace("Z", ""))

        # Format for Google Calendar
        start_formatted = start_dt.strftime("%Y%m%dT%H%M%S")
        end_formatted = end_dt.strftime("%Y%m%dT%H%M%S")

        # Build Google Calendar URL with recurrence
        google_calendar_url = (
            f"https://calendar.google.com/calendar/render?action=TEMPLATE"
            f"&text={quote_plus(title)}"
            f"&dates={start_formatted}/{end_formatted}"
            f"&details={quote_plus(description)}"
            f"&location={quote_plus(location)}"
            f"&recur={quote_plus(recurrence_rule)}"
        )

        return google_calendar_url

    except Exception as e:
        return f"Error creating recurring event: {str(e)}"

def create_class_schedule(course_name: str, days: list, start_time: str, end_time: str,
                         semester_start: str, semester_end: str, location: str = "") -> str:
    """
    Helper function to create a recurring class schedule.

    Args:
        course_name (str): Name of the course
        days (list): List of weekdays (e.g., ['MO', 'WE', 'FR'])
        start_time (str): Start time in HH:MM format (e.g., '14:00')
        end_time (str): End time in HH:MM format (e.g., '15:30')
        semester_start (str): Semester start date in YYYY-MM-DD format
        semester_end (str): Semester end date in YYYY-MM-DD format
        location (str, optional): Classroom location

    Returns:
        str: Google Calendar URL for the class schedule
    """
    try:
        # Create start and end datetime strings
        start_datetime = f"{semester_start}T{start_time}:00"
        end_datetime = f"{semester_start}T{end_time}:00"

        # Build recurrence rule for class schedule
        days_str = ",".join(days)
        until_date = datetime.fromisoformat(semester_end).strftime("%Y%m%d")
        recurrence_rule = f"FREQ=WEEKLY;BYDAY={days_str};UNTIL={until_date}"

        return create_recurring_event(
            title=course_name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            recurrence_rule=recurrence_rule,
            description=f"Class schedule for {course_name}",
            location=location
        )

    except Exception as e:
        return f"Error creating class schedule: {str(e)}"
