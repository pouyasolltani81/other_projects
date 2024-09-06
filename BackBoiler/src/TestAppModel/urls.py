from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .services import Test1, Test2

urlpatterns = [
    path('Test1/', Test1, name='test1'),
    path('Test2/<int:a_data>', Test2, name='test2'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)