"""
Products application administration module
"""
from django.contrib import admin
from.models import Category, Product, Size, Type, Price, Coffee, Offer, Review


class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model
    """
    list_display = (
        'friendly_name',
        'name',
        'category',
        'rating',
        'image',
        'image_alt',
        'discontinued',
    )

    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model
    """
    list_display = (
        'friendly_name',
        'name',
    )


class PriceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Price model
    """
    list_display = (
        'product',
        'size',
        'sku',
    )
    ordering = ['product', 'size']


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for Review model
    """
    list_display = (
        'user',
        'product',
    )
    ordering = ['user', 'product']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Size)
admin.site.register(Type)
admin.site.register(Coffee)
admin.site.register(Offer)
admin.site.register(Review, ReviewAdmin)
