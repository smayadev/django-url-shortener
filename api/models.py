from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

class PathsAPIKey(AbstractAPIKey):
    """
    API Keys for accessing the Paths API.
    The `is_admin` field determines whether the key has full access.
    """
    is_admin = models.BooleanField(default=False)
