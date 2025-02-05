from django.urls import path, include
from .views import (
    ShortenURLApiView,
    ResolveURLApiView,
)

urlpatterns = [
    path('shorten/', ShortenURLApiView.as_view(), name="shorten_url"),
    path("resolve/<str:short_code>/", ResolveURLApiView.as_view(), name="resolve_url"),
]