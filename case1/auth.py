import gspread
from oauth2client.service_account import ServiceAccountCredentials

def auth(api_key):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    
    # Reading Credentails from ServiceAccount Keys file
    credentials = ServiceAccountCredentials.from_json_keyfile_name(api_key, 
                                                                   scope)
    
    # intitialize authorization object            
    gc = gspread.authorize(credentials)
    return gc
