"""
Profiles application model configuration module
"""
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for storing and updating
    default delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    address_1 = models.CharField(max_length=80, blank=True, default="")
    address_2 = models.CharField(max_length=80, blank=True, default="")
    postcode = models.CharField(max_length=20, blank=True, default="")
    town_or_city = models.CharField(max_length=40, blank=True, default="")
    county = models.CharField(max_length=80, blank=True, default="")
    country = CountryField(blank_label='Country', null=True, blank=True)

    def __str__(self):
        """
        Return username of linked user
        """
        return self.user.username

    @admin.display(description='Full Name')
    def full_name(self):
        """
        Display full name of linked user
        """
        return self.user.get_full_name()

    @admin.display(description='username')
    def user_name(self):
        """
        Display username of linked user
        """
        return self.user.username


class Reward(models.Model):
    """
    A model for User Rewards
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, default=0.0)
    free_delivery = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return username of linked user
        """
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    # If user is new
    if created:
        # Create UserProfile
        UserProfile.objects.create(user=instance)
    # Save UserProfile
    instance.userprofile.save()
