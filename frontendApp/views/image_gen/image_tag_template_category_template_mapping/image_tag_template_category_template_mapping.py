

from django.shortcuts import render,redirect

# Create your views here.


# def add_image_tag_template_category_template_mapping_page(request):
#     try:
#         return render(request,'frontendApp/image_tag_template_category_template_mapping/add_image_tag_template_category_template_mapping.html')
#     except Exception as e:
#         print("This error is add_image_tag_template_category_template_mapping_page --->: ",e)
#         return render(request, 'error.html' , {'error': 500})



def list_image_tag_template_category_template_mapping_page(request):
    try:
        return render(request,'imageGen/layout.html')
    except Exception as e:
        print("This error is list_image_tag_template_category_template_mapping_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

# def update_image_tag_template_category_template_mapping_page(request, slug_id):
#     try:
#         return render(request,'frontendApp/image_tag_template_category_template_mapping/add_image_tag_template_category_template_mapping.html')
#     except Exception as e:
#         print("This error is update_image_tag_template_category_template_mapping_page --->: ",e)
#         return render(request, 'error.html' , {'error': 500})

