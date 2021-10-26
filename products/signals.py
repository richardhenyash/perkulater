from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Review


@receiver(post_save, sender=Review)
def update_rating_on_add_or_edit(sender, instance, **kwargs):
    """
    Update product rating on add or edit of review
    """
    instance.product.calculate_rating()


@receiver(post_delete, sender=Review)
def update_rating_on_delete(sender, instance, **kwargs):
    """
    Update product rating on delete of review
    """
    if instance.product:
        instance.product.calculate_rating()
