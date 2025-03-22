


from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from apiApp.models import user_detail, role_has_permissions, workspace, user_api_key
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import ExpiredSignatureError, InvalidTokenError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.conf import settings

class AccessControlMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        # Exempted paths that do not require authentication
        exempt_paths = [
            'api/login/', 
            'api/send-otp/', 
            'api/logout/', 
            'api/check-otp/', 
            'api/new-password/',
            'api/get-refresh-token/',
            'api/check-invitation-code/',
            'api/registration/',
            'api/registration-check-otp/',
            # 'api/image-templates/',
        ]

        # Normalize the request path
        normalized_path = request.path.lstrip('/')
        print(f"Request path: {request.path}, Normalized path: {normalized_path}")

        # Skip checks for exempt paths
        if any(normalized_path.startswith(path) for path in exempt_paths):
            print(normalized_path,'normalized_path')
            print(f"Exempt path accessed: {normalized_path}")
            return self.get_response(request)

        # # Skip checks for Django admin files (static/media)
        # if normalized_path.startswith(settings.MEDIA_URL.strip('/')) or normalized_path.startswith(settings.STATIC_URL.strip('/')):
        #     print(f"Static or Media path accessed: {normalized_path}")
        #     return self.get_response(request)


        # Skip checks for Django admin file
        if normalized_path.startswith('dev-admin/'):
            print(f"Admin or static path accessed: {normalized_path}")
            return self.get_response(request)
        
        # # Skip checks for Django admin file
        # if normalized_path.startswith(''):
        if not normalized_path.startswith('api/'):
            print(f"Admin or static path accessed: {normalized_path}")
            return self.get_response(request)

        try:
            # Authentication by API Key - GJ
            if "x-api-key" in request.headers:
                api_key = request.headers.get("x-api-key")
                email = request.headers.get("x-email")
                
                # check api key with email 
                try:
                    request_user_mail_obj = User.objects.get(email=email)  
                except User.DoesNotExist:
                    return JsonResponse({"error": "User mail not found."}, status=404)

                try:
                    user_detail_obj = user_detail.objects.get(user_id = request_user_mail_obj)                
                except user_detail.DoesNotExist:
                    return JsonResponse({"error": "User mail not found."}, status=404)
                
                try:
                    api_obj = user_api_key.objects.filter(api_key = api_key, user_detail_id = user_detail_obj)
                except user_api_key.DoesNotExist:
                    return JsonResponse({"error": "API key not found."}, status=404)
                
                # user, token = self.authenticate_user(request)
                request.user = request_user_mail_obj  # Assign authenticated user to request
                user = request_user_mail_obj
                print(f"Authenticated user: {request.user}")
                
                django_login(request, request_user_mail_obj)
                
            else:
            
                # Authenticate the user using JWT
                user, token = self.authenticate_user(request)
                request.user = user  # Assign authenticated user to request
                print(f"Authenticated user: {request.user}")
                # request.abc = 10
                
            request.is_admin = False
            request.is_user = False
            if not user.is_superuser:
                try:
                    user_obj = user_detail.objects.get(user_id=request.user.id) 
                except user_detail.DoesNotExist:
                    return JsonResponse({
                        "error": "user not found."
                    }, status=404)

                if user_obj.role_id.name == 'admin':
                    request.is_admin = True
                else:
                    request.is_user = True

        except AuthenticationFailed as e:
            print(f"JWT Authentication failed: {e}")
            return JsonResponse({"error": "Authentication failed. Invalid or expired token."}, status=401)
        except ExpiredSignatureError:
            print("JWT Token has expired.")
            return JsonResponse({"error": "Token has expired. Please log in again."}, status=401)
        except InvalidTokenError:
            print("Invalid JWT Token.")
            return JsonResponse({"error": "Invalid token."}, status=401)
        except Exception as e:
            print(f"Unexpected error during JWT Authentication: {e}")
            return JsonResponse({"error": "An unexpected error occurred during authentication."}, status=500)

        # Superusers bypass all checks
        if user.is_superuser:
            print("Superuser access granted.")
            return self.get_response(request)

        # Resolve the route name
        try:
            resolver_match = resolve(f'/{normalized_path}')
            route_name = resolver_match.url_name
            print(f"Resolved route name: {route_name}")
        except Exception as ex:
            print(f"Error resolving route for path: {request.path}, Exception: {ex}")
            return JsonResponse({"error": "Unable to resolve route."}, status=403)

        # Check user permissions and workspaces
        try:
            # Fetch user details
            user_details_obj = user_detail.objects.get(user_id=user)
            permission_obj = role_has_permissions.objects.filter(role_id=user_details_obj.role_id)
            permission_list = [perm.permission_id.name for perm in permission_obj]
            print(f"User permissions: {permission_list}")

            # Verify if the route is in the user's permissions
            if route_name not in permission_list:
                print(f"Access denied - {route_name} not in permissions.")
                return JsonResponse({"error": "Access denied."}, status=403)

        except Exception as e:
            print(f"Error in AccessControlMiddleware: {e}")
            return JsonResponse({"error": "An unexpected error occurred while checking permissions."}, status=403)

        return self.get_response(request)

    def authenticate_user(self, request):
        """
        Authenticate the user using SimpleJWT and return the user and token.
        """
        header = request.headers.get('Authorization', None)
        if header is None or not header.startswith('Bearer '):
            raise AuthenticationFailed("Authorization header is missing or invalid.")

        # Extract the token
        token = header.split(' ')[1]

        # Debugging: log the token
        print(f"Received token: {token}")

        try:
            validated_token = self.jwt_authenticator.get_validated_token(token)
            user = self.jwt_authenticator.get_user(validated_token)
            return user, validated_token
        except ExpiredSignatureError:
            print("Token has expired.")
            raise AuthenticationFailed("Token has expired. Please log in again.")
        except InvalidTokenError:
            print("Invalid JWT Token.")
            raise AuthenticationFailed("Invalid token.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise AuthenticationFailed("Unexpected error during token validation.")

