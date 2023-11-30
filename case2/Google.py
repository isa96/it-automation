import os.path
import datetime

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def read_gsheet(spreadsheet_id, range, service):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    return values[1:]

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

def create_folder_in_parent(service, parent_id, folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }

    file = service.files().create(body=file_metadata).execute()
    return file.get('id')

# Check if the name folder is already exists
def check_folder_name(service, parent_folder_id, folder_name):
    results = service.files().list(q=f"'{parent_folder_id}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                                   fields="files(id)").execute()
    
    return len(results.get('files', [])) > 0

# Generate unique folder name if the name is already exists
def generate_unique_folder_name(service, parent_folder_id, folder_name):
    suffix = 1
    new_folder_name = folder_name
    while check_folder_name(service, parent_folder_id, new_folder_name):
        suffix += 1
        new_folder_name = f"{folder_name} ({suffix})"
    
    return new_folder_name

# Set permission of a folder to everyone has the link can view this folder
def set_folder_permissions(service, folder_id):
    permission = {
        'type': 'anyone',
        'role': 'reader',
        'allowFileDiscovery': False
    }
    service.permissions().create(fileId=folder_id, body=permission).execute()
