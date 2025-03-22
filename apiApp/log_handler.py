
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
        workspace_slug_id = record['extra']['extra']['workspace_slug_id']
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

