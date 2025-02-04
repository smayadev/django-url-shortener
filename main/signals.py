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
    cache_key = f"url:{instance.src_path}"    
    redis_client.delete(cache_key)
