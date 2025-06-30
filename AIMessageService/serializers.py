

from rest_framework import serializers
from AIMessageService.models import ai_message, input_json


class ai_message_serializer(serializers.ModelSerializer):
    class Meta:
        model = ai_message
        # fields = '__all__'
        exclude = ['created_date', 'updated_date']
        
        
class input_json_serializer(serializers.ModelSerializer):
    class Meta:
        model = input_json
        # fields = '__all__'
        exclude = ['created_date', 'updated_date']

