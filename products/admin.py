from django.contrib import admin
from.models import Category, Product, Size, Type, Price, Coffee, Offer, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'category',
        'rating',
        'image',
    )

    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'size',
        'sku',
    )
    ordering = ['product', 'size']


class ReviewAdmin(admin.ModelAdmin):
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
