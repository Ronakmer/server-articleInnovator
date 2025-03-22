from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import console_metrics_serializer
from apiApp.models import console_metrics, domain

# from .serializers import ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import json
from django.db.models import Sum, Avg, Func



def console_metrics_data(queryset):
    try:
        # Group by 'country' and aggregate the sums for other fields
        country_result = queryset.values('country').annotate(
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impression'),
            avg_ctr=Func(
                Avg('ctr'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure ctr is cast to NUMERIC and rounded
            ),
            avg_position=Func(
                Avg('position'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure position is cast to NUMERIC and rounded
            )
        ).order_by('country')

        # Group by 'page' and aggregate the sums for other fields
        page_result = queryset.values('page').annotate(
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impression'),
            avg_ctr=Func(
                Avg('ctr'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure ctr is cast to NUMERIC and rounded
            ),
            avg_position=Func(
                Avg('position'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure position is cast to NUMERIC and rounded
            )
        ).order_by('page')

        # Group by 'date' and aggregate the sums for other fields
        date_result = queryset.values('date').annotate(
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impression'),
            avg_ctr=Func(
                Avg('ctr'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure ctr is cast to NUMERIC and rounded
            ),
            avg_position=Func(
                Avg('position'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure position is cast to NUMERIC and rounded
            )
        ).order_by('date')

        # Group by 'query' and aggregate the sums for other fields
        query_result = queryset.values('query').annotate(
            total_clicks=Sum('clicks'),
            total_impressions=Sum('impression'),
            avg_ctr=Func(
                Avg('ctr'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure ctr is cast to NUMERIC and rounded
            ),
            avg_position=Func(
                Avg('position'), 
                function='ROUND', 
                template='ROUND(CAST(%(expressions)s AS NUMERIC), 2)'  # Ensure position is cast to NUMERIC and rounded
            )
        ).order_by('query')

        # Convert query result to JSON format
        date_result_list = list(date_result)
        for item in date_result_list:
            item['date'] = item['date'].strftime('%Y-%m-%d')  # Format date as string

        date_result = json.dumps(date_result_list)

        query_result_list = list(query_result)
        query_result = json.dumps(query_result_list)

        page_result_list = list(page_result)
        page_result = json.dumps(page_result_list)

        country_result_list = list(country_result)
        country_result = json.dumps(country_result_list)

        return {
            "date_result": date_result,
            "query_result": query_result,
            "page_result": page_result,
            "country_result": country_result
        }


    except Exception as e:
        print("This error is console_metrics_data --->: ", e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)
