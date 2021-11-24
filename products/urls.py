"""
Products application url configuration module
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete/<int:product_id>/',
        views.delete_product, name='delete_product'
    ),
    path(
        'edit_prices/<int:product_id>/',
        views.edit_prices, name='edit_prices'
    ),
    path(
        'review_product/<int:product_id>/',
        views.review_product, name='review_product'
    ),
    path(
        'review_product/',
        views.review_product_all,
        name='review_products_all'
    ),
    path(
        'delete_review/<int:product_id>/<int:user_id>/',
        views.delete_review, name='delete_review'
    ),
]
