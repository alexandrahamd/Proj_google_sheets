from django.urls import path
from app.apps import AppConfig
from app.views import AppView

app_name = AppConfig.name

urlpatterns = [
    path('', AppView.as_view(), name='app'),
]