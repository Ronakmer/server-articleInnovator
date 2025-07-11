"""
Django settings for articleInnovator project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from pathlib import Path
import os
from datetime import timedelta
import platform
import sys



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4+hrr&l009p%xz&y220#1e5#z0*j#=f!t5m#cl74wzrhlwj2!s"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "corsheaders",
    "apiApp",
    "frontendApp",
    "AIMessageService",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "competitorApp",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", 
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apiApp.middleware.access_control.AccessControlMiddleware",  # custom access middleware for apiApp
    # "apiApp.middleware.rate_limit.RateLimitMiddleware",  # custom rate limit middleware
    # "apiApp.middleware.activity_log.ActivityLogMiddleware",  # custom log save for apiApp
    "frontendApp.middleware.access_control.AccessControlMiddleware",  # custom access middleware for frontendApp
    
]


ROOT_URLCONF = "articleInnovator.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "articleInnovator.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

############### start additional settings ###############


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'articleinnovators', 
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': '127.0.0.1', 
#         'PORT': '5432',
#     },
#      'ai_messages_db': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'ai_messages',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     },
#     'competitor_db': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'competitor',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': '127.0.0.1',
#         'PORT': '5433',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'articleinnovators',
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'OPTIONS': {
            'sslmode': os.getenv('PG_SSLMODE', 'require')
        }
    },
    'ai_messages_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ai_messages',
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'OPTIONS': {
            'sslmode': os.getenv('PG_SSLMODE', 'require')
        }
    },
    'competitor_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'competitor',
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'OPTIONS': {
            'sslmode': os.getenv('PG_SSLMODE', 'require')
        }
    }
}

############### end additional settings ###############



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



############### start additional settings ###############

#  static path
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

#  media path
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')


# smtp for mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ronakmer.dev@gmail.com' 
EMAIL_HOST_PASSWORD = 'oens yqpx zwxo tmbt'

#  Iframe
X_FRAME_OPTIONS = 'SAMEORIGIN'


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Using the database backend
SESSION_COOKIE_SECURE = False  # Set to True in production if using HTTPS
# SESSION_COOKIE_SECURE = True  # Set to True in production if using HTTPS


SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),    
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),  # Set to 2 hours
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}




REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
    

    

# AWS S3 settings

AWS_ACCESS_KEY_ID = 'AKIA6GBMBSQAVBQZMKF2'  
AWS_SECRET_ACCESS_KEY = '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' 
AWS_STORAGE_BUCKET_NAME = 'article-innovator-article-josn-files'  
AWS_S3_REGION_NAME = 'us-east-1' 
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"  





# wayback-files

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         # "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "custom_domain": AWS_S3_CUSTOM_DOMAIN,
#             "access_key": AWS_ACCESS_KEY_ID,
#             "secret_key": AWS_SECRET_ACCESS_KEY,
#             "region_name": AWS_S3_REGION_NAME,
#         }
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#         "LOCATION": "/static/",
#         'OPTIONS': {  
#             'location': BASE_DIR / 'static'
#         }
#     },
# }


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": os.path.join(BASE_DIR, "media"),
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "LOCATION": "/static/",
        "OPTIONS": {
            "location": os.path.join(BASE_DIR, "static"),
        },
    },
    "custom_s3": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "region_name": AWS_S3_REGION_NAME,
        },
        # "LOCATION": "custom_files/", 
    },
}




#  image kit config
IMAGEKIT = {
    'PUBLIC_KEY': 'public_tlF7GbY5ixVQhO3I49pUgym/4lA=',
    'PRIVATE_KEY': 'private_QsF9D6YRrbJdWLn8hnZROA4HCMk=',
    'URL_ENDPOINT': 'https://ik.imagekit.io/botxbyte',
}

# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # For development
        # 'BACKEND': 'django.core.cache.backends.redis.RedisCache', # Use Redis for production
        # 'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis configuration
        # 'LOCATION': 'unique-snowflake',

    }
}




# ip host

ALLOWED_HOSTS = ['http://192.168.1.3:8000', 'localhost', '192.168.1.3', '192.168.1.3', '*']

# CORS_ALLOWED_ORIGINS = [
#         'http://siteyouwantto.allow.com',
#         'http://anothersite.allow.com',
#     ]

CSRF_TRUSTED_ORIGINS = [
        'http://siteyouwantto.allow.com',
    ]




CORS_ALLOW_ALL_ORIGINS = True

USE_TZ = False



# settings.py
DATABASE_ROUTERS = ['AIMessageService.db_router.AiMessageRouter']



############### end additional settings ###############




############### Celery Configuration ###############
# Celery settings
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Platform-specific worker configuration for MAXIMUM PARALLEL PROCESSING
if sys.platform == 'win32':
    # Windows - Use eventlet for high concurrency
    CELERY_WORKER_POOL = 'eventlet'
    CELERY_WORKER_CONCURRENCY = 100  # High concurrency for parallel processing
    
    # Windows-specific optimizations
    CELERY_WORKER_HIJACK_ROOT_LOGGER = False
    CELERY_WORKER_DISABLE_RATE_LIMITS = False
    
    print(" Celery configured for Windows - MASSIVE PARALLEL MODE:")
    print(f"   Pool: {CELERY_WORKER_POOL}")
    print(f"   Concurrency: {CELERY_WORKER_CONCURRENCY}")
    print(f"   Target: 50,000 URLs/minute")
else:
    # Linux/Mac - Use prefork for stability with high concurrency
    CELERY_WORKER_POOL = 'prefork'
    CELERY_WORKER_CONCURRENCY = 50  # High concurrency for parallel processing
    
    print(" Celery configured for Linux/Mac - MASSIVE PARALLEL MODE:")
    print(f"   Pool: {CELERY_WORKER_POOL}")
    print(f"   Concurrency: {CELERY_WORKER_CONCURRENCY}")
    print(f"   Target: 50,000 URLs/minute")

# Import Celery configuration for massive parallel processing
from competitorApp.views.cronjob.celery_config import *

# Additional database optimization for high-volume processing
DATABASES['default']['CONN_MAX_AGE'] = 600  # Keep connections alive longer

# Cache optimization for parallel processing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 10000,  # Increase cache size for URL processing
        }
    }
}

# Performance optimizations for massive parallel processing
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Session optimization for parallel requests
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

print(" Database and Cache optimized for parallel processing")

############### end Celery Configuration ###############
