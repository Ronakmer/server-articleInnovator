
import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view


# @api_view(['POST'])
# def verify_ai_configuration(request):
#     try:
#         api_key = request.data.get("api_key")
#         api_provider = request.data.get("api_provider")
#         api_model = request.data.get("api_model")
#         api_version= request.data.get("api_version")
#         api_url = request.data.get("api_url")

#         success = False
#         if api_provider == "Claude":
#             headers = {
#                 'x-api-key': api_key, # dynamic
#                 # 'anthropic-version': '2023-06-01', # dynamic
#                 'anthropic-version': api_version, # dynamic
#                 'content-type': 'application/json',
#             }

#             json_data = {
#                 # 'model': 'claude-3-opus-20240229', # dynamic
#                 'model': api_model, # dynamic
#                 'max_tokens': 1024, 
#                 'messages': [
#                     {
#                         'role': 'user',
#                         'content': 'How many moons does Jupiter have?',
#                     },
#                 ],
#             }
#             response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=json_data)
#             print(response.json())
#             if response.status_code == 200:
#                 success = True

#         if api_provider == "OpenAI":
#             url = "https://api.openai.com/v1/models"  # Replace with OpenAI's endpoint
#             headers = {"Authorization": f"Bearer {api_key}"}
#             response = requests.get(url, headers=headers)
#             print(response.json(),'//')
#             if response.status_code == 200:
#                 success = True
                
#         if api_provider == "Azure":
            
#             url = f"{api_url}/openai/deployments/{api_model}/chat/completions?api-version={api_version}"
#             headers = {
#                 "api-key": api_key,
#                 "Content-Type": "application/json"
#             }
#             data = {
#                 "messages": [{"role": "user", "content": "Hello, can you verify my Azure OpenAI API key?"}],
#                 "max_tokens": 10
#             }

#             try:
#                 response = requests.post(url, headers=headers, json=data)
#                 if response.status_code == 200:
#                     print("Azure OpenAI API key is working.")
#                     print("Response:", response.json())
#                     success = True
#                 else:
#                     print(f"Azure OpenAI API key failed: {response.status_code}")
#                     print(f"Response: {response.text}")
#                     success = False
#             except Exception as e:
#                 print(f"An error occurred while testing Azure OpenAI API: {e}")
#                 success = False

#         # return JsonResponse({'success': success})
#         return JsonResponse({
#             "message": success,
#         }, status=200)

    
#     except Exception as e:
#         print("This error is verify_ai_configuration --->: ",e)
#         return JsonResponse({"error": "Internal Server error.","success": False}, status=500)












from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
import logging

logger = logging.getLogger(__name__)

def validate_input_parameters(api_key, api_provider, api_models):
    """
    Validate input parameters for API configuration verification.
    
    Args:
        api_key (str): API authentication key
        api_provider (str): API provider name
        api_models (str or list): Models to verify
    
    Returns:
        tuple: (validated_models, error_response)
    """
    if not api_key or not api_provider:
        return None, JsonResponse({
            "success": False, 
            "error": "Missing API key or provider"
        }, status=400)

    # Convert models to list if string
    if isinstance(api_models, str):
        api_models = [model.strip() for model in api_models.split(",")]

    # Validate models
    if not api_models:
        return None, JsonResponse({
            "success": False, 
            "error": "No models specified"
        }, status=400)

    return api_models, None


def verify_claude_api(api_key, api_models, api_version=None):
    """
    Verify Claude API configuration.
    
    Args:
        api_key (str): Claude API key
        api_models (list): List of models to verify
        api_version (str, optional): API version
    
    Returns:
        dict: Verification results
    """
    headers = {
        'x-api-key': api_key,
        'anthropic-version': api_version or '2023-06-01',
        'content-type': 'application/json',
    }

    success = False
    failed_models = []

    for model in api_models:
        try:
            json_data = {
                'model': model,
                'max_tokens': 1024,
                'messages': [{'role': 'user', 'content': 'How many moons does Jupiter have?'}],
            }
            response = requests.post(
                'https://api.anthropic.com/v1/messages', 
                headers=headers, 
                json=json_data,
                timeout=10
            )
            
            if response.status_code == 200:
                success = True
            else:
                failed_models.append(model)
                logger.warning(f"Claude API verification failed for model {model}")
        except requests.RequestException as e:
            logger.error(f"Claude API request error: {e}")
            failed_models.append(model)

    return {
        # "success": success,
        "success": len(failed_models) == 0,
        "failed_models": failed_models
    }

def verify_openai_api(api_key, api_models):
    """
    Verify OpenAI API configuration.
    
    Args:
        api_key (str): OpenAI API key
        api_models (list): List of models to verify
    
    Returns:
        dict: Verification results
    """
    success = False
    failed_models = []

    for model in api_models:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": [{"role": "user", "content": "Hello, can you verify my OpenAI API key?"}],
                "max_tokens": 10
            }

            response = requests.post(
                url, 
                headers=headers, 
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                success = True
            else:
                failed_models.append(model)
                logger.warning(f"OpenAI API verification failed for model {model}")
        except requests.RequestException as e:
            logger.error(f"OpenAI API request error: {e}")
            failed_models.append(model)

    return {
        # "success": success,
        "success": len(failed_models) == 0,
        "failed_models": failed_models
    }


def verify_azure_api(api_key, api_models, api_url, api_version):
    """
    Verify Azure OpenAI API configuration.
    
    Args:
        api_key (str): Azure API key
        api_models (list): List of models to verify
        api_url (str): Azure API base URL
        api_version (str): API version
    
    Returns:
        dict: Verification results
    """
    success = False
    failed_models = []

    for model in api_models:
        try:
            url = f"{api_url}/openai/deployments/{model}/chat/completions?api-version={api_version}"
            headers = {
                "api-key": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "messages": [{"role": "user", "content": "Hello, can you verify my Azure OpenAI API key?"}],
                "max_tokens": 10
            }

            response = requests.post(
                url, 
                headers=headers, 
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                success = True
            else:
                failed_models.append(model)
                logger.warning(f"Azure API verification failed for model {model}")
        except requests.RequestException as e:
            logger.error(f"Azure API request error: {e}")
            failed_models.append(model)

    return {
        # "success": success,
        "success": len(failed_models) == 0,
        "failed_models": failed_models
    }



# def verify_novita_api(api_key, api_models, api_url, api_version=None):
#     """
#     Verify Novita API configuration.
    
#     Args:
#         api_key (str): Novita API key
#         api_models (list): List of models to verify
#         api_url (str): Novita API base URL
#         api_version (str, optional): API version
    
#     Returns:
#         dict: Verification results
#     """
#     success = False
#     failed_models = []

#     for model in api_models:
#         try:
#             url = f"{api_url}/v1/models/{model}/verify?api-version={api_version or 'v1'}"
#             headers = {
#                 "Authorization": f"Bearer {api_key}",
#                 "Content-Type": "application/json"
#             }
#             data = {
#                 "messages": [{"role": "user", "content": "Verify Novita API key?"}],
#                 "max_tokens": 10
#             }

#             response = requests.post(
#                 url, 
#                 headers=headers, 
#                 json=data,
#                 timeout=10
#             )
            
#             if response.status_code == 200:
#                 success = True
#             else:
#                 failed_models.append(model)
#                 logger.warning(f"Novita API verification failed for model {model}")
#         except requests.RequestException as e:
#             logger.error(f"Novita API request error: {e}")
#             failed_models.append(model)

#     return {
#         "success": len(failed_models) == 0,
#         "failed_models": failed_models
#     }


def verify_novita_api(api_key, api_models, api_url, api_version=None):
    """
    Verify Novita API configuration.
    
    Args:
        api_key (str): Novita API key
        api_models (list or str): List of models or single model string to verify
        api_url (str): Novita API base URL
        api_version (str, optional): API version
    
    Returns:
        dict: Verification results
    """
    import requests
    import logging

    # Set up logger if not already configured
    logger = logging.getLogger(__name__)
    
    success = True
    failed_models = []

    # Convert single model string to list if needed
    if isinstance(api_models, str):
        api_models = [api_models]

    for model in api_models:
        try:
            # Build the URL correctly based on Novita API structure
            # The URL should be the base endpoint, not model-specific
            url = f"{api_url}/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Format the request payload according to Novita API
            data = {
                "model": model,
                "messages": [{"role": "user", "content": "Verify Novita API key"}],
                "max_tokens": 10
            }

            response = requests.post(
                url, 
                headers=headers, 
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Novita API verification successful for model {model}")
            else:
                failed_models.append(model)
                logger.warning(f"Novita API verification failed for model {model}. Status code: {response.status_code}, Response: {response.text}")
                success = False
        except requests.RequestException as e:
            logger.error(f"Novita API request error for model {model}: {e}")
            failed_models.append(model)
            success = False

    return {
        "success": success,
        "failed_models": failed_models
    }



@api_view(['POST'])
def verify_ai_configuration(request):
    try:
        # Extract request parameters
        api_key = request.data.get("api_key")
        api_provider = request.data.get("api_provider")
        api_models = request.data.get("api_model")  # Multiple models as CSV
        api_version = request.data.get("api_version")
        api_url = request.data.get("api_url")

        # Validate input parameters
        validated_models, error_response = validate_input_parameters(api_key, api_provider, api_models)
        if error_response:
            return error_response

        # Provider-specific verification
        if api_provider == "Claude":
            verification_result = verify_claude_api(api_key, validated_models, api_version)
        elif api_provider == "OpenAI":
            verification_result = verify_openai_api(api_key, validated_models)
        elif api_provider == "Azure":
            verification_result = verify_azure_api(api_key, validated_models, api_url, api_version)
        elif api_provider == "Novita":  # New case for Novita
            verification_result = verify_novita_api(api_key, validated_models, api_url, api_version)

        else:
            return JsonResponse({
                "success": False, 
                "error": f"Unsupported API provider: {api_provider}"
            }, status=400)

        # Return verification results
        return JsonResponse(verification_result, status=200)

    except Exception as e:
        logger.error(f"Unexpected error in API verification: {e}")
        return JsonResponse({
            "success": False, 
            "error": "Internal Server error."
        }, status=500)