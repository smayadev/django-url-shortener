from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

class PathsAPIKey(AbstractAPIKey):
    """
    API Keys for accessing the Paths API.
    The is_admin field determines whether the key has full access.
    The is_system field determines whether the key has access to 
    system API endpoints such as captcha.
    """
    is_admin = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)
