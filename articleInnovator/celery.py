import os
from celery import Celery
import django
from django.conf import settings

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'articleInnovator.settings')

# Setup Django before creating Celery app
django.setup()

# Create Celery app
app = Celery('articleInnovator')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')

# Import and apply celery configuration from competitorApp
try:
    from competitorApp.views.cronjob.celery_config import (
        CELERY_BEAT_SCHEDULE, CELERY_TASK_ROUTES, CELERY_TASK_DEFAULT_QUEUE,
        CELERY_TASK_SERIALIZER, CELERY_RESULT_SERIALIZER, CELERY_ACCEPT_CONTENT,
        CELERY_RESULT_BACKEND, CELERY_TASK_RESULT_EXPIRES, CELERY_TASK_ANNOTATIONS
    )
    
    # Update Celery configuration
    app.conf.update(
        CELERY_BEAT_SCHEDULE=CELERY_BEAT_SCHEDULE,
        CELERY_TASK_ROUTES=CELERY_TASK_ROUTES,
        CELERY_TASK_DEFAULT_QUEUE=CELERY_TASK_DEFAULT_QUEUE,
        CELERY_TASK_SERIALIZER=CELERY_TASK_SERIALIZER,
        CELERY_RESULT_SERIALIZER=CELERY_RESULT_SERIALIZER,
        CELERY_ACCEPT_CONTENT=CELERY_ACCEPT_CONTENT,
        CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND,
        CELERY_TASK_RESULT_EXPIRES=CELERY_TASK_RESULT_EXPIRES,
        CELERY_TASK_ANNOTATIONS=CELERY_TASK_ANNOTATIONS,
        
        # Connection reliability settings
        broker_connection_retry_on_startup=True,
        broker_connection_retry=True,
        broker_connection_max_retries=10,
        broker_pool_limit=10,
        broker_connection_timeout=30,
        broker_heartbeat=30,
        task_reject_on_worker_lost=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
    )
    print(" Successfully loaded Celery configuration")
except ImportError:
    # Fallback configuration if import fails
    print("Warning: Could not import celery_config, using default settings")

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Add explicit task modules to ensure discovery
app.autodiscover_tasks(['competitorApp'], related_name='views.cronjob.tasks') 