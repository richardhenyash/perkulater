from django.shortcuts import get_object_or_404
from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import resolve

from .models import UserProfile, Reward
from checkout.models import Order

from products.test_data import build_test_data


class TestProfileViews(TestCase):
    """A class to test profiles views"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()
        
    def test_resolve_profile(self):
        """Test resolving profile view"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        found = resolve('/profile/')
        self.assertEqual(found.url_name, "profile")

    def test_resolve_order_history(self):
        """Test resolving order history view"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        # Get user object
        user = get_object_or_404(User, username="unittestuser")
        # Get user profile object
        user_profile = get_object_or_404(UserProfile, user=user)
        # Get order object
        order = Order.objects.get(user_profile=user_profile)
        url = f'/profile/order_history/{order.order_number}/'
        found = resolve(url)
        self.assertEqual(found.url_name, "order_history")
    
    def test_resolve_order_contact(self):
        """Test resolving order contact view"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        # Get user object
        user = get_object_or_404(User, username="unittestuser")
        # Get user profile object
        user_profile = get_object_or_404(UserProfile, user=user)
        # Get order object
        order = Order.objects.get(user_profile=user_profile)
        url = f'/profile/contact/{order.order_number}/'
        found = resolve(url)
        self.assertEqual(found.url_name, "order_contact")

    def test_get_profile(self):
        """Test returning profile view"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_post_edit_profile(self):
        """Test editing a profile"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        response = self.client.post(
            '/profile/', {
                'phone_number': '123456789',
                'address_1': 'Test Street Address 1',
                'address_2': 'Test Street Address 2',
                'town_or_city': 'Test Town',
                'county': 'Test County',
                'postcode': 'SE255XX',
                'country': "GB"})

        # Get user pbject
        user = get_object_or_404(User, username="unittestuser")
        # Get user profile object
        user_profile = get_object_or_404(UserProfile, user=user)
        # Perform tests
        self.assertEqual(user_profile.phone_number, '123456789')
        self.assertEqual(user_profile.address_1, 'Test Street Address 1')
        self.assertEqual(user_profile.address_2, 'Test Street Address 2')
        self.assertEqual(user_profile.town_or_city, 'Test Town')
        self.assertEqual(user_profile.county, 'Test County')
        self.assertEqual(user_profile.postcode, 'SE255XX')
        self.assertEqual(user_profile.country, 'GB')
        self.assertEqual(response.status_code, 200)

    def test_get_order_history(self):
        """Test returning order history view"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        # Get user object
        user = get_object_or_404(User, username="unittestuser")
        # Get user profile object
        user_profile = get_object_or_404(UserProfile, user=user)
        # Get order object
        order = Order.objects.get(user_profile=user_profile)
        url = f'/profile/order_history/{order.order_number}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
    
    def test_get_order_contact(self):
        """Test returning order contact view"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        # Get user object
        user = get_object_or_404(User, username="unittestuser")
        # Get user profile object
        user_profile = get_object_or_404(UserProfile, user=user)
        # Get order object
        order = Order.objects.get(user_profile=user_profile)
        url = f'/profile/contact/{order.order_number}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/order_contact.html')

    def test_post_order_contact(self):
        """Test submitting order contact form"""
        # login as test user
        loginresponse = self.client.login(username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        # Get user object
        user = get_object_or_404(User, username="unittestuser")
        # Get user profile object
        user_profile = get_object_or_404(UserProfile, user=user)
        # Get order object
        order = Order.objects.get(user_profile=user_profile)
        url = f'/profile/contact/{order.order_number}/'
        response = self.client.post(
            url, {'message': 'Test order contact message'})
        message = list(response.context.get('messages'))[0]
        self.assertTrue("Order contact email sent succesfully" in message.message)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/order_contact.html')
