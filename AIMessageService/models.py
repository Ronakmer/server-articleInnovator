from django.db import models
from django.utils import timezone

# Create your models here.


#  ai message
class ai_message(models.Model):
    article_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    article_message_count = models.IntegerField(default=0)
    article_message_total_count = models.IntegerField(default=0)
    ai_request = models.TextField(blank=True)
    ai_response = models.TextField(blank=True)
    ai_response_status = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message {self.message_id} for Article {self.article_id}"
