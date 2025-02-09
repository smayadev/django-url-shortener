from django.urls import path
from .views import redirect_to_dest, IndexView, get_captcha

urlpatterns = [
    path("", IndexView.as_view(), name="main_home"),
    path('captcha/', get_captcha, name='get_captcha'),
    path('<str:short_code>/', redirect_to_dest, name='redirect_to_dest')
]