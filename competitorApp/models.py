from django.db import models
from django.utils import timezone
import uuid

class competitor(models.Model):
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    competitor_domain_name=models.CharField(max_length=255)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.competitor_domain_name


class competitor_domain_mapping(models.Model):
    COMPETITOR_TYPE_CHOICES = [
        ('sitemap', 'Sitemap'),
        ('category', 'Category'),
    ]
    INTERVAL_UNIT_CHOICES = [
    ('minute', 'Minute'),
    ('hour', 'Hour'),
    ('day', 'Day'),
    ]

    slug_id = models.CharField(max_length=100,default="",  blank=True)
    domain_id=models.CharField(max_length=255)
    workspace_id=models.CharField(max_length=255)
    wp_status=models.CharField(max_length=255)
    article_status=models.CharField(max_length=255)
    wp_schedule_time=models.DateTimeField(default=timezone.now)
    article_priority=models.IntegerField(default=0)
    ai_content_flags=models.JSONField(default=dict)
    wp_author=models.CharField(max_length=255)
    wp_category=models.JSONField(default=dict)
    wp_tag=models.JSONField(default=dict)
    prompt=models.JSONField(default=dict)
    article_type=models.JSONField(default=dict)
    domain=models.JSONField(default=dict)
    workspace=models.JSONField(default=dict)
    competitor_id=models.ForeignKey(competitor, on_delete=models.SET_NULL, null=True, blank=True)
    competitor_type = models.CharField(
            max_length=50,
            choices=COMPETITOR_TYPE_CHOICES,
            default='sitemap'
    )    
    interval = models.IntegerField(default=30)
    interval_unit = models.CharField(max_length=10, choices=INTERVAL_UNIT_CHOICES, default='minute')
    created_by=models.CharField(max_length=255)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return  " Mapping Domain: " + self.domain_id



class competitor_selected_url(models.Model):
    SCRAP_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    EXTRACTION_METHOD_CHOICES = [
        ('loadmore', 'Load More'),
        ('nxtbtn', 'Next Button'),
        ('manual', 'Manual'),
    ]
    CHECK_METHOD_CHOICES = [
        ('requests', 'Requests'),
        ('selenium', 'Selenium'),
    ]

    slug_id = models.CharField(max_length=100,default="",  blank=True)
    competitor_id=models.ForeignKey(competitor, on_delete=models.SET_NULL, null=True, blank=True)
    selected_url=models.URLField(max_length=255)

    competitor_domain_mapping_id=models.ForeignKey(competitor_domain_mapping, on_delete=models.SET_NULL, null=True, blank=True)
    monitor_enabled=models.BooleanField(default=True)
    last_api_call_at=models.DateTimeField(default=timezone.now)
    next_api_call_at=models.DateTimeField(default=timezone.now)
    start_time=models.DateTimeField(default=timezone.now)
    end_time=models.DateTimeField(default=timezone.now)

    scrap_status = models.CharField(
        max_length=20,
        choices=SCRAP_STATUS_CHOICES,
        default='pending'
    )
    responses_status_code=models.IntegerField(default=200)
    extraction_method = models.CharField(
        max_length=20,
        choices=EXTRACTION_METHOD_CHOICES,
        default='manual'
    )
    check_method=models.CharField(
        max_length=20,
        choices=CHECK_METHOD_CHOICES,
        default='requests'
    )
    proxy = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional proxy (e.g., http://user:pass@ip:port)"
    )
    created_by=models.CharField(max_length=255)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.selected_url
    

class competitor_article_url(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    article_url=models.URLField(max_length=255)
    competitor_selected_url_id=models.ForeignKey(competitor_selected_url, on_delete=models.SET_NULL, null=True, blank=True)
    competitor_domain_mapping_id=models.ForeignKey(competitor_domain_mapping, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_status = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS_CHOICES,
        default='pending'
    )
    last_modified_date=models.DateTimeField(default=timezone.now)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.article_url


class category_url_selector(models.Model):
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    competitor_selected_url_id=models.ForeignKey(competitor_selected_url, on_delete=models.SET_NULL, null=True, blank=True)
    selector_name=models.CharField(max_length=255)
    selector=models.CharField(max_length=255)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.selector_name

class article_url_selector(models.Model):
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    competitor_article_url_id=models.ForeignKey(competitor_article_url, on_delete=models.SET_NULL, null=True, blank=True)
    competitor_selected_url_id=models.ForeignKey(competitor_selected_url, on_delete=models.SET_NULL, null=True, blank=True)
    source_title=models.JSONField(default=dict)
    source_content=models.JSONField(default=dict)
    source_featured_image=models.JSONField(default=dict)
    source_author=models.JSONField(default=dict)
    source_published_date=models.JSONField(default=dict)
    source_categories=models.JSONField(default=dict)
    source_tags=models.JSONField(default=dict)
    source_remove_selector=models.JSONField(default=dict)
    source_meta_description=models.JSONField(default=dict)
    source_meta_keywords=models.JSONField(default=dict)
    source_meta_title=models.JSONField(default=dict)
    source_outline=models.JSONField(default=list)
    source_internal_links=models.JSONField(default=list)
    source_external_links=models.JSONField(default=list)
    source_remove_selectors=models.JSONField(default=list)
    source_faqs=models.JSONField(default=list)

    is_verified=models.BooleanField(default=False)
    verified_by=models.CharField(max_length=255)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.verified_by

class competitor_selector_prompt(models.Model):
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    competitor_domain_mapping_id=models.ForeignKey(competitor_domain_mapping, on_delete=models.SET_NULL, null=True, blank=True)
    prompt=models.JSONField(default=dict)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.prompt

class competitor_url_daily_stats(models.Model):
    slug_id = models.CharField(max_length=100, default="", blank=True)
    competitor_selected_url_id = models.ForeignKey(competitor_selected_url, on_delete=models.CASCADE)
    stat_date = models.DateField()  # Daily bucket
    
    # Execution metrics
    total_runs = models.IntegerField(default=0)
    successful_runs = models.IntegerField(default=0)
    failed_runs = models.IntegerField(default=0)
    
    # Article discovery metrics
    total_articles_found = models.IntegerField(default=0)
    new_articles_added = models.IntegerField(default=0)
    duplicate_articles_skipped = models.IntegerField(default=0)
    
    # Performance metrics
    total_response_time_ms = models.BigIntegerField(default=0)  # Sum for calculating average
    fastest_response_ms = models.IntegerField(default=0)
    slowest_response_ms = models.IntegerField(default=0)
    
    # Error tracking
    last_error_message = models.TextField(blank=True, null=True)
    error_count = models.IntegerField(default=0)
    
    # Timestamps
    first_run_at = models.DateTimeField(null=True, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['competitor_selected_url_id', 'stat_date']
        indexes = [
            models.Index(fields=['stat_date']),
            models.Index(fields=['competitor_selected_url_id', 'stat_date']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @property
    def success_rate(self):
        if self.total_runs == 0:
            return 0
        return (self.successful_runs / self.total_runs) * 100

    @property
    def avg_response_time_ms(self):
        if self.successful_runs == 0:
            return 0
        return self.total_response_time_ms / self.successful_runs

    def __str__(self):
        return f"Stats for {self.competitor_selected_url_id.selected_url} on {self.stat_date}"
