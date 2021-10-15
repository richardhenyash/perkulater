from django.test import TestCase
from .models import Product


class TestProductViews(TestCase):
    """A class to test product views"""

    def test_get_all_products(self):
        """Test returning all products view"""
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 301)

    def test_get_query(self):
        """Test returning a query set of products"""
        response = self.client.get('/products', {'q': 'house'})
        self.assertEqual(response.status_code, 301)

    def test_get_query_blank(self):
        """Test returning a blank query set of products"""
        response = self.client.get('/products', {'q': ''})
        self.assertEqual(response.status_code, 301)

    def test_get_category(self):
        """Test returning all products in a category"""
        response = self.client.get('/products', {'category': 'coffee'})
        print(response.url)
        self.assertEqual(response.status_code, 301)

    def test_get_product_details(self):
        """Test returning product details"""
        product = Product.objects.create(
            name="Test Coffee")
        response = self.client.get(f'/products/{product.id}')
        self.assertEqual(response.status_code, 301)
