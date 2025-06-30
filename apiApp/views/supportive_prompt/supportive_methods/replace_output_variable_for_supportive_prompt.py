

from django.http import JsonResponse
from rest_framework.decorators import api_view
from apiApp.models import supportive_prompt, variables
import json



@api_view(['GET'])
def replace_output_variable_for_supportive_prompt(request):
    try:
        slug_id = request.GET.get('slug_id')
        if not slug_id:
            return JsonResponse({"error": "Missing slug_id", "success": False}, status=400)

        # Fetch the prompt object
        supportive_prompt_obj = supportive_prompt.objects.filter(slug_id=slug_id).first()
        if not supportive_prompt_obj:
            return JsonResponse({"error": "Supportive prompt not found", "success": False}, status=404)

        # Get the base text from prompt
        text = supportive_prompt_obj.supportive_prompt_data
        supportive_prompt_type_id = supportive_prompt_obj.supportive_prompt_type_id
        print(text)
       
        # # Fetch the variables object
        # variables_obj = variables.objects.filter(supportive_prompt_type_id=supportive_prompt_type_id).first()
        # if not variables_obj:
        #     return JsonResponse({"error": "variables not found", "success": False}, status=404)
     
        # print(variables_obj)
        
        
        # # Fetch all variable objects for this prompt type
        # variable_qs = variables.objects.filter(supportive_prompt_type_id=supportive_prompt_type_id)
        # print(variable_qs,'variable_qssdfsdfsadfsdf')
        
        # # Extract only the 'output' variable
        # output_var = variable_qs.filter(use_exact_value=True).first()
        # # output_var = variable_qs.filter(name="output").first()
        # print(output_var,'output_varsdfsdfwewefv')
        
        # if not output_var:
        #     return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

        # # Try to parse the output value as JSON
        # output_name = output_var.name
        # output_value = output_var.example_value
        # try:
        #     output_dict = json.loads(output_value)
        # except json.JSONDecodeError:
        #     output_dict = output_value  # fallback to raw string if not JSON

        # # Replace [[output]] in the text
        # placeholder = f"[[{output_name}]]"
        # updated_text = text.replace(placeholder, str(output_dict))

        # print(updated_text)
        
        # Fetch all variable objects for this prompt type
        variable_qs = variables.objects.filter(supportive_prompt_type_id=supportive_prompt_type_id)
        print(variable_qs, '--- variable_qs ---')

        # Extract output variable(s) where use_exact_value is True
        output_vars = variable_qs.filter(use_exact_value=True)
        print(output_vars, '--- output_var ---')

        # If there is no output variable, return error
        if not output_vars.exists():
            return JsonResponse({"error": "'output' variable not found", "success": False}, status=404)

        # Replace only the output variable(s) in the text
        for output_var in output_vars:
            var_name = output_var.name  # typically 'output'
            var_value = output_var.example_value

            try:
                parsed_value = json.loads(var_value)
            except json.JSONDecodeError:
                parsed_value = var_value  # fallback to raw string

            placeholder = f"[[{var_name}]]"
            text = text.replace(placeholder, str(parsed_value))

        print(text, '--- updated_text ---')


        return JsonResponse({
            "updated_text": text,
            "success": True
        }, status=200)

    except Exception as e:
        print("Error in replace_output_variable_for_supportive_prompt:", e)
        return JsonResponse({"error": "Internal Server Error", "success": False}, status=500)
