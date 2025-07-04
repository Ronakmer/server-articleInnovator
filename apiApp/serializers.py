
from rest_framework import serializers
from django.contrib.auth.models import User
from apiApp.models import (
    invitation_code_detail, role, dynamic_avatar_image,
    workspace, user_detail, permission, domain, wp_tag,
    wp_category, wp_author, ai_configuration, color_detail,
    language, country, motivation, article_type_field,
    article_type, prompt, image_tag, image_template_category,
    image_template, image_tag_template_category_template_mapping,
    article, article_info,  user_api_key, keyword,
    console_metrics, image_kit_configuration, activity_log, notification,
    supportive_prompt_type, supportive_prompt, variables, rabbitmq_queue,
    integration, integration_type
    
)


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']
                
        
class invitation_code_detail_serializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    email = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False)

    created_by_data = user_serializer(source='created_by', read_only=True)  
    email_data = user_serializer(source='email', read_only=True)  

    class Meta:
        model = invitation_code_detail
        exclude = ['id', 'created_date', 'updated_date']


class role_serializer(serializers.ModelSerializer):
    class Meta:
        model = role
        exclude = ['id', 'created_date', 'updated_date']
 
        
class permission_serializer(serializers.ModelSerializer):
    class Meta:
        model = permission
        exclude = ['id', 'created_date', 'updated_date']       


class dynamic_avatar_image_serializer(serializers.ModelSerializer):
    class Meta:
        model = dynamic_avatar_image
        exclude = ['id', 'created_date', 'updated_date']  

        
class for_workspace_user_detail_serializer(serializers.ModelSerializer):
    user_id = user_serializer()  

    class Meta:
        model = user_detail
        fields = ['full_name', 'slug_id', 'user_id']


class workspace_serializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    created_by_data = user_serializer(source='created_by', read_only=True)  
    user_details = for_workspace_user_detail_serializer(many=True, read_only=True) 
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = workspace
        exclude = ['id', 'created_date', 'updated_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Ensure user_details is correctly populated 
        representation['user_details'] = for_workspace_user_detail_serializer(instance.user_details.all(), many=True).data
      
        return representation


class ai_configuration_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True) 
    created_by_data = user_serializer(source='created_by', read_only=True)  
    
    class Meta:
        model = ai_configuration
        exclude = ['id', 'created_date', 'updated_date']

class image_kit_configuration_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True) 
    created_by_data = user_serializer(source='created_by', read_only=True)  
    
    class Meta:
        model = image_kit_configuration
        exclude = ['id', 'created_date', 'updated_date']
        

        
class user_detail_serializer(serializers.ModelSerializer):
    user_id = user_serializer()  
    role_id = role_serializer()  
    workspace_id = workspace_serializer(many=True)  
    created_by = user_serializer()

    class Meta:
        model = user_detail
        exclude = ['id', 'created_date', 'updated_date']


class domain_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(queryset=user_detail.objects.all(), many=True, write_only=True, required=False)
    writer_id = serializers.PrimaryKeyRelatedField(queryset=user_detail.objects.all(), many=True, write_only=True, required=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
    manager_id_data = user_detail_serializer(source='manager_id', read_only=True, many=True,)  
    writer_id_data = user_detail_serializer(source='writer_id', read_only=True, many=True,)  
    created_by_data = user_serializer(source='created_by', read_only=True)  


    class Meta:
        model = domain
        exclude = ['id', 'created_date', 'updated_date']


        
class wp_tag_serializer(serializers.ModelSerializer):
    domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
     
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  


    class Meta:
        model = wp_tag
        exclude = ['id', 'created_date', 'updated_date']       

        
class wp_category_serializer(serializers.ModelSerializer):    
    domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
     
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
    
    class Meta:
        model = wp_category
        exclude = ['id', 'created_date', 'updated_date']       


class wp_author_serializer(serializers.ModelSerializer):      
    domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
     
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  

    class Meta:
        model = wp_author
        exclude = ['id', 'created_date', 'updated_date', 'author_password']       
    
    
        
class color_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = color_detail
        exclude = ['id', 'created_date', 'updated_date'] 

          
class language_serializer(serializers.ModelSerializer):
    class Meta:
        model = language
        exclude = ['id', 'created_date', 'updated_date']  
        
        
class country_serializer(serializers.ModelSerializer):
    class Meta:
        model = country
        exclude = ['id', 'created_date', 'updated_date']  

        
class motivation_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), many=True, write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    workspace_id_data = workspace_serializer(source='workspace_id', many=True, read_only=True)  
    created_by_data = user_serializer(source='created_by', read_only=True)  

    class Meta:
        model = motivation
        exclude = ['id', 'created_date', 'updated_date']       

        
class article_type_field_serializer(serializers.ModelSerializer):
    class Meta:
        model = article_type_field
        exclude = ['id', 'created_date', 'updated_date']
        
class article_type_serializer(serializers.ModelSerializer): 
    article_type_field_id = serializers.PrimaryKeyRelatedField(queryset=article_type_field.objects.all(), write_only=True, many=True,required=False,allow_null=True)
    color_detail_id = serializers.PrimaryKeyRelatedField(queryset=color_detail.objects.all(), write_only=True,required=False,allow_null=True)
    
    
    article_type_field_id_data = article_type_field_serializer(source='article_type_field_id', read_only=True, many=True) 
    color_detail_id_data = color_detail_serializer(source='color_detail_id', read_only=True)  


    class Meta:
        model = article_type
        exclude = ['id', 'created_date', 'updated_date']





  
class rabbitmq_queue_serializer(serializers.ModelSerializer): 
    article_type_id_id = serializers.PrimaryKeyRelatedField(queryset=article_type.objects.all(), write_only=True, required=False, allow_null=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True,required=False,allow_null=True)

    article_type_id_data = article_type_serializer(source='article_type_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  

    class Meta:
        model = rabbitmq_queue
        exclude = ['id', 'created_date', 'updated_date']
  


class supportive_prompt_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = supportive_prompt_type
        exclude = ['id', 'created_date', 'updated_date']

  
class variables_serializer(serializers.ModelSerializer): 
    supportive_prompt_type_id = serializers.PrimaryKeyRelatedField(queryset=supportive_prompt_type.objects.all(), write_only=True, required=False, allow_null=True)
    article_type_id_id = serializers.PrimaryKeyRelatedField(queryset=article_type.objects.all(), write_only=True, required=False, allow_null=True)
    # workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)

    supportive_prompt_type_id_data = supportive_prompt_type_serializer(source='supportive_prompt_type_id', read_only=True) 
    article_type_id_data = article_type_serializer(source='article_type_id', read_only=True) 
    # workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  

    class Meta:
        model = variables
        exclude = ['id', 'created_date', 'updated_date']
  
  
class supportive_prompt_serializer(serializers.ModelSerializer): 
    supportive_prompt_type_id = serializers.PrimaryKeyRelatedField(queryset=supportive_prompt_type.objects.all(), write_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)

    supportive_prompt_type_id_data = supportive_prompt_type_serializer(source='supportive_prompt_type_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  

    class Meta:
        model = supportive_prompt
        exclude = ['id', 'created_date', 'updated_date']

        
class prompt_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    article_type_id = serializers.PrimaryKeyRelatedField(queryset=article_type.objects.all(), write_only=True, required=False)

    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True) 
    created_by_data = user_serializer(source='created_by', read_only=True)  
    article_type_id_data = article_type_serializer(source='article_type_id', read_only=True) 


    class Meta:
        model = prompt
        exclude = ['id', 'created_date', 'updated_date']


        
class image_tag_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)     
    created_by_data = user_serializer(source='created_by', read_only=True)  

    class Meta:
        model = image_tag
        exclude = ['id', 'created_date', 'updated_date']


        
class image_template_category_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)     
    created_by_data = user_serializer(source='created_by', read_only=True)  

    class Meta:
        model = image_template_category
        exclude = ['id', 'created_date', 'updated_date']

        
class image_template_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    image_tag_id = serializers.PrimaryKeyRelatedField(queryset=image_tag.objects.all(), write_only=True, many=True, required=False)
    image_template_category_id = serializers.PrimaryKeyRelatedField(queryset=image_template_category.objects.all(), write_only=True, many=True, required=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)     
    image_tag_id_data = image_tag_serializer(source='image_tag_id', read_only=True, many=True)     
    image_template_category_id_data = image_template_category_serializer(source='image_template_category_id', read_only=True, many=True)     
    created_by_data = user_serializer(source='created_by', read_only=True)  

    class Meta:
        model = image_template
        exclude = ['id', 'created_date', 'updated_date']


        
class image_tag_template_category_template_mapping_serializer(serializers.ModelSerializer):
    class Meta:
        model = image_tag_template_category_template_mapping
        fields = '__all__'
        
        
class article_serializer(serializers.ModelSerializer):
    # workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    # created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    # article_type_id = serializers.PrimaryKeyRelatedField(queryset=article_type.objects.all(), write_only=True)
    # domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
    # prompt_id = serializers.PrimaryKeyRelatedField(queryset=prompt.objects.all(), write_only=True,allow_null=True,required=False)
    # wp_author_id = serializers.PrimaryKeyRelatedField(queryset=wp_author.objects.all(), write_only=True,allow_null=True,required=False)
    # wp_category_id = serializers.PrimaryKeyRelatedField(queryset=wp_category.objects.all(), write_only=True, many=True,allow_null=True,required=False)
    # wp_tag_id = serializers.PrimaryKeyRelatedField(queryset=wp_tag.objects.all(), write_only=True, many=True,allow_null=True,required=False)
    
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=workspace.objects.all(), write_only=True, required=False, allow_null=True
    )
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, required=False, allow_null=True
    )
    article_type_id = serializers.PrimaryKeyRelatedField(
        queryset=article_type.objects.all(), write_only=True, required=False, allow_null=True
    )
    domain_id = serializers.PrimaryKeyRelatedField(
        queryset=domain.objects.all(), write_only=True, required=False, allow_null=True
    )
    prompt_id = serializers.PrimaryKeyRelatedField(
        queryset=prompt.objects.all(), write_only=True, required=False, allow_null=True
    )
    wp_author_id = serializers.PrimaryKeyRelatedField(
        queryset=wp_author.objects.all(), write_only=True, required=False, allow_null=True
    )
    wp_category_id = serializers.PrimaryKeyRelatedField(
        queryset=wp_category.objects.all(), write_only=True, many=True, required=False, allow_null=True
    )
    wp_tag_id = serializers.PrimaryKeyRelatedField(
        queryset=wp_tag.objects.all(), write_only=True, many=True, required=False, allow_null=True
    )

    

    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True) 
    created_by_data = user_serializer(source='created_by', read_only=True)  
    article_type_id_data = article_type_serializer(source='article_type_id', read_only=True) 
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 
    prompt_id_data = prompt_serializer(source='prompt_id', read_only=True) 
    wp_author_id_data = wp_author_serializer(source='wp_author_id', read_only=True) 
    wp_category_id_data = wp_category_serializer(source='wp_category_id', read_only=True, many=True) 
    wp_tag_id_data = wp_tag_serializer(source='wp_tag_id', read_only=True, many=True) 

    class Meta:
        model = article
        exclude = ['id', 'updated_date']
        
        
class article_info_serializer(serializers.ModelSerializer):
    # article_id_data = article_serializer(source='article_id', read_only=True) 

    class Meta:
        model = article_info
        exclude = ['id', 'created_date', 'updated_date']
        
        
        
# class competitor_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = competitor
#         exclude = ['id', 'created_date', 'updated_date']  
        
        
        
        
# class competitor_domain_mapping_serializer(serializers.ModelSerializer): 
#     domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
#     workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
#     competitor_id = serializers.PrimaryKeyRelatedField(queryset=competitor.objects.all(), write_only=True)
#     created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
#     article_type_id = serializers.PrimaryKeyRelatedField(queryset=article_type.objects.all(), write_only=True)
#     prompt_id = serializers.PrimaryKeyRelatedField(queryset=prompt.objects.all(), write_only=True)

#     domain_id_data = domain_serializer(source='domain_id', read_only=True) 
#     workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
#     competitor_id_data = color_detail_serializer(source='competitor_id', read_only=True)  
#     created_by_data = user_serializer(source='created_by', read_only=True)  
#     article_type_id_data = article_type_serializer(source='article_type_id', read_only=True)  
#     prompt_id_data = prompt_serializer(source='prompt_id', read_only=True)  


#     class Meta:
#         model = competitor_domain_mapping
#         exclude = ['id', 'created_date', 'updated_date']  

        
        
# class competitor_sitemap_url_serializer(serializers.ModelSerializer):
#     competitor_id = serializers.PrimaryKeyRelatedField(queryset=competitor.objects.all(), write_only=True)

#     competitor_id_data = color_detail_serializer(source='competitor_id', read_only=True)  


#     class Meta:
#         model = competitor_sitemap_url
#         exclude = ['id', 'created_date', 'updated_date']  

        
        
        
# class competitor_sitemap_url_mapping_serializer(serializers.ModelSerializer):
#     domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
#     workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
#     competitor_id = serializers.PrimaryKeyRelatedField(queryset=competitor.objects.all(), write_only=True)
#     created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
#     competitor_sitemap_url_id = serializers.PrimaryKeyRelatedField(queryset=competitor_sitemap_url.objects.all(), write_only=True)

#     domain_id_data = domain_serializer(source='domain_id', read_only=True) 
#     workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
#     competitor_id_data = color_detail_serializer(source='competitor_id', read_only=True)  
#     created_by_data = user_serializer(source='created_by', read_only=True)  
#     competitor_sitemap_url_id_data = competitor_sitemap_url_serializer(source='competitor_sitemap_url_id', read_only=True)  

#     class Meta:
#         model = competitor_sitemap_url_mapping
#         exclude = ['id', 'created_date', 'updated_date']  

        
        
# class competitor_article_url_serializer(serializers.ModelSerializer):
#     competitor_id = serializers.PrimaryKeyRelatedField(queryset=competitor.objects.all(), write_only=True)

#     competitor_id_data = color_detail_serializer(source='competitor_id', read_only=True)  

#     class Meta:
#         model = competitor_article_url
#         exclude = ['id', 'created_date', 'updated_date']  
        
        
#          
        
        
# class competitor_seo_extraction_mapping_serializer(serializers.ModelSerializer):
#     domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
#     workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
#     competitor_id = serializers.PrimaryKeyRelatedField(queryset=competitor.objects.all(), write_only=True)
#     created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
#     competitor_extraction_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

#     domain_id_data = domain_serializer(source='domain_id', read_only=True) 
#     workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
#     competitor_id_data = color_detail_serializer(source='competitor_id', read_only=True)  
#     created_by_data = user_serializer(source='created_by', read_only=True)  
#     competitor_extraction_id_data = competitor_extraction_serializer(source='competitor_extraction_id', read_only=True)  


#     class Meta:
#         model = competitor_seo_extraction_mapping
#         exclude = ['id', 'created_date', 'updated_date']  

        
        
class user_api_key_serializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    user_detail_id = serializers.PrimaryKeyRelatedField(queryset=user_detail.objects.all(), write_only=True)
    
    created_by_data = user_serializer(source='created_by', read_only=True)  
    user_detail_id_data = user_detail_serializer(source='user_detail_id', read_only=True)  

    class Meta:
        model = user_api_key
        exclude = ['id', 'created_date', 'updated_date']  

        
class keyword_serializer(serializers.ModelSerializer):
    prompt_id = serializers.PrimaryKeyRelatedField(queryset=prompt.objects.all(), write_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    article_type_id = serializers.PrimaryKeyRelatedField(queryset=article_type.objects.all(), write_only=True)
    language_id = serializers.PrimaryKeyRelatedField(queryset=language.objects.all(), write_only=True)
    country_id = serializers.PrimaryKeyRelatedField(queryset=country.objects.all(), write_only=True)
     
    prompt_id_data = prompt_serializer(source='prompt_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
    article_type_id_data = article_type_serializer(source='article_type_id', read_only=True)  
    language_id_data = language_serializer(source='language_id', read_only=True)  
    country_id_data = country_serializer(source='country_id', read_only=True)  

    class Meta:
        model = keyword
        exclude = ['id', 'created_date', 'updated_date']  

        
        



class console_metrics_serializer(serializers.ModelSerializer):
    domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 
    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True)  
    

    class Meta:
        model = console_metrics
        exclude = ['id', 'created_date', 'updated_date']  
        
        
        

class activity_log_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)

    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True) 
    user_id_data = user_serializer(source='user_id', read_only=True)  
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 

    class Meta:
        model = activity_log
        exclude = ['id', 'created_date']



class notification_serializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(queryset=workspace.objects.all(), write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    domain_id = serializers.PrimaryKeyRelatedField(queryset=domain.objects.all(), write_only=True)

    workspace_id_data = workspace_serializer(source='workspace_id', read_only=True) 
    user_id_data = user_serializer(source='user_id', read_only=True)  
    domain_id_data = domain_serializer(source='domain_id', read_only=True) 

    class Meta:
        model = notification
        exclude = ['id', 'created_date']
        
        
        
class integration_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = integration_type
        exclude = ['id', 'created_date', 'updated_date']  

        
class integration_serializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    integration_type_id = serializers.PrimaryKeyRelatedField(queryset=integration_type.objects.all(), write_only=True)

    created_by_data = user_serializer(source='created_by', read_only=True)  
    integration_type_id_data = integration_type_serializer(source='integration_type_id', read_only=True) 

    class Meta:
        model = integration
        exclude = ['id', 'created_date', 'updated_date']  