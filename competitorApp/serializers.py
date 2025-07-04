from rest_framework import serializers
from competitorApp.models import competitor, competitor_article_url, competitor_domain_mapping, competitor_selected_url, category_url_selector, article_url_selector, competitor_selector_prompt

class competitor_domain_mapping_serializer(serializers.ModelSerializer):
    class Meta:
        model = competitor_domain_mapping
        exclude = ['id','created_date', 'updated_date']

class competitor_serializer(serializers.ModelSerializer):
    domain_mapping_data = competitor_domain_mapping_serializer(source='competitor_domain_mapping_set', many=True, read_only=True)
    
    class Meta:
        model = competitor
        exclude = ['id','created_date', 'updated_date']


class competitor_selected_url_serializer(serializers.ModelSerializer):
    class Meta:
        model = competitor_selected_url
        exclude = ['id','created_date', 'updated_date']

class competitor_article_url_serializer(serializers.ModelSerializer):
    class Meta:
        model = competitor_article_url
        exclude = ['id','created_date', 'updated_date']

class category_url_selector_serializer(serializers.ModelSerializer):
    class Meta:
        model = category_url_selector
        exclude = ['id','created_date', 'updated_date']

class article_url_selector_serializer(serializers.ModelSerializer):
    class Meta:
        model = article_url_selector
        exclude = ['id','created_date', 'updated_date']

class competitor_selector_prompt_serializer(serializers.ModelSerializer):
    class Meta:
        model = competitor_selector_prompt
        exclude = ['id','created_date', 'updated_date']
