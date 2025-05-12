import uuid
import logging
import traceback
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.http import JsonResponse
from apiApp.models import activity_log
from django.utils.encoding import force_str

logger = logging.getLogger(__name__)

class ActivityLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = now()

    def process_response(self, request, response):
        self.log_activity(request, response=response)
        return response

    def process_exception(self, request, exception):
        response = JsonResponse({"error": "Something went wrong"}, status=500)
        self.log_activity(request, exception=exception, response=response)
        return response

    def log_activity(self, request, response=None, exception=None):
        try:
            user = request.user if request.user.is_authenticated else None
            workspace_id = getattr(user, 'workspace_id', None) if user else None
            domain_id = request.session.get('domain_id')

            if exception:
                level = "ERROR"
                message = f"Exception: {str(exception)}"
                status_code = 500
                line = traceback.extract_tb(exception.__traceback__)[-1][1] if exception.__traceback__ else 0
            else:
                status_code = getattr(response, 'status_code', 200)
                if status_code == 401:
                    level = "ERROR"
                elif status_code >= 400:
                    level = "WARNING"
                else:
                    level = "INFO"
                
                try:
                    # Safely decode response content
                    content = force_str(getattr(response, 'content', b''))[:1000]  # Limit length for DB
                except:
                    content = '[Could not decode response content]'

                message = f"User accessed {request.path} - Response: {content}"
                line = 0
            resolver_match = getattr(request, 'resolver_match', None)
                

            activity_log.objects.create(
                user_id=user,
                workspace_id=workspace_id,
                domain_id=domain_id,
                level=level,
                message=message,
                url=request.path,

                module = resolver_match.app_name if resolver_match and hasattr(resolver_match, 'app_name') else "Unknown",
                module_name = resolver_match.url_name if resolver_match and hasattr(resolver_match, 'url_name') else "Unknown",
                function = getattr(resolver_match.func, '__name__', 'Unknown') if resolver_match and hasattr(resolver_match, 'func') else "Unknown",
                status_code=str(status_code),
                user_role=getattr(user, 'role', '') if user else '',
                line=line,
                user_status=user.is_active if user else False,
                created_date=now(),
                slug_id=str(uuid.uuid4())
            )

        except Exception as log_error:
            logger.error(f"Activity logging failed: {log_error}")










# import uuid
# import logging
# import traceback
# from django.utils.deprecation import MiddlewareMixin
# from django.utils.timezone import now
# from django.http import JsonResponse
# from apiApp.models import activity_log

# logger = logging.getLogger(__name__)

# class ActivityLogMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.start_time = now()

#     def process_response(self, request, response):
#         self.log_activity(request, response=response)
#         return response

#     def process_exception(self, request, exception):
#         response = JsonResponse({"error": "Something went wrong"}, status=500)
#         self.log_activity(request, exception=exception, response=response)
#         return response

#     def log_activity(self, request, response=None, exception=None):
#         try:
#             user = request.user if request.user.is_authenticated else None
#             workspace_id = getattr(user, 'workspace_id', None) if user else None
#             domain_id = request.session.get('domain_id')

#             if exception:
#                 level = "ERROR"
#                 message = f"Error occurred: {str(exception)}"
#                 status_code = 500
#                 line = traceback.extract_tb(exception.__traceback__)[-1][1] if exception.__traceback__ else 0
#             else:
#                 status_code = getattr(response, 'status_code', 200)
#                 if status_code == 401:
#                     level = "ERROR"
#                 elif status_code >= 400:
#                     level = "WARNING"
#                 else:
#                     level = "INFO"
#                 message = f"User accessed {request.path}"
#                 line = 0

#             activity_log.objects.create(
#                 user_id=user,
#                 workspace_id=workspace_id,
#                 domain_id=domain_id,
#                 level=level,
#                 message=message,
#                 url=request.path,
#                 module=getattr(request.resolver_match, 'app_name', "Unknown") if request.resolver_match else "Unknown",
#                 module_name=getattr(request.resolver_match, 'url_name', "Unknown") if request.resolver_match else "Unknown",
#                 function=getattr(getattr(request.resolver_match, 'func', None), '__name__', "Unknown") if request.resolver_match else "Unknown",
#                 status_code=status_code,
#                 user_role=getattr(user, 'role', '') if user else '',
#                 line=line,
#                 user_status=user.is_active if user else False,
#                 created_date=now(),
#                 slug_id=str(uuid.uuid4())
#             )

#         except Exception as log_error:
#             logger.error(f"Activity logging failed: {log_error}")






# def process_view(self, request, view_func, view_args, view_kwargs):
#         try:
#             request._view_file = inspect.getfile(view_func)
#             request.view_name = view_func.name_
#         except Exception:
#             request._view_file = 'unknown'
#             request._view_name = 'unknown'
#         return None

#     def process_response(self, request, response):
#         view_file = getattr(request, '_view_file', 'unresolved')
#         view_name = getattr(request, '_view_name', 'unresolved')

#         print(f'[Middleware] View: {view_name}, File: {os.path.basename(view_file)}')
#         print(f'[Middleware] Response status: {response.status_code}')
#         return response