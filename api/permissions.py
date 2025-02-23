from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import PathsAPIKey


class HasSystemAPIKey(BaseHasAPIKey):
    """
    Only system keys can access
    """
    model = PathsAPIKey

    def has_permission(self, request, view):
        key = self.get_key(request)
        if not key:
            return False

        api_key = self.model.objects.get_from_key(key)
        return api_key and api_key.is_system


class HasAdminAPIKey(BaseHasAPIKey):
    """
    Only admin keys can access
    """
    model = PathsAPIKey

    def has_permission(self, request, view):
        key = self.get_key(request)
        if not key:
            return False

        api_key = self.model.objects.get_from_key(key)
        return api_key and api_key.is_admin


class HasAnyAPIKey(BaseHasAPIKey):
    """
    All valid API keys can access
    """
    model = PathsAPIKey

    def has_permission(self, request, view):
        key = self.get_key(request)
        if not key:
            return False

        api_key = self.model.objects.get_from_key(key)
        return api_key is not None