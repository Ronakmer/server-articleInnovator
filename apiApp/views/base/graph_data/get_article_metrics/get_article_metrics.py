from django.http import JsonResponse
from django.db.models import Q, Sum
from django.core.serializers import serialize
import json
from apiApp.models import console_metrics, domain, workspace, article, wp_category
from rest_framework.decorators import api_view

from django.db.models import Count
from django.db.models.functions import TruncDate


# Helper function to fetch metrics and aggregate data
def get_article_metrics(queryset):
    if not queryset.exists():
        return None

    # Group articles by date and count total articles for each date
    article_by_date = queryset.annotate(date=TruncDate('wp_schedule_time')).values('date').annotate(total_articles_by_date=Count('id')).order_by('date')

    # Convert the QuerySet result to a dictionary with date in 'YYYY-MM-DD' format
    article_by_date_dict = {
        result['date'].strftime('%Y-%m-%d'): result['total_articles_by_date']
        for result in article_by_date
    }

    total_articles = queryset.count()

    total_publish = queryset.filter(wp_status='publish').count()
    total_draft = queryset.filter(wp_status='draft').count()
    total_scheduled = queryset.filter(wp_status='future').count()

                
    # Calculate articles count per category
    category_article_count = {}
    categories = wp_category.objects.filter(domain_id__in=queryset.values('domain_id')).distinct()
    
    for category in categories:
        category_count = queryset.filter(wp_category_id=category).count()
        category_article_count[category.name] = category_count
        
    print(total_scheduled,'total_scheduled')
        
        
    return {
        'total_publish':total_publish,
        'total_draft':total_draft,
        'total_scheduled':total_scheduled,
        'total_articles':total_articles,
        'article_by_date_dict':article_by_date_dict,
        'category_article_count': category_article_count  # Add category count here

    }


