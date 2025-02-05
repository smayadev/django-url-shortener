import random
import string
from django.db import models
from django.core.validators import URLValidator
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
import redis

# redis_client = redis.StrictRedis.from_url(settings.CACHES["default"]["LOCATION"], decode_responses=True)


class Paths(models.Model):
    src_path = models.CharField(max_length=255, unique=True)
    dest_url = models.CharField(
        max_length=255, 
        validators=[URLValidator(schemes=['http', 'https'])],
        unique=True
    )
    admin_added = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique src_path
        """
        if not self.src_path:
            while True:
                tmp_path = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
                if not Paths.objects.filter(src_path=tmp_path).exists():
                    self.src_path = tmp_path
                    break
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Path'
        verbose_name_plural = 'Paths'

    def __str__(self):
        return self.src_path
    

# @receiver(post_delete, sender=Paths)
# def delete_url_cache_on_delete(sender, instance, **kwargs):
#     """
#     Remove the cached URL path when it is deleted from the db
#     """
#     cache_key = f"url:{instance.src_path}"
#     redis_client.delete(cache_key)
