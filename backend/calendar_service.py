from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class CalendarService:
  def __init__(self, access_token):
    creds = Credentials(token=access_token)
    self.service = build('calendar', 'v3', credentials=creds)
  def add_to_calendar(self, info):
    name = info["class_name"]
    location = info["location"]
    assignments = info["assignments"]

    events = []
    for (date, assignment) in assignments:
      event = {
        "summary": f"{name} - {assignment}",
        "location": location,
        "description": f"Assignment for {name}: {assignment}",
        "start": {
            "date": date
        },
        "end": {
            "date": date 
        },
      }

      created_event = (
        self.service.events()
        .insert(calendarId="primary", body=event)
        .execute()
      )
      events.append(created_event)
      
    return events
  
  def create_event(self, summary, description, due_date):
    event_body = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": due_date,
            "timeZone": 'America/Los_Angeles'
        },
        "end": {
            "dateTime": due_date,
            "timeZone": 'America/Los_Angeles'
        },
    }

    created_event = (
        self.service.events()
        .insert(calendarId="primary", body=event_body)
        .execute()
    )
    return created_event

  def update_event(self, event_id, summary=None, description=None, due_date=None):
    event = self.service.events().get(calendarId="primary", eventId=event_id).execute()
    if summary is not None:
        event["summary"] = summary
    if description is not None:
        event["description"] = description
    if due_date is not None:
        event["start"] = {"date": due_date}
        event["end"] = {"date": due_date }

    updated_event = (
        self.service.events()
        .update(calendarId="primary", eventId=event_id, body=event)
        .execute()
    )
    return updated_event

  def delete_event(self, event_id):
    self.service.events().delete(calendarId="primary", eventId=event_id).execute()
    return True





  