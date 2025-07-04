from loguru import logger
from apiApp.models import activity_log, workspace, notification, domain
from django.contrib.auth.models import User


base_url = 'https://127.0.0.1:8000/'

class Handler:
    def __init__(self):
        # Set up the Loguru logger to use the custom handler function
        logger.add(self.log_to_database)

    def log_to_database(self, message):
       
        # Loguru provides the log record as an object with attributes, not a dictionary
        print('0000000')
        record = message.record
        print(record,'record')
        
        # Extracting required data
        try:
            workspace_slug_id = record['extra']['extra']['workspace_slug_id']
        except (KeyError, TypeError):
            workspace_slug_id = None  # or some default value
        domain_slug_id = record['extra']['extra']['domain_slug_id']
        url = record['extra']['extra']['url']
        function = record['function']
        level = record['level'].name
        line = record['line']
        message = record['message']
        module = record['module']
        name = record['name']
        time = record['time']
        status_code = record['extra']['extra']['status_code']
        request_user = record['extra']['extra']['request_user']
        user_status = record['extra']['extra']['user_status']
        
        workspace_obj = None
        if workspace_slug_id:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        
        user_role = "superadmin" if request_user.is_superuser else "admin"

        if domain_slug_id:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            
            if domain_obj.manager_id.filter(user_id=request_user).exists():
                user_role = "manager"
            elif domain_obj.writer_id.filter(user_id=request_user).exists():
                user_role = "writer"
        
        
        activity_log.objects.create(
            workspace_id = workspace_obj,
            domain_id = domain_obj,
            url=f"{base_url}{url}",
            level = level,
            message = message,
            module = module,
            module_name  = name,
            status_code =  status_code,   
            function = function,
            line = line,
            time = time,
            user_id = request_user,
            user_role = user_role,
            user_status = user_status,
        )
        
        
        #  add notification
        if record['extra']['extra']['notify'] == True:
            notification.objects.create(
                workspace_id = workspace_obj,
                domain_id = domain_obj,
                user_id = request_user,
                send_time = time,
                message = message,
            )
            

# Instantiate the handler
db_handler = Handler()




# Record was: {'elapsed': datetime.timedelta(seconds=14, microseconds=738284), 'exception': None, 'extra': {'extra': {'notify': True, 'status_code': 200, 'workspace_slug_id': '77b4ad49-db8a-4434-aad5-c2351c953cc7', 'url': '/api/roles/', 'request_user': <User: superadmin@gmail.com>, 'domain_slug_id': 'ec676a34-eb18-4610-b1b8-99ba7d26d87a', 'user_status': True}}, 'file': (name='role.py', path='C:\\Users\\DELL\\Desktop\\botxbyte\\0-Article Innovator\\articleInnovator\\apiApp\\views\\role\\role.py'), 'function': 'list_role', 'level': (name='INFO', no=20, icon='ℹ️'), 'line': 48, 'message': 'This is aan info log message', 'module': 'role', 'name': 'apiApp.views.role.role', 'process': (id=12024, name='MainProcess'), 'thread': (id=20768, name='Thread-50 (process_request_thread)'), 'time': datetime(2025, 5, 5, 13, 5, 12, 489183, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800), 'India Standard Time'))}
