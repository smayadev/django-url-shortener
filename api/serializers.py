from rest_framework import serializers
from django.conf import settings
from main.models import Paths


class PathsSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        """
        Generates the full shortened URL using SITE_URL
        """
        site_url = settings.SITE_URL
        return f"{site_url}/{obj.src_path}"

    class Meta:
        model = Paths
        fields = ['src_path', 'dest_url', 'short_url']
        read_only_fields = ['src_path']