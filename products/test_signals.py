from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Product, Review

from .test_data import build_test_data


class TestProductSignals(TestCase):
    """A class to test the Product signals"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_update_rating_on_review_edit(self):
        """"Test product update rating signal on review edit"""
        product = get_object_or_404(Product, name="Test Coffee")
        reviews = Review.objects.filter(product=product)
        self.assertEqual(product.rating, 3.0)
        review = reviews[1]
        review.rating = 4.0
        review.save()
        self.assertEqual(product.rating, 3.0)
        review.rating = 2.0
        review.save()
        self.assertEqual(product.rating, 3.0)

    def test_update_rating_on_review_add(self):
        """Test product update rating signal on review add"""
        # Create new standard user for unit tests
        user2 = User.objects.create_user(
            'unittestuser2', 'unittestuser2@test.com', 'unittestuser2password')
        # Check product rating prior to adding review
        product = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(product.rating, 3.0)
        newreview = Review(
            product=product, user=user2, rating=5.0, review="Great coffee!")
        newreview.save()
        productupdated = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(round(float(productupdated.rating), 2), 3.67)

    def test_update_rating_on_review_delete(self):
        """Test product update rating signal on review add"""
        # Check product rating prior to deleting review
        product = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(product.rating, 3.0)
        review = Review.objects.filter(product=product).first()
        review.delete()
        productupdated = get_object_or_404(Product, name="Test Coffee")
        self.assertEqual(round(float(productupdated.rating), 2), 1.00)
