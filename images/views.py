from django.shortcuts import render, redirect
from .models import Image
from .google_drive import upload_file_to_drive, list_files_from_drive

def upload_image(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return HttpResponseBadRequest("No file uploaded")

        file = request.FILES['file']  # Get the uploaded file
        file_id = upload_file_to_drive(file)  # Upload the file to Google Drive

        return render(request, 'upload.html', {'message': 'File uploaded successfully', 'file_id': file_id})

    return render(request, 'upload.html')

def image_list(request):
    """Retrieve and display a limited number of images from Google Drive."""
    files = list_files_from_drive(folder_id="1rQ0S1rmbIsVEGfK-TnYMybwafsyeNwIo", max_results=5)
    print("Files:", files)
    #files = [{'id': '1g4GGH-xR__H6ApormrDkqmt5Ydr1-ZCD', 'title': 'developer.png', 'webContentLink': 'https://drive.google.com/uc?id=1g4GGH-xR__H6ApormrDkqmt5Ydr1-ZCD&export=download'}, {'id': '14gA8uWN8_5CymeRj6XVd8hFO2kypa0D_', 'title': 'bg.png', 'webContentLink': 'https://drive.google.com/uc?id=14gA8uWN8_5CymeRj6XVd8hFO2kypa0D_&export=download'}]
    return render(request, 'image_list.html', {'files': files})