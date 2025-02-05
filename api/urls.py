from django.urls import path, include
from .views import (
    ShortenURLApiView,
)

urlpatterns = [
    path('shorten/', ShortenURLApiView.as_view(), name="shorten_url")
]