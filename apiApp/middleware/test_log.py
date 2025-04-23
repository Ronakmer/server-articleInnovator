import uuid
import logging
import traceback
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.http import JsonResponse
from your_app.models import activity_log  # Update with your app name

logger = logging.getLogger(__name__)

class ActivityLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Logs every incoming request"""
        request.start_time = now()

    def process_response(self, request, response):
        """Logs details after response is sent"""
        try:
            # Get user details if logged in
            user = request.user if request.user.is_authenticated else None

            # Log the request details
            activity_log.objects.create(
                user_id=user,
                workspace_id=getattr(user, 'workspace_id', None),
                domain_id=request.session.get('domain_id', None),
                level="INFO",
                message=f"User accessed {request.path}",
                url=request.path,
                module=request.resolver_match.app_name if request.resolver_match else "Unknown",
                module_name=request.resolver_match.url_name if request.resolver_match else "Unknown",
                function=request.resolver_match.func.__name__ if request.resolver_match else "Unknown",
                status_code=response.status_code,
                user_role=getattr(user, 'role', '') if user else '',
                line=0,
                user_status=user.is_active if user else False,
                created_date=now(),
            )
        except Exception as e:
            logger.error(f"Logging failed: {e}")
        
        return response

    def process_exception(self, request, exception):
        """Logs any exceptions that occur in views"""
        try:
            user = request.user if request.user.is_authenticated else None

            activity_log.objects.create(
                user_id=user,
                workspace_id=getattr(user, 'workspace_id', None),
                domain_id=request.session.get('domain_id', None),
                level="ERROR",
                message=f"Error occurred: {str(exception)}",
                url=request.path,
                module=request.resolver_match.app_name if request.resolver_match else "Unknown",
                module_name=request.resolver_match.url_name if request.resolver_match else "Unknown",
                function=request.resolver_match.func.__name__ if request.resolver_match else "Unknown",
                status_code=500,
                user_role=getattr(user, 'role', '') if user else '',
                line=traceback.extract_tb(exception.__traceback__)[-1][1] if exception.__traceback__ else 0,
                user_status=user.is_active if user else False,
                created_date=now(),
            )
        except Exception as e:
            logger.error(f"Exception logging failed: {e}")

        return JsonResponse({"error": "Something went wrong"}, status=500)
