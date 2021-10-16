from django.shortcuts import get_object_or_404
from django.test import TestCase

from .models import Category, Coffee, Product


class TestProductModel(TestCase):
    """A class to test the Product model"""
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name="Coffee",
            friendly_name="All of our top quality coffees",
            size_description="Size",
            size_information="Test Size Information Line 1;Test Size Information Line 2;Test Size Information Line 3",
            type_description="Grind",
            type_information="Test Type Information Line 1;Test Type Information Line 2;Test Type Information Line 3",
            information_delimiter=";"
        )
        product = Product.objects.create(
            category=category,
            name="Test Coffee",
            friendly_name="Test Coffee Friendly Name",
            friendly_price="£7.50 - 250g",
            description_full="Test Full Description Paragraph 1;Test Full Description Paragraph 2;Test Full Description Paragraph 3",
            description_short="Test Short Description Line 1;Test Short Description Line 2",
            description_delimiter=";",
            rating=4.50,
            image_url="jump-leads-front-transparent.png",
            image="jump-leads-front-transparent.png",
        )

    def test_product_get_short_description(self):
        """Test get short description method"""
        product = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(product.get_short_description(), "Test Short Description Line 1")

    def test_product_get_description_array(self):
        """Test get description array method"""
        product = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(
            product.get_description_array(), [
                "Test Full Description Paragraph 1",
                "Test Full Description Paragraph 2",
                "Test Full Description Paragraph 3"]
            )


class TestCategoryModel(TestCase):
    """A class to test the Category model"""
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(
            name="Coffee",
            friendly_name="All of our top quality coffees",
            size_description="Size",
            size_information="Test Size Information Line 1;Test Size Information Line 2;Test Size Information Line 3",
            type_description="Grind",
            type_information="Test Type Information Line 1;Test Type Information Line 2;Test Type Information Line 3",
            information_delimiter=";"
        )

    def test_category_get_size_information_array(self):
        """Test get size information array method"""
        category = get_object_or_404(Category, name="Coffee")
        self.assertEqual(
            category.get_size_information_array(), [
                "Test Size Information Line 1",
                "Test Size Information Line 2",
                "Test Size Information Line 3"]
            )

    def test_category_get_type_information_array(self):
        """Test get type information array method"""
        category = get_object_or_404(Category, name="Coffee")
        self.assertEqual(
            category.get_type_information_array(), [
                "Test Type Information Line 1",
                "Test Type Information Line 2",
                "Test Type Information Line 3"]
            )


class TestCoffeeModel(TestCase):
    """A class to test the Coffee model"""
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name="Coffee",
            friendly_name="All of our top quality coffees",
            size_description="Size",
            size_information="Test Size Information Line 1;Test Size Information Line 2;Test Size Information Line 3",
            type_description="Grind",
            type_information="Test Type Information Line 1;Test Type Information Line 2;Test Type Information Line 3",
            information_delimiter=";"
        )
        product = Product.objects.create(
            category=category,
            name="Test Coffee",
            friendly_name="Test Coffee Friendly Name",
            friendly_price="£7.50 - 250g",
            description_full="Test Full Description Paragraph 1;Test Full Description Paragraph 2;Test Full Description Paragraph 3",
            description_short="Test Short Description Line 1;Test Short Description Line 2",
            description_delimiter=";",
            rating=4.50,
            image_url="jump-leads-front-transparent.png",
            image="jump-leads-front-transparent.png",
        )
        Coffee.objects.create(
            product=product,
            country="Test Country",
            farm="Test Farm",
            owner="Test Owner",
            variety="Test Variety",
            altitude="Test Variety",
            town="Test Town",
            region="Test Region",
            flavour_profile="Test Flavour Profile"
        )

    def test_get_all_fields(self):
        """Test get all fields method"""
        product = get_object_or_404(Product, name="Test Coffee")
        coffee = get_object_or_404(Coffee, product=product)
        self.assertEqual(
            coffee.get_all_fields(), [
                "product",
                "country",
                "farm",
                "owner",
                "variety",
                "altitude",
                "town",
                "region",
                "flavour_profile"
                ]
            )
