from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey
from .models import PathsAPIKey

try:
    admin.site.unregister(APIKey)
except admin.sites.NotRegistered:
    pass


@admin.register(PathsAPIKey)
class PathsAPIKeyAdmin(APIKeyModelAdmin):
    list_display = ("name", "prefix", "created", "expiry_date", "is_admin")
    fields = ("name", "revoked", "expiry_date", "is_admin")
    search_fields = ("name", "prefix")

    def get_readonly_fields(self, request, obj=None):
        """
        Prevent editing 'prefix' and 'created' for existing keys.
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ("prefix", "created")
        return readonly_fields