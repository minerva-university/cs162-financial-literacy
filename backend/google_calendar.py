from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pytz import timezone, utc
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the variables
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'default_calendar_id@group.calendar.google.com')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'path/to/default/credentials.json')

def get_calendar_service():
    """
    Initializes the Google Calendar API service.
    """
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=creds)
    return service

def convert_to_utc(dt_str, local_tz):
    """
    Converts a datetime string in the local timezone to UTC.

    Args:
        dt_str (str): The datetime string in ISO format (e.g., '2024-12-15T10:00:00').
        local_tz (str): The local timezone (e.g., 'America/New_York').

    Returns:
        datetime: The datetime object converted to UTC.
    """
    local = timezone(local_tz)
    naive_dt = datetime.fromisoformat(dt_str)
    local_dt = local.localize(naive_dt)
    return local_dt.astimezone(utc)

def create_google_calendar_event(mentor_email, mentee_email, mentor_name, mentee_name, start_time, end_time, description='', local_tz='UTC'):
    """
    Creates a Google Calendar event for a mentorship session.

    Args:
        mentor_email (str): Email of the mentor.
        mentee_email (str): Email of the mentee.
        mentor_name (str): Name of the mentor.
        mentee_name (str): Name of the mentee.
        start_time (str): Start time in ISO format (e.g., '2024-12-15T10:00:00').
        end_time (str): End time in ISO format.
        description (str): Description of the event.
        local_tz (str): Local timezone of the start_time and end_time.

    Returns:
        str: Google Calendar event ID.
    """
    service = get_calendar_service()

    # Convert times to UTC
    start_time_utc = convert_to_utc(start_time, local_tz)
    end_time_utc = convert_to_utc(end_time, local_tz)

    event = {
        'summary': f'Mentorship Session: {mentor_name} & {mentee_name}',
        'description': description or f'Mentorship session between {mentor_name} and {mentee_name}.',
        'start': {
            'dateTime': start_time_utc.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time_utc.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': mentor_email},
            {'email': mentee_email}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event, sendUpdates='all').execute()
    return created_event.get('id')

def delete_google_calendar_event(event_id):
    """
    Deletes a Google Calendar event.
    """
    service = get_calendar_service()
    service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
