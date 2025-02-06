
from rest_framework import status
from imagekitio import ImageKit
from django.conf import settings
from django.http import JsonResponse


import base64
from imagekitio.models import UploadFileRequestOptions


imagekit = ImageKit(
    private_key=settings.IMAGEKIT['PRIVATE_KEY'],
    public_key=settings.IMAGEKIT['PUBLIC_KEY'],
    url_endpoint=settings.IMAGEKIT['URL_ENDPOINT']
)


            
def upload_to_imagekit(image):
    try:
        url = "https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB.jpg"
        upload = imagekit.upload_file(
                file=url,
                file_name=image,
                options=UploadFileRequestOptions(
                    response_fields=["is_private_file", "tags"],
                    tags=["tag1", "tag2"]
                )
            )
        return upload  # The response from ImageKit
    
    
    except Exception as e:
        print("Error uploading to ImageKit:", e)
        return None






#         # url = "https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB.jpg"
#         # upload = imagekit.upload_file(
#         #         file=url,
#         #         file_name=image,
#         #         options=UploadFileRequestOptions(
#         #             response_fields=["is_private_file", "tags"],
#         #             tags=["tag1", "tag2"]
#         #         )
#         #     )



# # if 'url' in response:
# #     return response['url']
