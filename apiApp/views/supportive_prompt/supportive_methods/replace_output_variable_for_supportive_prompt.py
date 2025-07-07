

from django.http import JsonResponse
from rest_framework.decorators import api_view
from apiApp.models import supportive_prompt, variables
import json
from apiApp.models import article_type, variables, prompt, domain, wp_category, wp_author, wp_tag  # Make sure all models are imported



# @api_view(['GET'])
# def replace_output_variable_for_supportive_prompt(request):
#     try:
#         slug_id = request.GET.get('slug_id')
#         if not slug_id:
#             return JsonResponse({"error": "Missing slug_id", "success": False}, status=400)

#         # Fetch the prompt object
#         supportive_prompt_obj = supportive_prompt.objects.filter(slug_id=slug_id).first()
#         if not supportive_prompt_obj:
#             return JsonResponse({"error": "Supportive prompt not found", "success": False}, status=404)

#         # Get the base text from prompt
#         text = supportive_prompt_obj.supportive_prompt_data
#         supportive_prompt_type_id = supportive_prompt_obj.supportive_prompt_type_id
#         print(text)
        
#         # Fetch all variable objects for this prompt type
#         variable_qs = variables.objects.filter(supportive_prompt_type_id=supportive_prompt_type_id)
#         print(variable_qs, '--- variable_qs ---')

#         # Extract output variable(s) where use_exact_value is True
#         output_vars = variable_qs.filter(use_exact_value=True)
#         print(output_vars, '--- output_var ---')

#         # If there is no output variable, return error
#         if not output_vars.exists():
#             return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

#         # Replace only the output variable(s) in the text
#         for output_var in output_vars:
#             var_name = output_var.name  # typically 'output'
#             var_value = output_var.example_value

#             try:
#                 parsed_value = json.loads(var_value)
#             except json.JSONDecodeError:
#                 parsed_value = var_value  # fallback to raw string

#             placeholder = f"[[{var_name}]]"
#             text = text.replace(placeholder, str(parsed_value))

#         print(text, '--- updated_text ---')


#         return JsonResponse({
#             "updated_text": text,
#             "success": True
#         }, status=200)

#     except Exception as e:
#         print("Error in replace_output_variable_for_supportive_prompt:", e)
#         return JsonResponse({"error": "Internal Server Error", "success": False}, status=500)









@api_view(['GET'])
def replace_output_variable_for_supportive_prompt(request):
    try:
        slug_id = request.GET.get('slug_id')
        domain_slug_id = request.GET.get('domain_slug_id')

        # if not slug_id or not domain_slug_id:
        #     return JsonResponse({"error": "Missing slug_id or domain_slug_id", "success": False}, status=400)

        supportive_prompt_obj = supportive_prompt.objects.filter(slug_id=slug_id).first()
        if not supportive_prompt_obj:
            return JsonResponse({"error": "Supportive prompt not found", "success": False}, status=404)

        text = supportive_prompt_obj.supportive_prompt_data
        supportive_prompt_type_id = supportive_prompt_obj.supportive_prompt_type_id

        variable_qs = variables.objects.filter(supportive_prompt_type_id=supportive_prompt_type_id, use_exact_value=True)
        if not variable_qs.exists():
            return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

        if domain_slug_id:
            domain_obj = domain.objects.filter(slug_id=domain_slug_id).first()
            if not domain_obj:
                return JsonResponse({"error": "Domain not found", "success": False}, status=404)

        # Identify special variables
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

        # Build variable replacement dictionary
        variables_dict = {}

        for var in variable_qs:
            example_value = var.example_value

            if category_variable and var.id == category_variable.id:
                categories = list(
                    wp_category.objects.filter(domain_id=domain_obj).values('wp_cat_id', 'name', 'slug', 'description', 'slug_id')
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

            elif tag_variable and var.id == tag_variable.id:
                tags = list(
                    wp_tag.objects.filter(domain_id=domain_obj).values('wp_tag_id', 'name', 'slug', 'description', 'slug_id')
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

            elif author_variable and var.id == author_variable.id:
                authors = list(
                    wp_author.objects.filter(domain_id=domain_obj).values(
                        'wp_author_id', 'username', 'first_name', 'last_name', 'email', 'bio', 'profile_image', 'slug_id'
                    )
                )
                try:
                    template = json.loads(example_value)
                    if isinstance(template, list) and isinstance(template[0], dict):
                        reformatted = [{k: author.get(k, "") for k in template[0].keys()} for author in authors]
                        variables_dict[var.name] = json.dumps(reformatted)
                    elif isinstance(template, dict):
                        reformatted = [{k: author.get(k, "") for k in template.keys()} for author in authors]
                        variables_dict[var.name] = json.dumps(reformatted)
                    else:
                        variables_dict[var.name] = json.dumps(authors)
                except json.JSONDecodeError:
                    variables_dict[var.name] = json.dumps(authors)

            else:
                try:
                    parsed_value = json.loads(example_value)
                    variables_dict[var.name] = json.dumps(parsed_value) if isinstance(parsed_value, (dict, list)) else str(parsed_value)
                except json.JSONDecodeError:
                    variables_dict[var.name] = str(example_value)

        # Replace placeholders
        for var_name, var_val in variables_dict.items():
            placeholder = f"[[{var_name}]]"
            if placeholder in text:
                text = text.replace(placeholder, var_val)

        return JsonResponse({
            "updated_text": text,
            "success": True
        }, status=200)

    except Exception as e:
        print("Error in replace_output_variable_for_supportive_prompt:", e)
        return JsonResponse({"error": "Internal Server Error", "success": False}, status=500)
