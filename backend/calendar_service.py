from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class CalendarService:
  def __init__(self, provider_token):
    creds = Credentials(token=provider_token)
    self.service = build('calendar', 'v3', credentials=creds)
  def add_to_calendar(self, info):
    now = datetime.utcnow().isoformat() + 'Z'
    result = self.service.events().list(calendarId='primary', timeMin=now, eventTypes='default', maxResults=10, singleEvents=True, orderBy='updated').execute()
    events = result.get('items', [])

    return events




  