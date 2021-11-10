from django.apps import AppConfig


class BasketConfig(AppConfig):
    """
    Basket application configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket'
