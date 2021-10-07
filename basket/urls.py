from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add/<product_id>/', views.add_to_basket, name='add_to_basket'),
    path('adjust/<product_key>/', views.adjust_basket, name='adjust_basket'),
    path('remove/<product_key>/', views.remove_from_basket, name='remove_from_basket'),
]
