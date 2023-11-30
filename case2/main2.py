import numpy as np

from googleapiclient.errors import HttpError

from Google import read_gsheet, Create_Service, generate_unique_folder_name
from Google import create_folder_in_parent, set_folder_permissions

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive']

def main():
    try:
        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1TGj2Q-3geoRAdhZfjGfUaeadA0YUpUY7S5yYsR3r-k8'
        SAMPLE_RANGE_NAME = 'Sheet1!A:A'
        sheets_service = Create_Service('credentials.json', 'sheets', 'v4', SCOPES)
        new_folder_names = read_gsheet(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, sheets_service)
        new_folder_names = np.array(new_folder_names).transpose().tolist()[0]
        print("NEW FOLDER:\n\t", new_folder_names)

        # Works with Google Drive
        drive_service = Create_Service('credentials.json', 'drive', 'v3', SCOPES)
        for folder_name in new_folder_names:
            unique_folder_name = generate_unique_folder_name(drive_service,
                                                            '1rxe3uHZpTZa5HIz55EjXugeqKxX6e1-K',
                                                            folder_name)
        
            folder_id = create_folder_in_parent(drive_service, '1G0VCBSSGo1gLDLrGGoK106ESBlhmEgdK', unique_folder_name)
            print(f"Created {unique_folder_name} folder with ID: {folder_id}")
            set_folder_permissions(drive_service, folder_id)

    except HttpError as err:
        print('\n', err)

if __name__ == '__main__':
    main()