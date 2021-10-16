from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import resolve
from .models import Product

from .test_data import build_test_data


class TestProductViews(TestCase):
    """A class to test product views"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()
        
    def test_resolve_products(self):
        """Test resolving products view"""
        found = resolve('/products/')
        self.assertEqual(found.url_name, "products")

    def test_resolve_product_detail(self):
        """Test resolving product detail view"""
        product = Product.objects.create(
            name="Test Coffee")
        found = resolve(f'/products/{product.id}/')
        self.assertEqual(found.url_name, "product_detail")

    def test_get_all_products(self):
        """Test returning all products view"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_get_product_query(self):
        """Test returning a product query"""
        response = self.client.get('/products/', {'q': 'Coffee'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_get_product_query_blank(self):
        """Test returning a blank product query"""
        response = self.client.get('/products/', {'q': ''})
        self.assertEqual(response.status_code, 302)
    
    def test_get_category(self):
        """Test returning all products in a category"""
        response = self.client.get('/products/', {'q': 'category=Coffee'})
        self.assertEqual(response.status_code, 302)

    def test_get_product_details(self):
        """Test returning product detail view"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/{product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
