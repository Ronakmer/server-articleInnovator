
import os
from django.conf import settings
from django.core.files.base import ContentFile


def dynamic_avatar_image_process(logo, avatar_image_path):
    
    print(logo, avatar_image_path,'0ronakl')
    if logo:
        print(logo,'ronakx')
        return logo

    # Ensure logo is provided either via form upload or via avatar_image_path
    if avatar_image_path:
        print(avatar_image_path,'avatar_image_paths0.')
        if avatar_image_path.startswith("/media/"):
            avatar_image_path = avatar_image_path.replace('/media/', '', 1)
                
        # Construct the full path to the avatar image
        avatar_image_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, avatar_image_path))
        print(avatar_image_path, 'avatar_image_path')
        
        # Check if the file exists and assign it to logo
        if os.path.exists(avatar_image_path):
            try:
                with open(avatar_image_path, 'rb') as f:
                    file_content = f.read()  # Read the content before the file is closed
                
                # Create a ContentFile using the file content
                logo = ContentFile(file_content, name=os.path.basename(avatar_image_path))
                print(logo, 'logo')

            except Exception as e:
                print(f"Error reading the file {avatar_image_path}: {e}")
                return None  # Or handle error as per your requirements
        else:
            print(f"File not found: {avatar_image_path}")
            return None  # Or handle the missing file as needed

    return logo
