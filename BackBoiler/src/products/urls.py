from django.urls import path
from . import views

urlpatterns = [
    # path('add/', views.add_product, name='add_product'),
    path('view/', views.view_products, name='view_products'),
    path('add/', views.getthechoice, name='get_the_choice'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),  
    path('delete_all/', views.delete_all_products, name='delete_all_products'),  
]
