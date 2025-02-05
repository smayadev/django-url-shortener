from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import redis
from .models import Paths

redis_client = redis.StrictRedis.from_url(settings.CACHES["default"]["LOCATION"], decode_responses=True)

@receiver(post_delete, sender=Paths)
def delete_url_cache_on_delete(sender, instance, **kwargs):
    """
    Remove the cached URL path when deleted
    """
    try:
        cache_key = f"url:{instance.short_code}"    
        redis_client.delete(cache_key)
    except (redis.ConnectionError, redis.TimeoutError):
        print('redis connection failed when deleting shortened URL') 
