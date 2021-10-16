from django.test import TestCase
from django.urls import resolve

from products.models import Category, Coffee, Offer, Product, Price, Size, Type
from products.test_data import build_test_data

class TestHomeViews(TestCase):
    """A class to test home views"""
    @classmethod
    def setUpTestData(cls):
       build_test_data()

    def test_resolve_home(self):
        """Test resolving home view"""
        found = resolve('/')
        self.assertEqual(found.url_name, "home")

    def test_get_home(self):
        """Test returning home page view"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
