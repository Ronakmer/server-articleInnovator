from celery.schedules import crontab

# ============== CELERY CONFIGURATION FOR MASSIVE PARALLEL PROCESSING ==============
# Optimized for processing 50,000 URLs per minute in parallel

# Celery Beat Schedule - Scheduler runs every minute
CELERY_BEAT_SCHEDULE = {
    'parallel-url-checker': {
        'task': 'competitorApp.views.cronjob.tasks.url_checker_main_task',
        'schedule': crontab(minute='*'),  # Every minute - queues up to 50,000 URL tasks
    },
    'cleanup-daily': {
        'task': 'competitorApp.views.cronjob.tasks.cleanup_old_stats',
        'schedule': crontab(hour=2, minute=0),  # Daily cleanup at 2:00 AM
    },
}

# Task routing for parallel processing
# CELERY_TASK_ROUTES = {
#     # Scheduler task - runs on main queue
#     'competitorApp.views.cronjob.tasks.url_checker_main_task': {'queue': 'scheduler_queue'},
#     
#     # Individual URL processing tasks - distributed across worker queues
#     'competitorApp.views.cronjob.tasks.process_single_url_task': {'queue': 'url_worker_queue'},
#     
#     # Monitoring and stats tasks
#     'competitorApp.views.cronjob.tasks.get_processing_stats': {'queue': 'stats_queue'},
#     'competitorApp.views.cronjob.tasks.get_system_status': {'queue': 'stats_queue'},
#     
#     # Cleanup tasks
#     'competitorApp.views.cronjob.tasks.cleanup_old_stats': {'queue': 'cleanup_queue'},
# }

# Simplified routing - use default queue for all tasks
CELERY_TASK_ROUTES = {}

# Queue configuration
CELERY_TASK_DEFAULT_QUEUE = 'default'

# Basic settings optimized for massive parallel processing
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TASK_RESULT_EXPIRES = 1800  # 30 minutes (shorter for high volume)

# HIGH CONCURRENCY SETTINGS FOR 50,000 URLs
CELERY_WORKER_CONCURRENCY = 100  # High concurrency for parallel processing

# Task-specific configurations for maximum throughput
CELERY_TASK_ANNOTATIONS = {
    # Main scheduler task - queues 50,000 URLs quickly
    'competitorApp.views.cronjob.tasks.url_checker_main_task': {
        'rate_limit': '1/m',        # 1 scheduler task per minute
        'time_limit': 300,          # 5 minutes timeout for queuing
        'soft_time_limit': 240,     # 4 minutes soft timeout
        'priority': 9,              # High priority
    },
    
    # Individual URL processing tasks - the workers
    'competitorApp.views.cronjob.tasks.process_single_url_task': {
        'rate_limit': '50000/m',    # Up to 50,000 URL tasks per minute
        'time_limit': 120,          # 2 minutes timeout per URL
        'soft_time_limit': 90,      # 1.5 minutes soft timeout
        'priority': 5,              # Medium priority
        'max_retries': 3,           # Retry failed URLs
        'default_retry_delay': 60,  # 1 minute between retries
    },
    
    # Stats and monitoring tasks
    'competitorApp.views.cronjob.tasks.get_processing_stats': {
        'rate_limit': '10/m',       # 10 stats checks per minute
        'time_limit': 30,           # 30 seconds timeout
        'priority': 3,              # Low priority
    },
    
    'competitorApp.views.cronjob.tasks.get_system_status': {
        'rate_limit': '5/m',        # 5 status checks per minute
        'time_limit': 30,           # 30 seconds timeout
        'priority': 3,              # Low priority
    },
    
    # Cleanup tasks
    'competitorApp.views.cronjob.tasks.cleanup_old_stats': {
        'time_limit': 600,              # 10 minutes timeout
        'priority': 1,                  # Lowest priority
    },
}

# Performance optimization settings
CELERY_TASK_ACKS_LATE = True                        # Acknowledge tasks only after completion
CELERY_WORKER_PREFETCH_MULTIPLIER = 10              # Higher prefetch for better throughput
CELERY_TASK_REJECT_ON_WORKER_LOST = True            # Reject tasks if worker dies
CELERY_WORKER_DISABLE_RATE_LIMITS = False           # Keep rate limits for safety

# Memory and connection optimization
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000            # Restart worker after 1000 tasks (prevent memory leaks)
CELERY_BROKER_POOL_LIMIT = 100                      # Increase broker connection pool
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True    # Retry broker connections on startup

# Task routing optimization
CELERY_TASK_ROUTES_CACHE = True                     # Cache task routes for performance

# Result backend optimization
CELERY_RESULT_BACKEND_MAX_RETRIES = 3               # Retry result backend operations
CELERY_RESULT_CACHE_MAX = 10000                     # Cache up to 10,000 results

print(" Celery configured for MASSIVE PARALLEL processing:")
print(f"    Max URLs per minute: 50,000")
print(f"    Worker concurrency: {CELERY_WORKER_CONCURRENCY}")
print(f"    Max tasks per worker: {CELERY_WORKER_MAX_TASKS_PER_CHILD}")
print(f"    Prefetch multiplier: {CELERY_WORKER_PREFETCH_MULTIPLIER}") 