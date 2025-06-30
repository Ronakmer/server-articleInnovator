from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from apiApp.models import article_type, variables, prompt, domain, wp_category, wp_author, wp_tag  # Make sure all models are imported













# @api_view(['GET'])
# def replace_output_variable_for_article_type(request):
#     try:
#         prompt_slug_id = request.GET.get('prompt_slug_id')
#         domain_slug_id = request.GET.get('domain_slug_id')

#         # if not prompt_slug_id or not domain_slug_id:
#         #     return JsonResponse({"error": "Missing prompt_slug_id or domain_slug_id", "success": False}, status=400)

#         # Fetch prompt and article_type
#         prompt_obj = prompt.objects.filter(slug_id=prompt_slug_id).first()
#         if not prompt_obj:
#             return JsonResponse({"error": "Prompt not found", "success": False}, status=404)

#         article_type_obj = prompt_obj.article_type_id
#         if not article_type_obj:
#             return JsonResponse({"error": "Article type not found", "success": False}, status=404)

#         # Get prompt_data
#         prompt_data = prompt_obj.prompt_data or {}

#         # Fetch variable queryset
#         variable_qs = variables.objects.filter(article_type_id=article_type_obj.id, use_exact_value=True)
#         if not variable_qs.exists():
#             return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

#         # Identify category-type variable
#         category_keywords = ['category', 'categories']
#         category_variable = None
#         for var in variable_qs:
#             if any(keyword in var.name.lower() for keyword in category_keywords):
#                 category_variable = var
#                 break

#         # Get domain object
#         domain_obj = domain.objects.filter(slug_id=domain_slug_id).first()
#         if not domain_obj:
#             return JsonResponse({"error": "Domain not found", "success": False}, status=404)

#         # Build variables dict
#         variables_dict = {}
#         for var in variable_qs:
#             # If this is the category variable, replace with real wp_category data
#             if category_variable and var.id == category_variable.id:
#                 categories = list(
#                     wp_category.objects.filter(domain_id=domain_obj).values('wp_cat_id', 'name', 'slug', 'description')
#                 )

#                 try:
#                     # Try parsing example_value as a JSON template
#                     example_template = json.loads(var.example_value)

#                     # Example template is a list of dicts
#                     if isinstance(example_template, list) and isinstance(example_template[0], dict):
#                         reformatted = []
#                         for cat in categories:
#                             item = {}
#                             for key in example_template[0].keys():
#                                 item[key] = cat.get(key, "")
#                             reformatted.append(item)
#                         variables_dict[var.name] = json.dumps(reformatted)

#                     # Example template is a single dict
#                     elif isinstance(example_template, dict):
#                         # Use the first category and map to template keys
#                         item = {}
#                         first_cat = categories[0] if categories else {}
#                         for key in example_template.keys():
#                             item[key] = first_cat.get(key, "")
#                         variables_dict[var.name] = json.dumps(item)

#                     else:
#                         variables_dict[var.name] = json.dumps(categories)

#                 except json.JSONDecodeError:
#                     # fallback if example_value isn't JSON
#                     variables_dict[var.name] = str(var.example_value)


#             else:
#                 # Use example value, parsed if JSON
#                 try:
#                     parsed = json.loads(var.example_value)
#                     variables_dict[var.name] = json.dumps(parsed) if isinstance(parsed, (dict, list)) else str(parsed)
#                 except json.JSONDecodeError:
#                     variables_dict[var.name] = str(var.example_value)

#         # Recursively replace placeholders
#         def replace_variables_recursive(obj):
#             if isinstance(obj, dict):
#                 return {k: replace_variables_recursive(v) for k, v in obj.items()}
#             elif isinstance(obj, list):
#                 return [replace_variables_recursive(item) for item in obj]
#             elif isinstance(obj, str):
#                 for var_name, var_val in variables_dict.items():
#                     placeholder = f"[[{var_name}]]"
#                     if placeholder in obj:
#                         obj = obj.replace(placeholder, var_val)
#                 return obj
#             return obj

#         updated_prompt_data = replace_variables_recursive(prompt_data)

#         return JsonResponse({
#             "updated_prompt_data": updated_prompt_data,
#             "success": True
#         }, status=200)

#     except Exception as e:
#         print("Error in replace_output_variable_for_article_type:", e)
#         return JsonResponse({"error": "Internal Server Error", "success": False}, status=500)
















# @api_view(['GET'])
# def replace_output_variable_for_article_type(request):
#     try:
#         prompt_slug_id = request.GET.get('prompt_slug_id')
#         domain_slug_id = request.GET.get('domain_slug_id')

#         prompt_obj = prompt.objects.filter(slug_id=prompt_slug_id).first()
#         if not prompt_obj:
#             return JsonResponse({"error": "Prompt not found", "success": False}, status=404)

#         article_type_obj = prompt_obj.article_type_id
#         if not article_type_obj:
#             return JsonResponse({"error": "Article type not found", "success": False}, status=404)

#         prompt_data = prompt_obj.prompt_data or {}

#         variable_qs = variables.objects.filter(article_type_id=article_type_obj.id, use_exact_value=True)
#         if not variable_qs.exists():
#             return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

#         domain_obj = domain.objects.filter(slug_id=domain_slug_id).first()
#         if not domain_obj:
#             return JsonResponse({"error": "Domain not found", "success": False}, status=404)

#         # Identify category and tag type variables
#         category_keywords = ['category', 'categories']
#         tag_keywords = ['tag', 'tags']
#         category_variable = None
#         tag_variable = None

#         for var in variable_qs:
#             var_name_lower = var.name.lower()
#             if not category_variable and any(keyword in var_name_lower for keyword in category_keywords):
#                 category_variable = var
#             if not tag_variable and any(keyword in var_name_lower for keyword in tag_keywords):
#                 tag_variable = var

#         variables_dict = {}

#         for var in variable_qs:
#             # Handle category variable
#             if category_variable and var.id == category_variable.id:
#                 categories = list(
#                     wp_category.objects.filter(domain_id=domain_obj).values('wp_cat_id', 'name', 'slug', 'description')
#                 )
#                 example_value = var.example_value
#                 try:
#                     example_template = json.loads(example_value)
#                     if isinstance(example_template, list) and isinstance(example_template[0], dict):
#                         reformatted = []
#                         for cat in categories:
#                             item = {}
#                             for key in example_template[0].keys():
#                                 item[key] = cat.get(key, "")
#                             reformatted.append(item)
#                         variables_dict[var.name] = json.dumps(reformatted)
#                     elif isinstance(example_template, dict):
#                         item = {}
#                         first_cat = categories[0] if categories else {}
#                         for key in example_template.keys():
#                             item[key] = first_cat.get(key, "")
#                         variables_dict[var.name] = json.dumps(item)
#                     else:
#                         variables_dict[var.name] = json.dumps(categories)
#                 except json.JSONDecodeError:
#                     variables_dict[var.name] = str(example_value)

#             # Handle tag variable
#             elif tag_variable and var.id == tag_variable.id:
#                 tags = list(
#                     wp_tag.objects.filter(domain_id=domain_obj).values('wp_tag_id', 'name', 'slug', 'description')
#                 )
#                 example_value = var.example_value
#                 try:
#                     example_template = json.loads(example_value)
#                     if isinstance(example_template, list) and isinstance(example_template[0], dict):
#                         reformatted = []
#                         for tag in tags:
#                             item = {}
#                             for key in example_template[0].keys():
#                                 item[key] = tag.get(key, "")
#                             reformatted.append(item)
#                         variables_dict[var.name] = json.dumps(reformatted)
#                     elif isinstance(example_template, dict):
#                         item = {}
#                         first_tag = tags[0] if tags else {}
#                         for key in example_template.keys():
#                             item[key] = first_tag.get(key, "")
#                         variables_dict[var.name] = json.dumps(item)
#                     else:
#                         variables_dict[var.name] = json.dumps(tags)
#                 except json.JSONDecodeError:
#                     variables_dict[var.name] = str(example_value)

#             # Other variables
#             else:
#                 try:
#                     parsed = json.loads(var.example_value)
#                     variables_dict[var.name] = json.dumps(parsed) if isinstance(parsed, (dict, list)) else str(parsed)
#                 except json.JSONDecodeError:
#                     variables_dict[var.name] = str(var.example_value)

#         def replace_variables_recursive(obj):
#             if isinstance(obj, dict):
#                 return {k: replace_variables_recursive(v) for k, v in obj.items()}
#             elif isinstance(obj, list):
#                 return [replace_variables_recursive(item) for item in obj]
#             elif isinstance(obj, str):
#                 for var_name, var_val in variables_dict.items():
#                     placeholder = f"[[{var_name}]]"
#                     if placeholder in obj:
#                         obj = obj.replace(placeholder, var_val)
#                 return obj
#             return obj

#         updated_prompt_data = replace_variables_recursive(prompt_data)

#         return JsonResponse({
#             "updated_prompt_data": updated_prompt_data,
#             "success": True
#         }, status=200)

#     except Exception as e:
#         print("Error in replace_output_variable_for_article_type:", e)
#         return JsonResponse({"error": "Internal Server Error", "success": False}, status=500)







@api_view(['GET'])
def replace_output_variable_for_article_type(request):
    try:
        prompt_slug_id = request.GET.get('prompt_slug_id')
        domain_slug_id = request.GET.get('domain_slug_id')

        prompt_obj = prompt.objects.filter(slug_id=prompt_slug_id).first()
        if not prompt_obj:
            return JsonResponse({"error": "Prompt not found", "success": False}, status=404)

        article_type_obj = prompt_obj.article_type_id
        if not article_type_obj:
            return JsonResponse({"error": "Article type not found", "success": False}, status=404)

        prompt_data = prompt_obj.prompt_data or {}

        variable_qs = variables.objects.filter(article_type_id=article_type_obj.id, use_exact_value=True)
        if not variable_qs.exists():
            return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

        domain_obj = domain.objects.filter(slug_id=domain_slug_id).first()
        if not domain_obj:
            return JsonResponse({"error": "Domain not found", "success": False}, status=404)

        # Identify variable types
        category_keywords = ['category', 'categories']
        tag_keywords = ['tag', 'tags']
        author_keywords = ['author', 'authors']
        category_variable = tag_variable = author_variable = None

        for var in variable_qs:
            var_name_lower = var.name.lower()
            if not category_variable and any(k in var_name_lower for k in category_keywords):
                category_variable = var
            if not tag_variable and any(k in var_name_lower for k in tag_keywords):
                tag_variable = var
            if not author_variable and any(k in var_name_lower for k in author_keywords):
                author_variable = var

        variables_dict = {}

        for var in variable_qs:
            example_value = var.example_value

            # Category variable
            if category_variable and var.id == category_variable.id:
                categories = list(
                    wp_category.objects.filter(domain_id=domain_obj).values('wp_cat_id', 'name', 'slug', 'description')
                )
                try:
                    template = json.loads(example_value)
                    if isinstance(template, list) and isinstance(template[0], dict):
                        reformatted = [{k: cat.get(k, "") for k in template[0].keys()} for cat in categories]
                        variables_dict[var.name] = json.dumps(reformatted)
                    elif isinstance(template, dict):
                        first_cat = categories[0] if categories else {}
                        variables_dict[var.name] = json.dumps({k: first_cat.get(k, "") for k in template.keys()})
                    else:
                        variables_dict[var.name] = json.dumps(categories)
                except json.JSONDecodeError:
                    variables_dict[var.name] = str(example_value)

            # Tag variable
            elif tag_variable and var.id == tag_variable.id:
                tags = list(
                    wp_tag.objects.filter(domain_id=domain_obj).values('wp_tag_id', 'name', 'slug', 'description')
                )
                try:
                    template = json.loads(example_value)
                    if isinstance(template, list) and isinstance(template[0], dict):
                        reformatted = [{k: tag.get(k, "") for k in template[0].keys()} for tag in tags]
                        variables_dict[var.name] = json.dumps(reformatted)
                    elif isinstance(template, dict):
                        first_tag = tags[0] if tags else {}
                        variables_dict[var.name] = json.dumps({k: first_tag.get(k, "") for k in template.keys()})
                    else:
                        variables_dict[var.name] = json.dumps(tags)
                except json.JSONDecodeError:
                    variables_dict[var.name] = str(example_value)

            # Author variable
            elif author_variable and var.id == author_variable.id:
                authors = list(
                    wp_author.objects.filter(domain_id=domain_obj).values(
                        'wp_author_id', 'username', 'first_name', 'last_name', 'email', 'bio', 'profile_image'
                    )
                )
                try:
                    template = json.loads(example_value)

                    # Return full list of authors with reformatted fields
                    if isinstance(template, list) and isinstance(template[0], dict):
                        reformatted = [
                            {k: author.get(k, "") for k in template[0].keys()} for author in authors
                        ]
                        variables_dict[var.name] = json.dumps(reformatted)

                    # Even if it's a dict, return full list using dict keys
                    elif isinstance(template, dict):
                        reformatted = [
                            {k: author.get(k, "") for k in template.keys()} for author in authors
                        ]
                        variables_dict[var.name] = json.dumps(reformatted)

                    else:
                        variables_dict[var.name] = json.dumps(authors)

                except json.JSONDecodeError:
                    variables_dict[var.name] = json.dumps(authors)

            # Regular variables
            else:
                try:
                    parsed = json.loads(example_value)
                    variables_dict[var.name] = json.dumps(parsed) if isinstance(parsed, (dict, list)) else str(parsed)
                except json.JSONDecodeError:
                    variables_dict[var.name] = str(example_value)

        def replace_variables_recursive(obj):
            if isinstance(obj, dict):
                return {k: replace_variables_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_variables_recursive(item) for item in obj]
            elif isinstance(obj, str):
                for var_name, var_val in variables_dict.items():
                    placeholder = f"[[{var_name}]]"
                    if placeholder in obj:
                        obj = obj.replace(placeholder, var_val)
                return obj
            return obj

        updated_prompt_data = replace_variables_recursive(prompt_data)

        return JsonResponse({
            "updated_prompt_data": updated_prompt_data,
            "success": True
        }, status=200)

    except Exception as e:
        print("Error in replace_output_variable_for_article_type:", e)
        return JsonResponse({"error": "Internal Server Error", "success": False}, status=500)
