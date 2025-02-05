from django.urls import path
from .views import redirect_to_dest, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="main_home"),
    path('<str:short_code>/', redirect_to_dest, name='redirect_to_dest'),
]