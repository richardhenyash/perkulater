from django.test import TestCase
from django.urls import resolve
from django.shortcuts import get_object_or_404

from products.models import Product, Size, Type

from products.test_data import build_test_data


class TestBasketViews(TestCase):
    """A class to test basket views"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_resolve_basket(self):
        """Test resolving basket view"""
        found = resolve('/basket/')
        self.assertEqual(found.url_name, "view_basket")

    def test_resolve_add_to_basket(self):
        """Test resolving add to basket view"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/basket/add/{product.id}/'
        found = resolve(url)
        self.assertEqual(found.url_name, "add_to_basket")

    def test_resolve_adjust_basket(self):
        """Test resolving adjust basket view"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        found = resolve(f'/basket/adjust/{product_key}/')
        self.assertEqual(found.url_name, "adjust_basket")

    def test_resolve_remove_from_basket(self):
        """Test resolving remove from basket view"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        found = resolve(f'/basket/remove/{product_key}/')
        self.assertEqual(found.url_name, "remove_from_basket")

    def test_get_basket(self):
        """Test returning basket view"""
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "basket/basket.html")

    def test_add_to_basket(self):
        """Test add to basket"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/basket/add/{product.id}/'
        form_data = {
            'product-size': "250g",
            'product-type': "Whole Bean",
            'product-quantity': "1",
            'redirect_url': "/products/"
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)

    def test_adjust_basket(self):
        """Test adjust basket"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        url = f'/basket/adjust/{product_key}/'
        form_data = {
            'product-quantity': "2",
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)

    def test_remove_from_basket(self):
        """Test remove from basket"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        url = f'/basket/add/{product.id}/'
        form_data = {
            'product-size': "250g",
            'product-type': "Whole Bean",
            'product-quantity': "1",
            'redirect_url': "/products/"
        }
        response = self.client.post(url, form_data)
        url = f'/basket/remove/{product_key}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
