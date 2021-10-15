from django.test import TestCase
from django.urls import resolve
from .models import Order


class TestCheckoutViews(TestCase):
    """A class to test checkout views"""

    def test_resolve_checkout(self):
        """Test resolving checkout view"""
        found = resolve('/checkout/')
        self.assertEqual(found.url_name, "checkout")

    def test_resolve_checkout_success(self):
        """Test resolving checkout success view"""
        order = Order.objects.create(
            full_name="Test Name",
            email="test@gmail.com",
            phone_number="123456789",
            address_1="Test Address 1",
            town_or_city="Town Or City",
            country="GB",
            order_total=7.50,
            delivery_cost=2.00,
            grand_total=9.50,
            stripe_pid="Test Stripe PID",
            )
        found = resolve(f'/checkout/checkout_success/{order.order_number}')
        self.assertEqual(found.url_name, "checkout_success")

    def test_resolve_wh(self):
        """Test resolving webhook handler view"""
        found = resolve('/checkout/wh/')
        self.assertEqual(found.url_name, "webhook")

    def test_resolve_cache_checkout(self):
        """Test resolving cache checkout data view"""
        found = resolve('/checkout/cache_checkout_data/')
        self.assertEqual(found.url_name, "cache_checkout_data")

