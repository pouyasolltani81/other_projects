from django.contrib import admin
from django.urls import path
from django.urls import include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [

    path('swagger-yaml/', SpectacularAPIView.as_view(), name='swagger-yaml'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='swagger-yaml'), name='swagger'),

    path('admin/', admin.site.urls),
    path('User/', include('UserModel.urls')),
    path('TestApp/', include('TestAppModel.urls')),
    path('logs/', include('logmanager.urls')),
]