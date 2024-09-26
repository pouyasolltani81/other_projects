from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .services import GetLogs
from .views import ShowLogs

urlpatterns = [
    path('GetLogs/', GetLogs, name='get_logs'),

    path('ShowLogs/', ShowLogs, name='show_logs'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)