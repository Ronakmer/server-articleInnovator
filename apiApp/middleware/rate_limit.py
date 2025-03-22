

########################################## ip band  ##########################################



from django.core.cache import cache
from django.http import JsonResponse
from datetime import datetime, timedelta

class RateLimitMiddleware:
    RATE_LIMIT = 1000  # Max requests allowed
    TIME_WINDOW = 60  # Time window in seconds (1 minute)
    BAN_DURATION = 86400  # 24 hours in seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract correct client IP, even behind proxies
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown')).split(',')[0].strip()

        # Identify user (handle anonymous users)
        user_id = getattr(request.user, "id", "anonymous")
        
        # Define cache keys
        ban_key = f"banned_{user_id}_{ip}"
        rate_key = f"rate_limit_{user_id}_{ip}"

        # Check if user+IP is banned
        if cache.get(ban_key):
            return JsonResponse({'error': 'Your account or IP is banned for 24 hours due to excessive requests.'}, status=403)

        # Get request timestamps within the rate limit window
        request_timestamps = cache.get(rate_key, [])
        now = datetime.now()
        valid_timestamps = [t for t in request_timestamps if (now - t).seconds < self.TIME_WINDOW]

        if len(valid_timestamps) >= self.RATE_LIMIT:
            # Ban user+IP for 24 hours
            cache.set(ban_key, True, timeout=self.BAN_DURATION)
            return JsonResponse({'error': 'Too many requests. You are banned for 24 hours.'}, status=429)

        # Allow request and update timestamps
        valid_timestamps.append(now)
        cache.set(rate_key, valid_timestamps, timeout=self.TIME_WINDOW)

        return self.get_response(request)
