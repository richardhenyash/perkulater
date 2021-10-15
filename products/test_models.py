from django.test import TestCase

from .models import Category, Coffee, Product


class TestProductModel(TestCase):
    """A class to test the Product model"""

    def test_product_get_short_description(self):
        """Test get short description method"""
        product = Product.objects.create(
            name="Test Coffee",
            description_short="Test Short Description Line 1;Test Short Description Line 2",
            description_delimiter=";")
        self.assertEqual(product.get_short_description(), "Test Short Description Line 1")

    def test_product_get_description_array(self):
        """Test get description array method"""
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
    """A class to test the Category model"""

    def test_category_get_size_information_array(self):
        """Test get size information array method"""
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
        """Test get type information array method"""
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


class TestCoffeeModel(TestCase):
    """A class to test the Coffee model"""

    def test_get_all_fields(self):
        """Test get all fields method"""
        coffee = Coffee.objects.create(
            country="Country",
            farm="Farm",
            owner="Owner",
            variety="Variety",
            altitude="Altitude",
            town="Town",
            region="Region",
            flavour_profile="Flavour Profile")
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
