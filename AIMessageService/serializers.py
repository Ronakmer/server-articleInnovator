

from rest_framework import serializers
from AIMessageService.models import ai_message

class ai_message_serializer(serializers.ModelSerializer):
    class Meta:
        model = ai_message
        # fields = '__all__'
        exclude = ['created_date', 'updated_date']

