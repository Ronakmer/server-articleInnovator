# competitorApp/db_router.py

class CompetitorRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'competitorApp':
            return 'competitor_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'competitorApp':
            return 'competitor_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'competitorApp':
            return db == 'competitor_db'
        return None
