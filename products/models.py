from django.db import models


class Category(models.Model):
    """
    A model for product categories.
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    A model for products.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, blank=True)
    friendly_price = models.CharField(max_length=100, blank=True)
    description_full = models.TextField(blank=True)
    description_short = models.CharField(max_length=254)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Size(models.Model):
    """
    A model for product sizes.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=254)

    def __str__(self):
        return self.size


class Type(models.Model):
    """
    A model for product types.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=254)

    def __str__(self):
        return self.type


class Price(models.Model):
    """
    A model for product prices.
    """
    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(
        'Size', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.product) + ", " + str(self.size)


class Coffee(models.Model):
    """
    A model for coffees. Contains specific information for coffees
    which is not required on other products.
    """
    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=254, blank=True)
    farm = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=100, blank=True)
    variety = models.CharField(max_length=100, blank=True)
    altitude = models.CharField(max_length=20, blank=True)
    town = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    flavour_profile = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return str(self.product)


class Offer(models.Model):
    """
    A model for current offers.
    """
    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=254, blank=True)
    description_full = models.CharField(max_length=254, blank=True)
    display_in_banner = models.BooleanField(default=False)
    product_multiple = models.IntegerField(null=True, blank=True)
    discount = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    free_delivery_amount = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.description)
