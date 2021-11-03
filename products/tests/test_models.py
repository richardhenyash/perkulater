from django.shortcuts import get_object_or_404
from django.test import TestCase

from products.models import Category, Coffee, Product, Price, Review, Size

from .test_data import build_test_data


class TestProductModel(TestCase):
    """A class to test the Product model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_product_get_short_description(self):
        """Test get short description method"""
        product = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(
            product.get_short_description(),
            "Test Short Description Line 1"
        )

    def test_product_get_description_array(self):
        """Test get description array method"""
        product = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(
            product.get_description_array(), [
                "Test Full Description Paragraph 1",
                "Test Full Description Paragraph 2",
                "Test Full Description Paragraph 3"]
        )

    def test_product_calculate_rating(self):
        """Test calculate rating method"""
        product = get_object_or_404(Product, name="Test Coffee")
        reviews = Review.objects.filter(product=product)
        self.assertEqual(product.calculate_rating(), 3.0)
        review = reviews[1]
        review.rating = 4.0
        review.save()
        self.assertEqual(product.calculate_rating(), 4.5)
        review.rating = 2.0
        review.save()
        self.assertEqual(product.calculate_rating(), 3.5)


class TestCategoryModel(TestCase):
    """A class to test the Category model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

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
        build_test_data()

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


class TestPriceModel(TestCase):
    """A class to test the Price model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_price_str(self):
        """Test Price string method"""
        product = get_object_or_404(Product, name="Test Coffee")
        size = get_object_or_404(Size, size="250g")
        price = get_object_or_404(Price, product=product, size=size)
        self.assertEqual(str(price), "Test Coffee, 250g")
