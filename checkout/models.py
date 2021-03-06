"""
Checkout application model configuration module
"""
import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField
from django.shortcuts import get_object_or_404
from products.models import Offer, Price, Product, Size, Type
from profiles.models import UserProfile


class Order(models.Model):
    """
    A model for recording order information
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    address_1 = models.CharField(max_length=80, null=False, blank=False)
    address_2 = models.CharField(max_length=80, blank=True, default="")
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, blank=True, default="")
    postcode = models.CharField(max_length=20, blank=True, default="")
    country = CountryField(blank_label='Country *', null=False, blank=False)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    previous_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_basket = models.TextField(blank=True, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update the grand total each time a line item is added,
        including discount and delivery cost
        """
        # Get Delvery Offer
        offer = get_object_or_404(Offer, description="Delivery")
        # Set free delivery amount
        free_delivery_amount = offer.get_free_delivery_amount()
        # Set delivery percentage
        delivery_percentage = offer.get_delivery_percentage()
        # Set delivery minimum charge
        delivery_minimum = offer.get_delivery_minimum()
        # Aggregate line items to calculate order total
        order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        order_total = round(Decimal(order_total), 2)
        # Apply discount if set and calculate final order total
        if self.discount > 0 and order_total > 0:
            self.previous_total = order_total
            self.order_total = order_total - self.discount
        else:
            self.previous_total = order_total
            self.order_total = order_total
        # Calculate delivery cost
        if order_total < free_delivery_amount:
            delivery = order_total * (Decimal(delivery_percentage / 100))
            if delivery < delivery_minimum:
                self.delivery_cost = delivery_minimum
            else:
                self.delivery_cost = round(delivery, 2)
        else:
            self.delivery_cost = round(Decimal(0.0), 2)
        # Set grand total
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override save method to set the order number, if required
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    A model for recording order information for each order line item
    """
    order = models.ForeignKey(
        Order, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    price = models.ForeignKey(
        Price, null=False, blank=False, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size, null=False, blank=False, on_delete=models.CASCADE)
    type = models.ForeignKey(
        Type, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override save method to calculate and set the lineitem total
        and update the order total
        """
        self.lineitem_total = self.price.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.price.sku} on order {self.order.order_number}'
