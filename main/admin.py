from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import Paths


@admin.register(Paths)
class PathsAdmin(admin.ModelAdmin):
    list_display = ['dest_url', 'short_code', 'shortened_url', 'admin_added']
    search_fields = ['dest_url', 'short_code']

    def shortened_url(self, obj):
        """Constructs the full shortened URL dynamically"""
        if settings.SITE_URL.endswith('/'):
            site_url = settings.SITE_URL[:-1]
        else:
            site_url = settings.SITE_URL
        short_url = f'{site_url}/{obj.short_code}'
        return format_html('<a href="{}" target="_blank">{}</a>', short_url, short_url)

    shortened_url.short_description = "Shortened URL"

