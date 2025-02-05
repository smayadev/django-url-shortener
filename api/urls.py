from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PathsViewSet

router = DefaultRouter()
router.register(r'paths', PathsViewSet, basename="paths")

urlpatterns = [
    path("", include(router.urls)),
]
