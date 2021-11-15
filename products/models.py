from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg


class Category(models.Model):
    """
    A model for product categories.
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254, null=False, blank=False)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    description = models.CharField(max_length=254, null=False, blank=False)
    size_description = models.CharField(max_length=50, blank=True)
    size_information = models.CharField(max_length=254, blank=True)
    type_description = models.CharField(max_length=50, blank=True)
    type_information = models.CharField(max_length=254, blank=True)
    information_delimiter = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.name

    def get_description(self):
        return self.description

    def get_friendly_name(self):
        return self.friendly_name

    def get_size_information_array(self):
        delim = self.information_delimiter
        return self.size_information.split(delim)

    def get_type_information_array(self):
        delim = self.information_delimiter
        return self.type_information.split(delim)


class Product(models.Model):
    """
    A model for products.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254, null=False, blank=False)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    friendly_price = models.CharField(
        max_length=100, null=False, blank=False, default="£7.50 - 250g")
    description_full = models.TextField(
        null=False, blank=False)
    description_short = models.CharField(
        max_length=254, null=False, blank=False)
    description_delimiter = models.CharField(
        max_length=3, null=False, blank=False, default=";")
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_alt = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    def get_short_description(self):
        """
        Return the first item of the short description
        split with the delimiter
        """
        delim = self.description_delimiter
        return self.description_short.split(delim)[0]

    def get_description_array(self):
        """
        Return an array of the full description
        split with the delimiter
        """
        delim = self.description_delimiter
        return self.description_full.split(delim)

    def calculate_rating(self):
        """
        Calculate the average product rating
        from all related reviews
        """
        self.rating = self.reviews.all().aggregate(Avg("rating"))[
            'rating__avg']
        self.save()
        return self.rating


class Size(models.Model):
    """
    A model for product sizes.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=254, null=False, blank=False)
    default_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.size

    def get_default_price(self):
        return self.default_price


class Type(models.Model):
    """
    A model for product types.
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=254, null=False, blank=False)

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
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False)
    sku = models.CharField(blank=True, default="", max_length=254)

    def __str__(self):
        return str(self.product) + ", " + str(self.size)

    def get_product(self):
        return str(self.product)

    def get_size(self):
        return str(self.size)

    def get_price(self):
        return (self.price)

    def get_sku(self):
        return (self.sku)


class Coffee(models.Model):
    """
    A model for coffees. Contains specific information for coffees
    which is not required on other products.
    """
    product = models.ForeignKey(
        'Product', null=True, blank=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=254, null=False, blank=False)
    farm = models.CharField(max_length=100, null=False, blank=False)
    owner = models.CharField(max_length=100, null=False, blank=False)
    variety = models.CharField(max_length=100, null=False, blank=False)
    altitude = models.CharField(max_length=20, null=False, blank=False)
    town = models.CharField(max_length=100, null=False, blank=False)
    region = models.CharField(max_length=100, null=False, blank=False)
    flavour_profile = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        return str(self.product)

    def get_all_fields(self):
        """
        Returns a list of all field names apart from id on the instance.
        """
        fields = []
        for field in self._meta.fields:
            if field.name != "id":
                fields.append(field.name)
        return fields


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
    delivery_minimum = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    delivery_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.description)

    def get_free_delivery_amount(self):
        return self.free_delivery_amount

    def get_delivery_percentage(self):
        return self.delivery_percentage

    def get_delivery_minimum(self):
        return self.delivery_minimum


class Review(models.Model):
    """
    A model for product reviews.
    """
    product = models.ForeignKey(
        'Product', null=True, blank=True,
        related_name='reviews', on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ", " + str(self.product)
