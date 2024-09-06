from django.urls import path
from . import views

urlpatterns = [
    path('download/', views.download_logs, name='download_logs'),
    path('filter/', views.filter_logs, name='filter_logs'),
]
