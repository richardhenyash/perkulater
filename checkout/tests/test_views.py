from django.test import TestCase
from django.urls import resolve
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from checkout.models import Order

from products.tests.test_data import build_test_data
from profiles.models import Reward


class TestCheckoutViews(TestCase):
    """A class to test checkout views"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_resolve_checkout(self):
        """Test resolving checkout view"""
        found = resolve('/checkout/')
        self.assertEqual(found.url_name, "checkout")

    def test_resolve_checkout_success(self):
        """Test resolving checkout success view"""
        order = Order.objects.create(
            full_name="Test Name",
            email="test@gmail.com",
            phone_number="123456789",
            address_1="Test Address 1",
            town_or_city="Town Or City",
            country="GB",
            order_total=7.50,
            delivery_cost=2.00,
            grand_total=9.50,
            stripe_pid="Test Stripe PID",
            )
        found = resolve(f'/checkout/checkout_success/{order.order_number}/')
        self.assertEqual(found.url_name, "checkout_success")

    def test_resolve_wh(self):
        """Test resolving webhook handler view"""
        found = resolve('/checkout/wh/')
        self.assertEqual(found.url_name, "webhook")

    def test_resolve_cache_checkout(self):
        """Test resolving cache checkout data view"""
        found = resolve('/checkout/cache_checkout_data/')
        self.assertEqual(found.url_name, "cache_checkout_data")

    def test_get_checkout(self):
        """Test get checkout view"""
        session = self.client.session
        session["basket"] = {"1_1_1": 1}
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)

    def test_get_checkout_basket_empty(self):
        """Test get checkout view"""
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        redirect_url = '/products/'
        self.assertRedirects(response, redirect_url)

    def test_post_checkout_success(self):
        """Test successful post to checkout view"""
        form_data = {
            'full_name': "Joe Bloggs",
            'email': "joebloggs@gmail.com",
            'phone_number': "123456789",
            'address_1': "Test Address 1",
            'address_2': "Test Address 2",
            'town_or_city': "Town Or City",
            'county': "Test County",
            'postcode': "SE255XX",
            'country': "GB",
            'stripe_pid': "Test Stripe PID",
            'client_secret': (
                "pi_xxxxxxxxxxxxxxxxxxx_secret" +
                "_xxxxxxxxxxxxxxxxxx"),
            'save-info': True,
        }
        session = self.client.session
        session["basket"] = {"1_1_1": 1}
        session.save()
        response = self.client.post('/checkout/', form_data)
        order = get_object_or_404(Order, full_name="Joe Bloggs")
        self.assertEqual(order.full_name, "Joe Bloggs")
        self.assertEqual(order.email, "joebloggs@gmail.com")
        self.assertEqual(order.grand_total, 9.50)
        self.assertEqual(response.status_code, 302)
        redirect_url = f'/checkout/checkout_success/{order.order_number}/'
        self.assertRedirects(response, redirect_url)

    def test_post_checkout_no_discount_applied(self):
        """
        Test no discount is applied at checkout if the user
        does not have an active reward
        """
        # login as Joe Bloggs
        loginresponse = self.client.login(
            username='joebloggs', password='joebloggspassword')
        self.assertTrue(loginresponse)
        # Get user object
        user = get_object_or_404(User, username="joebloggs")
        # Get user reward
        user_reward = Reward.objects.filter(user=user).first()
        # Set user reward discount percentage to 0.0
        user_reward.discount = 0.0
        user_reward.save()
        form_data = {
            'full_name': "Joe Bloggs",
            'email': "joebloggs@gmail.com",
            'phone_number': "123456789",
            'address_1': "Test Address 1",
            'address_2': "Test Address 2",
            'town_or_city': "Town Or City",
            'county': "Test County",
            'postcode': "SE255XX",
            'country': "GB",
            'stripe_pid': "Test Stripe PID",
            'client_secret': (
                "pi_xxxxxxxxxxxxxxxxxxx_secret" +
                "_xxxxxxxxxxxxxxxxxx"),
            'save-info': True,
        }
        session = self.client.session
        session["basket"] = {"1_1_1": 10}
        session.save()
        response = self.client.post('/checkout/', form_data)
        order = get_object_or_404(Order, full_name="Joe Bloggs")
        # Check ourder has been created
        self.assertEqual(order.full_name, "Joe Bloggs")
        self.assertEqual(order.email, "joebloggs@gmail.com")
        # Check no discount has been applied
        self.assertEqual(order.grand_total, 75.00)
        # Check user has been redirected to correct page
        self.assertEqual(response.status_code, 302)
        redirect_url = f'/checkout/checkout_success/{order.order_number}/'
        self.assertRedirects(response, redirect_url)

    def test_post_checkout_discount_applied_and_reward_removed(self):
        """
        Test discount is applied correctly at checkout
        if the user has an active reward
        """
        # login as Joe Bloggs
        loginresponse = self.client.login(
            username='joebloggs', password='joebloggspassword')
        self.assertTrue(loginresponse)
        form_data = {
            'full_name': "Joe Bloggs",
            'email': "joebloggs@gmail.com",
            'phone_number': "123456789",
            'address_1': "Test Address 1",
            'address_2': "Test Address 2",
            'town_or_city': "Town Or City",
            'county': "Test County",
            'postcode': "SE255XX",
            'country': "GB",
            'stripe_pid': "Test Stripe PID",
            'client_secret': (
                "pi_xxxxxxxxxxxxxxxxxxx_secret" +
                "_xxxxxxxxxxxxxxxxxx"),
            'save-info': True,
        }
        session = self.client.session
        session["basket"] = {"1_1_1": 10}
        session.save()
        response = self.client.post('/checkout/', form_data)
        order = get_object_or_404(Order, full_name="Joe Bloggs")
        # Check ourder has been created
        self.assertEqual(order.full_name, "Joe Bloggs")
        self.assertEqual(order.email, "joebloggs@gmail.com")
        # Check discount has been applied
        self.assertEqual(order.grand_total, 67.50)
        # Check user has been redirected to correct page
        self.assertEqual(response.status_code, 302)
        redirect_url = f'/checkout/checkout_success/{order.order_number}/'
        self.assertRedirects(response, redirect_url)
        # Get user object
        user = get_object_or_404(User, username="joebloggs")
        # Get user reward
        user_reward = Reward.objects.filter(user=user).first()
        # Check user reward has been set back to 0 after being used
        self.assertEqual(user_reward.discount, 0.0)

    def test_post_checkout_invalid_form(self):
        """Test post to checkout view with invalid form"""
        form_data = {
            'full_name': "",
            'email': "test@gmail.com",
            'phone_number': "123456789",
            'address_1': "Test Address 1",
            'address_2': "Test Address 2",
            'town_or_city': "Town Or City",
            'county': "Test County",
            'postcode': "SE255XX",
            'country': "GB",
            'stripe_pid': "Test Stripe PID",
            'client_secret': (
                "pi_xxxxxxxxxxxxxxxxxxx_" +
                "secret_xxxxxxxxxxxxxxxxxx"),
            'save-info': True,
        }
        session = self.client.session
        session["basket"] = {"1_1_1": 1}
        session.save()
        response = self.client.post('/checkout/', form_data)
        self.assertEqual(response.status_code, 302)
        redirect_url = '/checkout/'
        self.assertRedirects(response, redirect_url)

    def test_get_checkout_success(self):
        """Test get checkout success view"""
        order = Order.objects.create(
            full_name="Test Name",
            email="test@gmail.com",
            phone_number="123456789",
            address_1="Test Address 1",
            town_or_city="Town Or City",
            country="GB",
            order_total=7.50,
            delivery_cost=2.00,
            grand_total=9.50,
            stripe_pid="Test Stripe PID",
            )
        url = f'/checkout/checkout_success/{order.order_number}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
