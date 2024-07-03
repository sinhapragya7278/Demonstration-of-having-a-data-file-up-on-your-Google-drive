# improting and uploading files
from google.colab import files
#connecting to the google drive
from google.colab import drive
drive.mount('/content/drive')
# Installing required libraries
!pip install pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
# Authenticating and authorizing access
import os
import pandas as pd
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import pickle
# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive']
def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
# Setting Up Service Account Authentication
import os
import pandas as pd
import io
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive']

# Path to the service account key JSON file
SERVICE_ACCOUNT_FILE = 'prime-ember.json'  # Replace with the actual file name

# Authenticate and construct service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# Get file ID and download the file (retrieving and downloading files)
def get_file_id(file_name):
    results = service.files().list(
        q=f"name='{file_name}'",
        spaces='drive',
        fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
        return None
    else:
        for item in items:
            print(f'Found file: {item["name"]} ({item["id"]})')
            return item["id"]

file_name = 'supply_chain_data.csv'  # Replace with the name of your file
file_id = get_file_id(file_name)

def download_file(file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Download {int(status.progress() * 100)}%.')

    fh.seek(0)
    return pd.read_csv(fh)

# Download the file and load it into a DataFrame
if file_id:
    df = download_file(file_id)
    print(df.head())
