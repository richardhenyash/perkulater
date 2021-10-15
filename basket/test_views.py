from django.test import TestCase
from django.urls import resolve

from products.models import Category, Product, Size, Type


class TestBasketViews(TestCase):
    """A class to test basket views"""

    def test_resolve_basket(self):
        """Test resolving basket view"""
        found = resolve('/basket/')
        self.assertEqual(found.url_name, "view_basket")

    def test_add_to_basket(self):
        """Test resolving add to basket view"""
        product = Product.objects.create(
            name="Test Coffee")
        found = resolve(f'/basket/add/{product.id}/')
        self.assertEqual(found.url_name, "add_to_basket")

    def test_adjust_basket(self):
        """Test resolving adjust basket view"""
        product = Product.objects.create(
            name="Test Coffee"
        )
        category = Category.objects.create(
            name="Coffee"
        )
        type = Type.objects.create(
            category=category,
            type="Whole Bean"
        )
        size = Size.objects.create(
            category=category,
            size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(type.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        found = resolve(f'/basket/adjust/{product_key}/')
        self.assertEqual(found.url_name, "adjust_basket")

    def test_remove_from_basket(self):
        """Test resolving remove from basket view"""
        product = Product.objects.create(
            name="Test Coffee"
        )
        category = Category.objects.create(
            name="Coffee"
        )
        type = Type.objects.create(
            category=category,
            type="Whole Bean"
        )
        size = Size.objects.create(
            category=category,
            size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(type.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        found = resolve(f'/basket/remove/{product_key}/')
        self.assertEqual(found.url_name, "remove_from_basket")
