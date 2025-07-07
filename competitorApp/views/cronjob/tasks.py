from celery import shared_task
from django.utils import timezone
# from loguru import logger  # Removing to fix logging issues
from .main_checker import get_due_urls, check_single_url
import time

# Simple test task to verify task discovery
@shared_task
def test_task():
    """Simple test task to verify Celery is working"""
    return {"status": "success", "message": "Test task executed successfully!", "timestamp": timezone.now().isoformat()}

@shared_task
def debug_urls_task():
    """Debug task to check URL status in database"""
    try:
        from competitorApp.models import competitor_selected_url
        from django.utils import timezone
        
        now = timezone.now()
        log_info(f" DEBUG: Current time: {now}")
        
        # Check total URLs
        total_urls = competitor_selected_url.objects.all().count()
        log_info(f" DEBUG: Total URLs in database: {total_urls}")
        
        # Check enabled URLs
        enabled_urls = competitor_selected_url.objects.filter(monitor_enabled=True).count()
        log_info(f" DEBUG: URLs with monitor_enabled=True: {enabled_urls}")
        
        # Check URLs due for processing
        due_urls = competitor_selected_url.objects.filter(
            next_api_call_at__lte=now,
            monitor_enabled=True
        ).count()
        log_info(f" DEBUG: URLs due for processing: {due_urls}")
        
        # Show first 5 URLs that should be due
        sample_urls = competitor_selected_url.objects.filter(
            monitor_enabled=True
        ).order_by('next_api_call_at')[:5]
        
        for url in sample_urls:
            log_info(f" DEBUG: URL {url.id} - next_call: {url.next_api_call_at}, enabled: {url.monitor_enabled}, url: {url.selected_url}")
        
        return {
            'status': 'success',
            'current_time': now.isoformat(),
            'total_urls': total_urls,
            'enabled_urls': enabled_urls,
            'due_urls': due_urls,
            'timestamp': now.isoformat()
        }
        
    except Exception as e:
        log_error(f" DEBUG ERROR: {e}")
        return {'status': 'error', 'message': str(e)}

# Simple logging function
def log_info(message):
    print(f"[CELERY INFO] {timezone.now()}: {message}")

def log_error(message):
    print(f"[CELERY ERROR] {timezone.now()}: {message}")

@shared_task
def url_checker_main_task():
    """
    Main scheduler task - Distributes up to 50,000 URLs to parallel workers
    This task runs every minute and queues individual URL tasks for parallel processing
    """
    try:
        log_info(" Starting URL checker main task - PARALLEL MODE (50,000 URLs)")
        log_info(f" Current time: {timezone.now()}")
        start_time = timezone.now()
        
        # Debug: Check if we can import and call the function
        try:
            from .main_checker import get_due_urls
            log_info(" Successfully imported get_due_urls")
        except Exception as import_error:
            log_error(f" Import error: {import_error}")
            return {'status': 'error', 'message': f'Import error: {import_error}'}
        
        # Get URLs that need checking (up to 50,000)
        log_info(" Calling get_due_urls...")
        due_urls = get_due_urls(limit=50000)
        log_info(f" get_due_urls returned: {len(due_urls) if due_urls else 0} URLs")
        
        if not due_urls:
            log_info(" No URLs due for checking")
            return {'status': 'success', 'message': 'No URLs due', 'urls_processed': 0}
        
        log_info(f" Found {len(due_urls)} URLs - Starting PARALLEL processing")
        
        # Queue each URL as a separate task for parallel processing
        total_urls = len(due_urls)
        tasks_queued = 0
        
        for url_obj in due_urls:
            # Queue individual URL processing task
            process_single_url_task.delay(url_obj.id)
            tasks_queued += 1
            
            # Log progress every 1000 URLs
            if tasks_queued % 1000 == 0:
                log_info(f" Queued {tasks_queued}/{total_urls} tasks...")
        
        end_time = timezone.now()
        queuing_time = (end_time - start_time).total_seconds()
        
        result = {
            'status': 'success',
            'message': f'Queued {total_urls} URLs for PARALLEL processing',
            'urls_queued': total_urls,
            'tasks_queued': tasks_queued,
            'queuing_time_seconds': round(queuing_time, 2),
            'estimated_completion_minutes': round(total_urls / 1000, 1),  # Estimate based on 1000 URLs/min per worker
            'timestamp': timezone.now().isoformat()
        }
        
        log_info(f" Parallel queuing complete: {tasks_queued} tasks queued in {queuing_time:.2f}s")
        log_info(f" Estimated completion time: {result['estimated_completion_minutes']} minutes")
        return result
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'message': str(e),
            'timestamp': timezone.now().isoformat()
        }
        log_error(f" Main task failed: {error_result}")
        return error_result


@shared_task(bind=True, max_retries=3)
def process_single_url_task(self, url_id):
    """
    Process a single URL - This runs in parallel for maximum throughput
    Each URL gets its own worker task for true parallel processing
    """
    try:
        success, message = check_single_url(url_id)
        
        result = {
            'url_id': url_id,
            'status': 'success' if success else 'failed',
            'message': message,
            'worker_id': self.request.id,
            'timestamp': timezone.now().isoformat()
        }
        
        # Only log failures to reduce noise
        if not success:
            log_error(f" URL {url_id} failed: {message}")
        
        return result
        
    except Exception as e:
        # Retry failed URLs up to 3 times
        if self.request.retries < self.max_retries:
            log_info(f" Retrying URL {url_id}, attempt {self.request.retries + 1}")
            raise self.retry(countdown=60)  # Wait 1 minute before retry
        
        error_result = {
            'url_id': url_id,
            'status': 'error',
            'message': str(e),
            'worker_id': self.request.id,
            'timestamp': timezone.now().isoformat()
        }
        log_error(f" URL {url_id} failed permanently: {e}")
        return error_result


@shared_task
def get_processing_stats():
    """
    Get real-time processing statistics
    """
    try:
        from celery import current_app
        
        # Get active tasks
        inspect = current_app.control.inspect()
        active_tasks = inspect.active()
        
        if active_tasks:
            total_active = sum(len(tasks) for tasks in active_tasks.values())
        else:
            total_active = 0
        
        # Get queue stats
        from competitorApp.models import competitor_selected_url
        now = timezone.now()
        
        total_urls = competitor_selected_url.objects.filter(monitor_enabled=True).count()
        due_urls = competitor_selected_url.objects.filter(
            next_api_call_at__lte=now,
            monitor_enabled=True
        ).count()
        
        return {
            'total_monitored_urls': total_urls,
            'urls_due_for_checking': due_urls,
            'active_worker_tasks': total_active,
            'workers_available': True if active_tasks else False,
            'timestamp': now.isoformat()
        }
        
    except Exception as e:
        log_error(f" Stats check failed: {e}")
        return {'error': str(e)}


@shared_task
def cleanup_old_stats():
    """
    Daily task to cleanup old statistics
    """
    try:
        from competitorApp.models import competitor_url_daily_stats
        from datetime import timedelta
        
        # Delete stats older than 30 days
        cutoff_date = timezone.now().date() - timedelta(days=30)
        deleted_count = competitor_url_daily_stats.objects.filter(
            stat_date__lt=cutoff_date
        ).delete()[0]
        
        log_info(f" Cleaned up {deleted_count} old stats records")
        return {
            'status': 'success',
            'deleted_count': deleted_count,
            'cutoff_date': cutoff_date.isoformat()
        }
        
    except Exception as e:
        log_error(f" Cleanup failed: {e}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def get_system_status():
    """
    Get current system status - optimized for parallel processing
    """
    try:
        from competitorApp.models import competitor_selected_url
        
        now = timezone.now()
        
        total_urls = competitor_selected_url.objects.filter(monitor_enabled=True).count()
        due_urls = competitor_selected_url.objects.filter(
            next_api_call_at__lte=now,
            monitor_enabled=True
        ).count()
        
        sitemap_urls = competitor_selected_url.objects.filter(
            competitor_domain_mapping_id__competitor_type='sitemap',
            monitor_enabled=True
        ).count()
        
        category_urls = competitor_selected_url.objects.filter(
            competitor_domain_mapping_id__competitor_type='category',
            monitor_enabled=True
        ).count()
        
        return {
            'total_monitored_urls': total_urls,
            'due_for_checking': due_urls,
            'sitemap_urls': sitemap_urls,
            'category_urls': category_urls,
            'processing_mode': 'PARALLEL',
            'max_urls_per_minute': 50000,
            'timestamp': now.isoformat()
        }
        
    except Exception as e:
        log_error(f" Status check failed: {e}")
        return {'error': str(e)} 