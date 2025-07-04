from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import datetime
import random, os, json
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.

            

#  invitation code details
class invitation_code_detail(models.Model):
    invitation_code = models.CharField(max_length=100,default="", blank=True, unique=True)
    article_limitation = models.IntegerField(default=1000, null=True, blank=True)
    domain_limitation = models.IntegerField(default=10, null=True, blank=True)
    workspace_limitation = models.IntegerField(default=10, null=True, blank=True)
    used = models.BooleanField(default=False)
    used_date = models.DateField(null=True, blank=True)
    email = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, related_name='created_by_user', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.invitation_code
    
    
#  role
class role(models.Model):
    name = models.CharField(max_length=200, default="", unique=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100, default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        # Convert the name to lowercase
        self.name = self.name.lower()

        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


#  permission 
class permission(models.Model):
    name = models.CharField(max_length=200,default="")
    description = models.CharField(max_length=200,default="")
    group = models.CharField(max_length=200,default="")
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
 
 
    
#  role has permissions 
class role_has_permissions(models.Model):
    permission_id=models.ForeignKey(to=permission,on_delete=models.CASCADE)
    role_id=models.ForeignKey(to=role,on_delete=models.CASCADE)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.role_id.name} - {self.permission_id.name}"
    
    
    
# dynamic avatar image
class dynamic_avatar_image(models.Model):
    AVATAR_CHOICES = [
        ('workspace', 'Workspace'),
        ('profile', 'Profile'),
    ]
    
    avatar_type = models.CharField(max_length=200, choices=AVATAR_CHOICES, null=True, blank=True)
    avatar_image = models.ImageField(upload_to="avatar", default="")
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        
        if self.pk:
            # Fetch the previous avatar_image to compare
            original_instance = dynamic_avatar_image.objects.get(pk=self.pk)
            if self.avatar_image and self.avatar_image != original_instance.avatar_image:
                # Only change the image name if the image has been updated
                if self.avatar_type:
                    ext = os.path.splitext(self.avatar_image.name)[1]
                    self.avatar_image.name = f"{self.avatar_type}_{self.slug_id}{ext}"
        else:
            # New instance, change the image name right away
            if self.avatar_type:
                ext = os.path.splitext(self.avatar_image.name)[1]
                self.avatar_image.name = f"{self.avatar_type}_{self.slug_id}{ext}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.avatar_type


#  workspace 
class workspace(models.Model):
    name = models.CharField(max_length=200,default="", unique=True)
    # rabbitmq_queue = models.TextField(null=True, blank=True, default="")
    logo = models.FileField(upload_to="workspace", null=True, blank=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
#  ai Configuration
class ai_configuration(models.Model):
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=200,default="",  blank=True)
    api_provider = models.CharField(max_length=200,default="",  blank=True)
    api_type = models.CharField(max_length=200,default="",  blank=True)
    api_version = models.CharField(max_length=200,default="",  blank=True)
    api_url = models.CharField(max_length=200,default="",  blank=True)
    api_key = models.CharField(max_length=200,default="",  blank=True)
    api_model = models.CharField(max_length=200,default="",  blank=True)
    ai_rate_key_id = models.CharField(max_length=200,default="",  blank=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.api_type} - {self.email}"



#  image kit Configuration
class image_kit_configuration(models.Model):
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    public_key = models.CharField(max_length=200, default="", blank=True)
    private_key = models.CharField(max_length=200, default="", blank=True)
    url_endpoint = models.CharField(max_length=200, default="", blank=True)
    status = models.BooleanField(default=True)
    default_section = models.BooleanField(default=False)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override

        # Ensure only one default_section=True per workspace
        if self.default_section:
            image_kit_configuration.objects.filter(workspace_id=self.workspace_id, default_section=True).update(default_section=False)

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.workspace_id.name}"



#  user detail
class user_detail(models.Model):
    user_id=models.ForeignKey(to=User,on_delete=models.CASCADE, null=True, blank=True)
    role_id=models.ForeignKey(to=role,on_delete=models.CASCADE, null=True, blank=True)
    workspace_id=models.ManyToManyField(workspace, related_name='user_details', blank=True)
    article_limitation=models.IntegerField(default=1000, null=True, blank=True)
    domain_limitation=models.IntegerField(default=10, null=True, blank=True)
    workspace_limitation=models.IntegerField(default=10, null=True, blank=True)
    full_name=models.CharField(max_length=100,default="",  blank=True)
    profile_image=models.ImageField(upload_to="user", default="",  blank=True)
    status=models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(to=User, related_name='created_by', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name



#  api key
class user_api_key(models.Model):
    user_detail_id = models.ForeignKey(to=user_detail,on_delete=models.CASCADE, null=True, blank=True)
    api_key = models.CharField(max_length=200,default="", blank=True)
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.api_key} - {self.user_detail_id.user_id.username}"
    


#  domain
class domain(models.Model):
    manager_id = models.ManyToManyField(user_detail, related_name='domain_manager', blank=True)
    writer_id = models.ManyToManyField(user_detail, related_name='domain_writer', blank=True)    
    name = models.CharField(max_length=200, unique=True)
    wordpress_username = models.CharField(max_length=200)
    wordpress_application_password = models.CharField(max_length=200)
    permalinks = models.CharField(max_length=200,default="")
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        print(self.manager_id)
        return self.name
    

#  wordpress tag
class wp_tag(models.Model):
    
    DERIVED_CHOICES = [
        ('ai', 'Ai'),
        ('wordpress', 'Wordpress'),
    ]

    domain_id = models.ForeignKey(to=domain,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="")
    slug = models.CharField(max_length=200,default="")
    description = models.CharField(max_length=1000,default="")
    wp_tag_id = models.CharField(max_length=200,default="")
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    derived_by =  models.CharField( max_length=50, choices=DERIVED_CHOICES, blank=True, null=True, default=None )
    

    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
#  wordpress category
class wp_category(models.Model):
    DERIVED_CHOICES = [
        ('ai', 'Ai'),
        ('wordpress', 'Wordpress'),
    ]


    domain_id = models.ForeignKey(to=domain,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="")
    slug = models.CharField(max_length=200,default="")
    description = models.CharField(max_length=1000,default="")
    wp_cat_id = models.CharField(max_length=200,default="")
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    derived_by =  models.CharField( max_length=50, choices=DERIVED_CHOICES, blank=True, null=True, default=None )
    default_section = models.BooleanField(default=False)


    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)


        # Ensure only one default_section=True per workspace
        if self.default_section:
            wp_category.objects.filter(domain_id=self.domain_id, default_section=True).update(default_section=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
#  wordpress author 
class wp_author(models.Model):
    
    DERIVED_CHOICES = [
        ('ai', 'Ai'),
        ('wordpress', 'Wordpress'),
    ]
    
    domain_id = models.ForeignKey(to=domain,on_delete=models.CASCADE)
    username = models.CharField(max_length=200,default="")
    author_password=models.CharField(max_length=200,default="")
    first_name = models.CharField(max_length=200,default="")
    last_name = models.CharField(max_length=200,default="")
    email = models.CharField(max_length=200,default="")
    bio = models.CharField(max_length=200,default="")
    wp_author_id = models.CharField(max_length=200,default="")
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    profile_image=models.ImageField(upload_to="wp_author", default="",  blank=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    derived_by =  models.CharField( max_length=50, choices=DERIVED_CHOICES, blank=True, null=True, default=None )

    default_section = models.BooleanField(default=False)

    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

        # Ensure only one default_section=True per workspace
        if self.default_section:
            wp_author.objects.filter(domain_id=self.domain_id, default_section=True).update(default_section=False)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username
    

#  color
class color_detail(models.Model):
    bg_color = models.CharField(max_length=200)
    text_color = models.CharField(max_length=200,default="")
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bg_color} - {self.text_color}"


#  language
class language(models.Model):
    name = models.CharField(max_length=200, default="", unique=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
#  country
class country(models.Model):
    name = models.CharField(max_length=200, default="", unique=True)
    country_flag=models.FileField(upload_to="country_flag", null=True, blank=True)    
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
   
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#  motivation
class motivation(models.Model):
    # workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    workspace_id = models.ManyToManyField(workspace, blank=True)
    
    quote = models.CharField(max_length=200, default="")
    quote_author = models.CharField(max_length=200, default="")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.quote} - {self.quote_author}"
    
    
#  article type field
class article_type_field(models.Model):
    name = models.CharField(max_length=200,default="")
    label = models.CharField(max_length=200,default="")
    placeholder = models.CharField(max_length=200,default="")
    field_type = models.CharField(max_length=200,default="")
    required = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


#  article type
class article_type(models.Model):
    
    CATEGORY_CHOICES = [
        ('keyword', 'Keyword'),
        ('url', 'Url'),
        # ('manual', 'Manual'),
    ]
    ARTICLE_CATEGORY_CHOICES = [
        ('generative', 'Generative'),
        ('rephrase', 'Rephrase'),
        ('outliner', 'Outliner'),
        ('manual', 'Manual'),
    ]

    article_type_field_id = models.ManyToManyField(article_type_field, blank=True)
    color_detail_id = models.ForeignKey(color_detail, on_delete=models.CASCADE,  null=True, blank=True)
    name = models.CharField(max_length=200,default="")
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, null=True, blank=True)
    article_type_image = models.ImageField(upload_to="article-type", default="",  blank=True)    
    article_category = models.CharField(max_length=200, choices=ARTICLE_CATEGORY_CHOICES, null=True, blank=True)
    title = models.CharField(max_length=200, default="",  blank=True)
    description = models.CharField(max_length=200, default="",  blank=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    # rabbitmq_queue = models.TextField(null=True, blank=True, default="")
    rabbitmq_worker = models.CharField(max_length=200, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



#  rabbitmq_queue
class rabbitmq_queue(models.Model):
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE, null=True, blank=True)
    article_type_id = models.ForeignKey(to=article_type, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default="",unique=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#  supportive_prompt_type
class supportive_prompt_type(models.Model):
    name = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=1000,default="")
    example = models.TextField(default="")
    # supportive_variables = models.TextField(default="")
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



#  variables
class variables(models.Model):
    # workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE, null=True, blank=True)
    supportive_prompt_type_id = models.ForeignKey(to=supportive_prompt_type, on_delete=models.CASCADE, null=True, blank=True)
    article_type_id = models.ForeignKey(to=article_type, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default="")
    required = models.BooleanField(default=True)
    value = models.TextField(default="")
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#  supportive_prompt
class supportive_prompt(models.Model):
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE, null=True, blank=True)
    supportive_prompt_type_id = models.ForeignKey(to=supportive_prompt_type, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=1000,default="")
    supportive_prompt_data = models.TextField(default="")
    ai_model = models.CharField(max_length=200, default="")

    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




#  prompt
class prompt(models.Model):
    article_type_id = models.ForeignKey(to=article_type, on_delete=models.CASCADE, null=True, blank=True)
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, default="")
    ai_rate_model = models.CharField(max_length=200, default="")
    prompt_data = models.JSONField(default=dict)  
    supportive_prompt_json_data = models.JSONField(default=dict)  
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
#   article
class article(models.Model):
    
    WP_STATUS_CHOICES = [
        ('publish', 'Publish'),
        ('draft', 'Draft'),
        ('future', 'Future'),
        ('trash', 'Trash'),
    ]
    ARTICLE_STATUS_CHOICES = [
        ('initiate ', 'Initiate'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('review', 'Review'),
    ]
    
    prompt_id = models.ForeignKey(to=prompt, on_delete=models.CASCADE, null=True, blank=True)
    article_type_id = models.ForeignKey(to=article_type, on_delete=models.CASCADE, null=True, blank=True)
    domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
    wp_author_id = models.ForeignKey(to=wp_author, on_delete=models.CASCADE, null=True, blank=True)
    wp_category_id = models.ManyToManyField(wp_category, blank=True)  
    wp_tag_id = models.ManyToManyField(wp_tag, blank=True)  
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE, null=True, blank=True)    
    wp_title = models.CharField(max_length=200, default="",  blank=True)
    wp_post_id = models.CharField(max_length=200, default="",  blank=True)
    wp_excerpt = models.CharField(max_length=500, default="",  blank=True)
    wp_modified_date = models.CharField(max_length=200, default="",  blank=True)
    keyword = models.CharField(max_length=200, default="",  blank=True)  
    url = models.CharField(max_length=200, default="",  blank=True)  
    wp_slug = models.CharField(max_length=200, default="",  blank=True)
    wp_content = models.CharField(max_length=500, default="",  blank=True)
    meta_description = models.CharField(max_length=200, default="",  blank=True)
    meta_tag = models.CharField(max_length=200, default="",  blank=True)
    meta_keyword = models.CharField(max_length=200, default="",  blank=True)
    wp_featured_image=models.CharField(max_length=200, default="", null=True, blank=True)    
    wp_status = models.CharField(max_length=200, choices=WP_STATUS_CHOICES, null=True, blank=True)
    article_status = models.CharField(max_length=200, choices=ARTICLE_STATUS_CHOICES, null=True, blank=True)    
    wp_schedule_time = models.DateTimeField(null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    ai_content_flags = models.JSONField(default=dict, blank=True, null=True)

    # is_category_selected_by_ai = models.BooleanField(default=True)
    # is_category_generated_by_ai = models.BooleanField(default=True)
    # is_tag_selected_by_ai = models.BooleanField(default=True)
    # is_tag_generated_by_ai = models.BooleanField(default=True)
    # is_author_selected_by_ai = models.BooleanField(default=True)
    # is_meta_description_generated_by_ai = models.BooleanField(default=True)
    # is_meta_keyword_generated_by_ai = models.BooleanField(default=True)
    # is_meta_title_generated_by_ai = models.BooleanField(default=True)
    # is_internal_links_generated_by_ai = models.BooleanField(default=True)
    # is_external_links_generated_by_ai = models.BooleanField(default=True)


    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)


    def __str__(self):
        return self.wp_title



#  article info
class article_info(models.Model):
    article_id = models.ForeignKey(to=article, on_delete=models.CASCADE, null=True, blank=True)

    custom_fields  = models.JSONField(default=dict)
    word_count = models.IntegerField(null=True, blank=True)
    image_count = models.IntegerField(null=True, blank=True)
    heading_count = models.IntegerField(null=True, blank=True)
    total_paragraphs = models.IntegerField(null=True, blank=True)
    long_paragraphs = models.IntegerField(null=True, blank=True)
    medium_paragraphs = models.IntegerField(null=True, blank=True)
    short_paragraphs = models.IntegerField(null=True, blank=True)
    total_sentences = models.IntegerField(null=True, blank=True)
    long_sentences = models.IntegerField(null=True, blank=True)
    medium_sentences = models.IntegerField(null=True, blank=True)
    short_sentences = models.IntegerField(null=True, blank=True)
    passive_sentences = models.IntegerField(null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.wp_title

    
    
#  internal links
class internal_links(models.Model):
    
    DERIVED_CHOICES = [
        ('ai', 'Ai'),
        ('wordpress', 'Wordpress'),
    ]
    
    article_id = models.ForeignKey(to=article, on_delete=models.CASCADE, null=True, blank=True)
    link_type = models.CharField(max_length=100, null=True, blank=True) # inbound / outbound
    post_title = models.CharField(max_length=100, null=True, blank=True)
    anchor_text = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    from_post_id = models.IntegerField(null=True, blank=True)
    to_post_id = models.IntegerField(null=True, blank=True)
    ai_generated = models.BooleanField(default=False)
    verify_by = models.ForeignKey(to=User, related_name='internal_links_verify_by', on_delete=models.SET_NULL, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    derived_by =  models.CharField( max_length=50, choices=DERIVED_CHOICES, blank=True, null=True, default=None )
    created_by = models.ForeignKey(to=User, related_name='internal_links_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.link_type



#  external links
class external_links(models.Model):
    
    DERIVED_CHOICES = [
        ('ai', 'Ai'),
        ('wordpress', 'Wordpress'),
    ]
    
    article_id = models.ForeignKey(to=article, on_delete=models.CASCADE, null=True, blank=True)
    anchor_text = models.CharField(max_length=100, null=True, blank=True)
    domain_name = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    ai_generated = models.BooleanField(default=False)
    verify_by = models.ForeignKey(to=User, related_name='external_links_verify_by', on_delete=models.SET_NULL, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    derived_by =  models.CharField( max_length=50, choices=DERIVED_CHOICES, blank=True, null=True, default=None )
    created_by = models.ForeignKey(to=User, related_name='external_links_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.anchor_text
    
    

#  console metrics
class console_metrics(models.Model):
    domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE)    #unic
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)  
    query = models.CharField(max_length=255)
    page = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    date = models.DateField()
    clicks = models.IntegerField()
    ctr = models.FloatField()
    impression = models.IntegerField()
    position = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     unique_together = ('query', 'page', 'country', 'device', 'date')

    def __str__(self):
        return self.query


#  analytics metrics
class analytics_metrics(models.Model):
    domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE)
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
    date = models.DateField()
    page = models.CharField(max_length=255)
    active_users = models.IntegerField()
    new_users = models.IntegerField()
    average_session_duration = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')}" 
    

#  domain install log
class domain_install_log(models.Model):
    domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
    log_type = models.CharField(max_length=100, null=True, blank=True)
    log_text = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
 
    
#  domain install log percentage % 
class domain_install_log_percentage(models.Model):
    domain_install_log_id = models.ForeignKey(to=domain_install_log, on_delete=models.CASCADE, null=True, blank=True)
    domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
    log_percentage = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)







# #  competitor
# class competitor(models.Model):
#     competitor_domain_name = models.CharField(max_length=100,default="",  blank=True)
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)

#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return self.competitor_domain_name


# #  competitor domain mapping
# class competitor_domain_mapping(models.Model):
        
#     COMPETITOR_TYPE_CHOICES = [
#         ('domain ', 'Domain'),
#         ('sitemap', 'Sitemap'),
#         ('category', 'Category'),
#     ]
#     INTERVAL_CHOICES = [
#         ('one-minute', 'One Minute'),
#         ('five-minutes', 'Five Minutes'),
#         ('thirty-minutes', 'Thirty Minutes'),
#         ('one-hour', 'One Hour'),
#         ('two-hours', 'Two Hours'),
#         ('five-hours', 'Five Hours'),
#         ('ten-hours', 'Ten Hours'),
#         ('twelve-hours', 'Twelve Hours'),
#         ('fifteen-hours', 'Fifteen Hours'),
#         ('one-day', 'One Day'),
#         ('three-days', 'Three Days'),
#         ('seven-days', 'Seven Days'),
#         ('fifteen-days', 'Fifteen Days'),
#     ]

#     prompt_id = models.ForeignKey(to=prompt, on_delete=models.CASCADE, null=True, blank=True)
#     article_type_id = models.ForeignKey(to=article_type, on_delete=models.CASCADE, null=True, blank=True)
#     domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
#     workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     competitor_type = models.CharField(max_length=200, choices=COMPETITOR_TYPE_CHOICES, default="")
#     interval = models.CharField(max_length=200, choices=INTERVAL_CHOICES, default="")
#     competitor_domain_name = models.CharField(max_length=100,default="",  blank=True)
#     last_col_time = models.DateField()
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)


#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"{self.competitor_domain_name} - {self.interval}" 

        
        
        
# # competitor sitemap url
# class competitor_sitemap_url(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     site_map_url = models.CharField(max_length=200,default="",  blank=True)
#     last_modified_date = models.DateField()
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)

#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"{self.site_map_url}" 
   

# #  competitor sitemap url mapping
# class competitor_sitemap_url_mapping(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     competitor_sitemap_url_id = models.ForeignKey(to=competitor_sitemap_url, on_delete=models.CASCADE, null=True, blank=True)
#     domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
#     selected_sitemap_url = models.BooleanField(default=False)
#     workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)


#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"competitor_id: {self.competitor_id} | competitor_sitemap_url_id: {self.competitor_sitemap_url_id} | selected_sitemap_url: {self.selected_sitemap_url}"
        
        
        
        
# # competitor article url
# class competitor_article_url(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     last_modified_date = models.DateField()
#     article_url = models.CharField(max_length=200,default="",  blank=True)
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)

#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"{self.article_url}"  
        
        
# # competitor article url mapping    
# class competitor_article_url_mapping(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     competitor_article_url_id = models.ForeignKey(to=competitor_article_url, on_delete=models.CASCADE, null=True, blank=True)
#     domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
#     selected_article_url = models.BooleanField(default=False)
#     workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)


#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"competitor_id: {self.competitor_id} | competitor_article_url_id: {self.competitor_article_url_id} | selected_article_url: {self.selected_article_url}"

        
        
# #  competitor extraction
# class competitor_extraction(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
#     workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
#     # selected_article_url = models.CharField(max_length=200,default="", null=True, blank=True)
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"{self.competitor_id.competitor_domain_name}"  
        

        
# #  competitor extraction mapping
# class competitor_extraction_mapping(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     competitor_extraction_id = models.ForeignKey(to=competitor_extraction, on_delete=models.CASCADE, null=True, blank=True)
#     domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
#     workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
#     selected_article_url = models.CharField(max_length=200,default="",  blank=True)
#     selecter_key = models.CharField(max_length=200,default="",  blank=True)
#     selecter_value = models.CharField(max_length=200,default="",  blank=True)
#     attribute_name = models.CharField(max_length=200,default="",  blank=True)
#     attribute_content = models.CharField(max_length=200,default="",  blank=True)
#     multiple_selection = models.BooleanField(default=False)
#     attribute_selection = models.BooleanField(default=False)
#     extra_selection = models.BooleanField(default=False)
#     remove_selection = models.BooleanField(default=False)

#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     def __str__(self):
#         return f"{self.selected_article_url}"      
        
        
# #  competitor seo extraction_mapping
# class competitor_seo_extraction_mapping(models.Model):
#     competitor_id = models.ForeignKey(to=competitor, on_delete=models.CASCADE, null=True, blank=True)
#     competitor_extraction_id = models.ForeignKey(to=competitor_extraction, on_delete=models.CASCADE, null=True, blank=True)
#     domain_id = models.ForeignKey(to=domain, on_delete=models.CASCADE, null=True, blank=True)
#     workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE)
#     remove_blocker_images = models.BooleanField(default=False)
#     remove_google_analytics = models.BooleanField(default=False)
#     remove_google_adsense = models.BooleanField(default=False)
#     remove_script = models.BooleanField(default=False)
#     remove_style = models.BooleanField(default=False)
#     remove_404_internal_links = models.BooleanField(default=False)
#     meta_title_selection = models.BooleanField(default=False)
#     meta_description_selection = models.BooleanField(default=False)
#     meta_keyword_selection = models.BooleanField(default=False)
#     slug_id = models.CharField(max_length=100,default="",  blank=True)
#     created_date=models.DateTimeField(default=timezone.now)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

#     # Generate a slug using UUID
#     def save(self, *args, **kwargs):
#         if not self.slug_id:
#             self.slug_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)
        
#     # def __str__(self):
#     #     return f"{self.selected_article_url}"  
        
        


#  keyword
class keyword(models.Model):
    INTERVAL_CHOICES = [
        ('one ', 'One'),
        ('two', 'Two'),
        ('three', 'Three'),
        ('four', 'Four'),
        ('five', 'Five'),
    ]


    prompt_id = models.ForeignKey(to=prompt, on_delete=models.CASCADE, null=True, blank=True)
    article_type_id = models.ForeignKey(to=article_type, on_delete=models.CASCADE, null=True, blank=True)
    workspace_id = models.ForeignKey(to=workspace, on_delete=models.CASCADE, null=True, blank=True)
    language_id = models.ForeignKey(to=language, on_delete=models.CASCADE, null=True, blank=True)
    country_id = models.ForeignKey(to=country, on_delete=models.CASCADE, null=True, blank=True)
    
    keyword_value = models.CharField(max_length=200, default="")
    interval = models.CharField(max_length=200, choices=INTERVAL_CHOICES, default="")
    google = models.BooleanField(null=True, blank=True)
    bing = models.BooleanField(null=True, blank=True)
    news = models.BooleanField(null=True, blank=True)
    web = models.BooleanField(null=True, blank=True)
    no_result = models.IntegerField(null=True, blank=True)
    proxy = models.CharField(max_length=200, default="")
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)


    def __str__(self):
        return self.keyword_value



#  notification 
class notification(models.Model):
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE, null=True, blank=True)
    domain_id = models.ForeignKey(to=domain,on_delete=models.CASCADE, null=True, blank=True)
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    send_time=models.DateTimeField(default=timezone.now, null=True, blank=True)
    seen_time=models.DateTimeField(null=True, blank=True)
    message=models.CharField(max_length=5000,default="", blank=True)
    read = models.BooleanField(default=False, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date=models.DateTimeField(default=timezone.now)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)


    def __str__(self):
        return self.message


#  activity log
class activity_log(models.Model):
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE, null=True, blank=True)
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    domain_id = models.ForeignKey(to=domain,on_delete=models.CASCADE, null=True, blank=True)
    level = models.CharField(max_length=100)
    message = models.TextField()
    url = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    status_code = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    user_role = models.CharField(max_length=100)
    line = models.IntegerField()
    user_status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date=models.DateTimeField(default=timezone.now)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

 
    def __str__(self):
        return f"{self.level} - {self.message[:50]}"
    


class integration_type(models.Model):
    PERMISSION_CHOICES = [
        ('superadmin', 'Superadmin'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=250, blank=True)
    permission_choice = models.CharField(max_length=250, choices=PERMISSION_CHOICES)
    integration_field = models.JSONField(blank=True)  # Store only keys like ["bucket_name", "access_key"]
    slug_id = models.CharField(max_length=100, default="", blank=True, unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class integration(models.Model):
    integration_type_id = models.ForeignKey(to=integration_type,on_delete=models.CASCADE, null=True, blank=True)
    integration_json_data = models.JSONField(blank=True)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100, default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.description} - {self.integration_type_id.name}"






######## image GEN ########
    
#   image tag
class image_tag(models.Model):
    # TAG_STATUS_CHOICES = [
    #     ('active', 'Active'),
    #     ('suspend', 'Suspend'),
    # ]

    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default="")
    # status = models.CharField( max_length=10, choices=TAG_STATUS_CHOICES, default='active')
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#   image template category
class image_template_category(models.Model):
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default="", unique=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    status = models.BooleanField(default=True)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#   image template
class image_template(models.Model):
    # TEMPLATE_STATUS_CHOICES = [
    #     ('active', 'Active'),
    #     ('suspend', 'Suspend'),
    # ]

    image_tag_id = models.ManyToManyField(image_tag, blank=True)
    image_template_category_id = models.ManyToManyField(image_template_category, blank=True)
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default="")
    template_json = models.TextField()
    template_image_path = models.TextField()
    # status = models.CharField( max_length=10, choices=TEMPLATE_STATUS_CHOICES, default='active')
    status = models.BooleanField(default=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
            self.status = True  # forcefully override
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#   template tag template mapping
class image_tag_template_category_template_mapping(models.Model):
    image_tag_id = models.ForeignKey(image_tag, on_delete=models.CASCADE, null=True, blank=True)
    image_template_category_id = models.ForeignKey(image_template_category, on_delete=models.CASCADE, null=True, blank=True)
    image_template_id = models.ForeignKey(image_template, on_delete=models.CASCADE, null=True, blank=True)
    workspace_id = models.ForeignKey(to=workspace,on_delete=models.CASCADE, null=True, blank=True)
    slug_id = models.CharField(max_length=100,default="",  blank=True)
    created_date=models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)

    # Generate a slug using UUID
    def save(self, *args, **kwargs):
        if not self.slug_id:
            self.slug_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.image_tag_id.name} - {self.image_template_category_id.name}-{self.image_template_id.name}"

