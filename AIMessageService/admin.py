from django.contrib import admin

# Register your models here.

from AIMessageService.models import ai_message, input_json

admin.site.register(ai_message)
admin.site.register(input_json)
