# AIMessageService/db_router.py
class AiMessageRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'AIMessageService':
            return 'ai_messages_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'AIMessageService':
            return 'ai_messages_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'AIMessageService':
            return db == 'ai_messages_db'
        return None
