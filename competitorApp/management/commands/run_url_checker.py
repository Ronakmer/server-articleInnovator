from django.core.management.base import BaseCommand
from competitorApp.views.cronjob.main_checker import check_single_url, get_due_urls
from competitorApp.models import competitor_selected_url


class Command(BaseCommand):
    help = 'URL checker for competitor monitoring'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            choices=['status', 'test', 'manual'],
            default='status',
            help='Mode: status, test, or manual'
        )
        parser.add_argument(
            '--url-id',
            type=int,
            help='URL ID to test (for test mode)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Number of URLs to process (for manual mode)'
        )

    def handle(self, *args, **options):
        mode = options['mode']
        
        if mode == 'status':
            self.show_status()
        elif mode == 'test':
            self.test_single_url(options['url_id'])
        elif mode == 'manual':
            self.run_manual_check(options['limit'])

    def show_status(self):
        """Show system status"""
        try:
            from django.utils import timezone
            
            now = timezone.now()
            total_urls = competitor_selected_url.objects.filter(monitor_enabled=True).count()
            due_urls = competitor_selected_url.objects.filter(
                next_api_call_at__lte=now,
                monitor_enabled=True
            ).count()
            
            self.stdout.write(f"Total URLs: {total_urls}")
            self.stdout.write(f"Due for checking: {due_urls}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

    def test_single_url(self, url_id):
        """Test a single URL"""
        if not url_id:
            self.stdout.write(self.style.ERROR("Please provide --url-id=123"))
            return
        
        try:
            url_obj = competitor_selected_url.objects.get(id=url_id)
            
            self.stdout.write(f"Testing URL: {url_obj.selected_url}")
            self.stdout.write(f"Enabled: {url_obj.monitor_enabled}")
            
            if not url_obj.monitor_enabled:
                self.stdout.write(self.style.WARNING("URL monitoring is disabled"))
                return
            
            success, message = check_single_url(url_id)
            
            if success:
                self.stdout.write(self.style.SUCCESS(f"Success: {message}"))
            else:
                self.stdout.write(self.style.WARNING(f"Failed: {message}"))
                
        except competitor_selected_url.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"URL ID {url_id} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

    def run_manual_check(self, limit):
        """Manually run URL checking"""
        try:
            due_urls = get_due_urls(limit=limit)
            
            if not due_urls:
                self.stdout.write("No URLs due for checking")
                return
            
            self.stdout.write(f"Processing {len(due_urls)} URLs...")
            
            success_count = 0
            for i, url_obj in enumerate(due_urls, 1):
                success, message = check_single_url(url_obj.id)
                if success:
                    success_count += 1
                
                if i % 10 == 0:  # Progress every 10 URLs
                    self.stdout.write(f"Processed {i}/{len(due_urls)}")
            
            self.stdout.write(self.style.SUCCESS(
                f"Complete: {success_count}/{len(due_urls)} successful"
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}")) 