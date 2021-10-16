from django.test import TestCase
from django.urls import resolve

from .models import Order
from products.models import Category, Coffee, Offer, Product, Price, Size, Type


class TestCheckoutViews(TestCase):
    """A class to test checkout views"""
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name="Coffee",
            friendly_name="All of our top quality coffees",
            size_description="Size",
            size_information="one 250g packet makes approximately 15 cups of coffee",
            type_description="Grind",
            type_information="whole bean - awesome coffee beans just as they are!;fine - espresso;medium - aeropress, stovetop, drip, V60, chemex;coarse - cafetieres and cold brew",
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
        Type.objects.create(
            category=category,
            type="Whole Bean"
        )
        size = Size.objects.create(
            category=category,
            size="250g")
        Price.objects.create(
            product=product,
            size=size,
            price=7.50,
            sku="TEST SKU")
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
        Offer.objects.create(
            description="Delivery",
            free_delivery_amount=30.00,
            delivery_minimum=2.00,
            delivery_percentage=10.00
        )
        Offer.objects.create(
            description="Test Offer 1",
            description_full="Test Offer 1 Description Full",
            display_in_banner=True
        )
        Offer.objects.create(
            description="Test Offer 2",
            description_full="Test Offer 2 Description Full",
            display_in_banner=True
        )

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
