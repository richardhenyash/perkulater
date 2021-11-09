from django.db import models
from django.contrib.auth.models import User


class Basket(models.Model):
    """
    A model for the Basket.
    Allows the basket to be cleared when an order is addded in
    the database by the webhook handler
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    clear_basket = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
