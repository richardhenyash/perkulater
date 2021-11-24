"""
Profiles application administration module
"""
from django.contrib import admin

from.models import UserProfile, Reward


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model
    """
    list_display = (
        'user_name', 'full_name',
    )


class RewardAdmin(admin.ModelAdmin):
    """
    Admin configuration for Reward model
    """
    list_display = (
        'user', 'date'
    )
    ordering = ['user', 'date']


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reward, RewardAdmin)
