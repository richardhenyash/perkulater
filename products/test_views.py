from django.test import TestCase
from .models import Product

# Create your tests here.


class TestProductViews(TestCase):

    def test_get_all_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/templates/products.html')

    def test_get_product_details(self):
        product = Product.objects.create(
            name="Test Coffee")
        response = self.client.get(f'/products/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/templates/product_detail.html')
