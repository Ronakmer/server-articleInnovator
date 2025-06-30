


from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from django.db.models import Q
from AIMessageService.models import input_json
from AIMessageService.serializers import input_json_serializer
from AIMessageService.views.base.process_pagination.process_pagination import process_pagination
import json
# import redis


def add_article_input_json(request_data):
    try:
        serializer = input_json_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return {
                'success': True,
                'message': 'Data saved successfully',
                'data': serializer.data,
                'status': 200
            }

        return {
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors,
            'status': 400
        }

    except Exception as e:
        print("Error in save_article_input_json:", e)
        return {
            'success': False,
            'message': 'Internal server error',
            'status': 500
        }
