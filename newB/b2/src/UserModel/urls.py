from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .services import ServiceLogin, GetUserToken
from .views import UsersListView

urlpatterns = [
    path('ServiceLogin/', ServiceLogin, name='service_login'),
    path('GetUserToken/', GetUserToken, name='get_user_token'),

    path('UsersList/', UsersListView.as_view(), name='users_list'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)