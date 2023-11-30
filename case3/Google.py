import os.path
import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    # print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    # print(SCOPES)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        # print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
    
def create_calendar_event(service, summary, start_time, duration, location, attendees):
    # Waktu mulai dan selesai event
    start = start_time.isoformat()
    end = (start_time + datetime.timedelta(minutes=duration)).isoformat()

    # Membuat objek event
    event = {
        'summary': summary,
        'start': {'dateTime': start, 'timeZone': 'Asia/Jakarta'},
        'end': {'dateTime': end, 'timeZone': 'Asia/Jakarta'},
        'location': location,
        'attendees': [{'email': attendee} for attendee in attendees],
        'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 720}]},
        'sendNotifications': True,
        'sendUpdates': 'externalOnly'
    }

    # Mengirim permintaan untuk membuat event
    created_event = service.events().insert(calendarId='primary', body=event).execute()

    print(f"Event '{summary}' berhasil dibuat dengan ID: {created_event['id']}")
    return created_event

# Fungsi untuk mengirim email
def send_invitation_email(sender, password, recipients, subject, body):
    # Konfigurasi email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    # Tambahkan konten email
    msg.attach(MIMEText(body, 'plain'))

    # Tambahkan lampiran event calendar
    # ics_attachment = MIMEText(calendar_event, 'calendar')
    # ics_attachment.add_header('Content-Disposition', 'attachment', filename='event.ics')
    # msg.attach(ics_attachment)

    # Kirim email menggunakan SMTP
    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

    print(f"Email terkirim ke {recipients}")