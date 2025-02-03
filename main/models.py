from django.db import models
from django.core.validators import URLValidator

class Paths(models.Model):
    src_path = models.CharField(max_length=255, unique=True)
    dest_url = models.CharField(
        max_length=255, 
        validators=[URLValidator(schemes=['http', 'https'])],
        unique=True
    )

    class Meta:
        verbose_name = 'Path'
        verbose_name_plural = 'Paths'

    def __str__(self):
        return self.src_path
