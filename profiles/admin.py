from django.contrib import admin

from.models import UserProfile, Reward


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_name', 'full_name',
    )


class RewardAdmin(admin.ModelAdmin):
    list_display = (
        'user_profile', 'date'
    )
    ordering = ['user_profile', 'date']


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reward, RewardAdmin)
