from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.http import JsonResponse
import os 

ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']

def is_valid_image_file(file):
    if not file:
        return False
    if isinstance(file, (InMemoryUploadedFile, TemporaryUploadedFile)):
        file_extension = os.path.splitext(file.name)[1].lower()
        return file_extension in ALLOWED_IMAGE_EXTENSIONS
    return False
