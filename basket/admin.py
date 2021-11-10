from django.contrib import admin
from .models import Basket


class BasketAdmin(admin.ModelAdmin):
    """
    Admin configuration for Basket model
    """
    list_display = (
        'user', 'clear_basket'
    )
    ordering = ['user', 'clear_basket']


# Register your models here.
admin.site.register(Basket, BasketAdmin)
