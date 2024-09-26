from django.urls import path
from .views import scrape_product

urlpatterns = [
    path('scrape/', scrape_product, name='scrape_product'),
]