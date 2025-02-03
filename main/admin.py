from django.contrib import admin
from .models import Paths


@admin.register(Paths)
class PathsAdmin(admin.ModelAdmin):
    list_display = ['dest_url', 'src_path', 'admin_added']
    search_fields = ['dest_url', 'src_path']

