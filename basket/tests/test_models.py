"""
Basket application model tests
"""
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from basket.models import Basket

from products.tests.test_data import build_test_data


class TestBasketModel(TestCase):
    """A class to test the Basket model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_basket_str(self):
        """Test basket string method"""
        user = get_object_or_404(User, username="unittestuser")
        basket = Basket.objects.create(
            user=user, clear_basket=True)
        self.assertIsInstance(str(basket), str)
        self.assertEqual(str(basket), user.username)
