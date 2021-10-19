from django.contrib import admin
from.models import Category, Product, Size, Type, Price, Coffee, Offer


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


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(Type)
admin.site.register(Price)
admin.site.register(Coffee)
admin.site.register(Offer)
