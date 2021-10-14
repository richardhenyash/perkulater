from django.test import TestCase

from django.shortcuts import get_object_or_404
from .models import Category, Product, Size, Type, Price

class TestProductModel(TestCase):

    def test_product_get_short_description(self):
        product = Product.objects.create(
            name="Test Coffee",
            description_short="Test Short Description Line 1;Test Short Description Line 2",
            description_delimiter=";")
        self.assertEqual(product.get_short_description(), "Test Short Description Line 1")

    def test_product_get_description_array(self):
        product = Product.objects.create(
            name="Test Coffee",
            description_full="Test Full Description Paragraph 1;Test Full Description Paragraph 2;Test Full Description Paragraph 3",
            description_delimiter=";")
        self.assertEqual(
            product.get_description_array(), [
                "Test Full Description Paragraph 1",
                "Test Full Description Paragraph 2",
                "Test Full Description Paragraph 3"]
            )


class TestCategoryModel(TestCase):
    def test_category_get_size_information_array(self):
        category = Category.objects.create(
            name="Test Coffee",
            size_information="Test Size Information Line 1;Test Size Information Line 2;Test Size Information Line 3",
            information_delimiter=";")
        self.assertEqual(
            category.get_size_information_array(), [
                "Test Size Information Line 1",
                "Test Size Information Line 2",
                "Test Size Information Line 3"]
            )

    def test_category_get_type_information_array(self):
        category = Category.objects.create(
            name="Test Coffee",
            type_information="Test Type Information Line 1;Test Type Information Line 2;Test Type Information Line 3",
            information_delimiter=";")
        self.assertEqual(
            category.get_type_information_array(), [
                "Test Type Information Line 1",
                "Test Type Information Line 2",
                "Test Type Information Line 3"]
            )

