from django.apps import AppConfig


class ApiappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apiApp"

    # for log 
    def ready(self):
        from apiApp.log_handler import db_handler  
        # Initialize the handler when the app is ready
        db_handler