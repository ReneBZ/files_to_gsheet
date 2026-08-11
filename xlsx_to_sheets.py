import os
import sys
import pickle
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

MIME_TYPES = {
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xls': 'application/vnd.ms-excel',
}


def get_credentials():
    """Gets valid user credentials from storage or initiates an OAuth2 flow."""
    creds = None
    base_path = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(base_path, 'token.pickle')
    creds_path = os.path.join(base_path, 'credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"Error: credentials.json not found at {creds_path}")
                print("Please download it from Google Cloud Console.")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def upload_excel_to_sheet(file_path):
    """Uploads an Excel file to Google Drive as a Google Sheet."""
    ext = os.path.splitext(file_path)[1].lower()
    mimetype = MIME_TYPES.get(ext)
    if not mimetype:
        print(f"Unsupported file type: {ext} (expected .xlsx or .xls)")
        return

    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }

    media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)

    try:
        print(f"Uploading {file_name}...")
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='webViewLink'
        ).execute()

        web_view_link = file.get('webViewLink')
        print(f"Upload successful! Opening {web_view_link}")
        webbrowser.open(web_view_link)

    except Exception as e:
        print(f"An error occurred while uploading {file_name}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python xlsx_to_sheets.py <file_path> [file_path ...]")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        if os.path.exists(file_path):
            upload_excel_to_sheet(file_path)
        else:
            print(f"File not found: {file_path}")


if __name__ == '__main__':
    main()
