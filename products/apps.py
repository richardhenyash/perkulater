from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Products application configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    from django.apps import AppConfig

    def ready(self):
        import products.signals
