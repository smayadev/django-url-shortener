from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PathsViewSet, 
    ShortenURLViewSet, 
    ResolveURLViewSet, 
    StatsViewSet,
    GetCaptchaQuestionViewSet
)

router = DefaultRouter()
router.register(r'paths', PathsViewSet, basename="paths")
router.register(r'shorten', ShortenURLViewSet, basename="shorten")
router.register(r'resolve', ResolveURLViewSet, basename="resolve")
router.register(r'stats', StatsViewSet, basename="stats")
router.register(r'captcha', GetCaptchaQuestionViewSet, basename="captcha")

urlpatterns = [
    path("", include(router.urls)),
]
