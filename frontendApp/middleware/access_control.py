
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
from django.shortcuts import render,redirect


class AccessControlMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exempted paths that do not require authentication
        exempt_paths = [
            'forgot/', 
            'otp/', 
            'new-password/', 
            'verify-otp/',
            # 'dashboard/'
        ]

        # Normalize the request path
        normalized_path = request.path.lstrip('/')
        print(f"Request path: {request.path}, Normalized path: {normalized_path}")

        # Skip checks for exempt paths
        if any(normalized_path.startswith(path) for path in exempt_paths) or normalized_path == '':
            print(normalized_path,'normalized_pathx')
            print(f"Exempt path accessed: {normalized_path}")
            return self.get_response(request)

        # Skip checks for Django admin files (static/media)
        if normalized_path.startswith(settings.MEDIA_URL.strip('/')) or normalized_path.startswith(settings.STATIC_URL.strip('/')):
            print(f"Static or Media path accessed: {normalized_path}")
            return self.get_response(request)


        # Skip checks for Django admin file
        if normalized_path.startswith('dev-admin/'):
            print(f"Admin or static path accessed: {normalized_path}")
            return self.get_response(request)
        
        # # Skip checks for Django admin file
        # if normalized_path.startswith(''):
        if normalized_path.startswith('api/'):
            print(f"Admin or static path accessed: {normalized_path}")
            return self.get_response(request)


        request_user = request.user

        # Superusers bypass all checks
        if request_user.is_superuser:
            print("Superuser access granted.")
            return self.get_response(request)

        # Resolve the route name
        try:
            resolver_match = resolve(f'/{normalized_path}')
            route_name = resolver_match.url_name
            print(f"Resolved route name: {route_name}")
        except Exception as ex:
            print(f"Error resolving route for path: , Exception: {ex}")
            # return JsonResponse({"error": "Unable to resolve route."}, status=403)
            return render(request, 'frontendApp/base/error.html' , {'error': 403})


        # Check user permissions and workspaces
        try:
            print(request_user,'request_user')
            # Fetch user details
            user_details_obj = user_detail.objects.get(user_id=request_user)
            permission_obj = role_has_permissions.objects.filter(role_id=user_details_obj.role_id)
            permission_list = [perm.permission_id.name for perm in permission_obj]
            # print(f"User permissions: {permission_list}")

            # Verify if the route is in the user's permissions
            if route_name.replace("_page", "") not in permission_list:
                print(f"Access denied - {route_name} not in permissions.")
                # return JsonResponse({"error": "Access denied."}, status=403)
                return render(request, 'frontendApp/base/error.html' , {'error': 403})
            
        except Exception as e:
            print(f"Error in AccessControlMiddleware: {e}")
            # return JsonResponse({"error": "An unexpected error occurred while checking permissions."}, status=403)
            return render(request, 'frontendApp/base/error.html' , {'error': 403})
        

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

