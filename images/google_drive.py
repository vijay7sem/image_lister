import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.shortcuts import render

CREDENTIALS_FILE = "client_secrets.json"
gauth = GoogleAuth()
def authenticate_google_drive():
    """Authenticate and create a GoogleDrive instance using stored credentials."""
    gauth.LoadCredentialsFile(CREDENTIALS_FILE)
    
    if gauth.credentials is None:
        # Authenticate and save credentials if not already present
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    elif gauth.access_token_expired:
        # Refresh the tokens if expired
        gauth.Refresh()
    else:
        gauth.Authorize()  # Authorize if valid tokens are present

    gauth.SaveCredentialsFile(CREDENTIALS_FILE)  # Save credentials
    return GoogleDrive(gauth)
# def authenticate_google_drive():
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()
#     return GoogleDrive(gauth)

def upload_file_to_drive(file):
    # Create a temporary file path
    temp_file_name = f"temp_{file.name}"
    temp_file_path = default_storage.save(temp_file_name, ContentFile(file.read()))

    # Authenticate and create a GoogleDrive instance
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authenticate
    drive = GoogleDrive(gauth)

    # Create a GoogleDriveFile instance
    gfile = drive.CreateFile({'title': file.name})
    
    # Set the content from the temporary file
    gfile.SetContentFile(default_storage.path(temp_file_path))
    gfile.Upload()  # Upload the file

    return gfile['id']  # Return the file ID


def list_files_from_drive(folder_id, max_results=5):
    """List a limited number of files from a specified folder in Google Drive."""
    # Authenticate and create the Google Drive instance
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentication flow
    drive = GoogleDrive(gauth)
    
    # Query to get files from the specified folder
    query = f"'{folder_id}' in parents and (mimeType='image/jpeg' or mimeType='image/png')"
    file_list = drive.ListFile({'q': query, 'maxResults': max_results}).GetList()
    
    # Prepare the list of files to return
    files = []
    for file in file_list:
        files.append({
            'id': file['id'],
            'title': file['title'],
            'webContentLink': file['webContentLink']  # URL to view or download the file
        })
    
    return files
