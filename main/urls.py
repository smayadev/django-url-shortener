from django.urls import path
from .views import redirect_to_dest, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="main_home"),
    path('<str:src_path>/', redirect_to_dest, name='short_url_redirect'),
]