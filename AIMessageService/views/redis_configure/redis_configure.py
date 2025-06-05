

# # import json
# # from django.http import JsonResponse
# # from rest_framework.decorators import api_view
# # from django.conf import settings
# # import redis

# # # Redis connection (configure your host/port/db in settings.py)
# # redis_client = redis.StrictRedis(
# #     # host=getattr(settings, 'REDIS_HOST', 'localhost'),
# #     host=getattr(settings, 'REDIS_HOST', '127.0.0.1'),
# #     port=getattr(settings, 'REDIS_PORT', 6379),
# #     db=getattr(settings, 'REDIS_DB', 2),
# #     decode_responses=True
# # )

# # def redis_key(article_id, message_id):
# #     return f"article:{article_id}:message:{message_id}"




# import redis
# from django.conf import settings

# # redis_client = redis.StrictRedis(
# #     host=settings.REDIS_HOST,
# #     port=settings.REDIS_PORT,
# #     db=settings.REDIS_DB,
# #     decode_responses=True
# # )


# # Try different connection methods
# redis_client = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
#     decode_responses=True

# )

# # # Or with connection pooling
# # redis_client = redis.ConnectionPool(
# #     host=settings.REDIS_HOST,
# #     port=settings.REDIS_PORT,
# #     db=settings.REDIS_DB,
# #     decode_responses=True
# # )


# def redis_key(article_id, message_id):
#     return f"article:{article_id}:message:{message_id}"



