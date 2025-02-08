import random
import string
from django.db import models
from django.core.validators import URLValidator
from api.models import PathsAPIKey


class Paths(models.Model):
    short_code = models.CharField(max_length=255, unique=True)
    dest_url = models.CharField(
        max_length=255, 
        validators=[URLValidator(schemes=['http', 'https'])]
    )
    admin_added = models.BooleanField(default=False)
    api_key = models.ForeignKey(
        PathsAPIKey, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique short_code
        """
        if not self.short_code:
            while True:
                tmp_code = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
                if not Paths.objects.filter(short_code=tmp_code).exists():
                    self.short_code = tmp_code
                    break
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Path'
        verbose_name_plural = 'Paths'

    def __str__(self):
        return self.short_code
