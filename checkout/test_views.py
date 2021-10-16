from django.test import TestCase
from django.urls import resolve

from .models import Order

from products.test_data import build_test_data


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
        found = resolve(f'/checkout/checkout_success/{order.order_number}')
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

    def test_post_checkout(self):
        """Test post to checkout view"""
        form_data = {
            'full_name': "Test Name",
            'email': "test@gmail.com",
            'phone_number': "123456789",
            'address_1': "Test Address 1",
            'address_2': "Test Address 2",
            'town_or_city': "Town Or City",
            'county': "Test County",
            'postcode': "SE255XX",
            'country': "GB",
            'order_total': 7.50,
            'delivery_cost': 2.00,
            'grand_total': 9.50,
            'stripe_pid': "Test Stripe PID",
            'client_secret': "pi_xxxxxxxxxxxxxxxxxxx_secret_xxxxxxxxxxxxxxxxxx",
            'save-info': True,
        }
        session = self.client.session
        session["basket"] = {"1_1_1": 1}
        session.save()
        response = self.client.post('/checkout/', form_data)
        self.assertEqual(response.status_code, 302)

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
            'order_total': 7.50,
            'delivery_cost': 2.00,
            'grand_total': 9.50,
            'stripe_pid': "Test Stripe PID",
            'client_secret': "pi_xxxxxxxxxxxxxxxxxxx_secret_xxxxxxxxxxxxxxxxxx",
            'save-info': True,
        }
        session = self.client.session
        session["basket"] = {"1_1_1": 1}
        session.save()
        response = self.client.post('/checkout/', form_data)
        self.assertEqual(response.status_code, 302)

    def test_get_checkout(self):
        """Test get checkout view"""
        session = self.client.session
        session["basket"] = {"1_1_1": 1}
        session.save()
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
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")

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
        url = f'/checkout/checkout_success/{order.order_number}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
