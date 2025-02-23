from rest_framework import serializers
from django.conf import settings
from main.models import Paths


class CaptchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paths
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id', 'question', 'answer']


class PathsSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        """
        Generates the full shortened URL using SITE_URL
        """
        site_url = settings.SITE_URL
        return f"{site_url}/{obj.short_code}"

    class Meta:
        model = Paths
        fields = ['short_code', 'dest_url', 'short_url']
        read_only_fields = ['short_code']