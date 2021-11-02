from decimal import Decimal
from django.test import TestCase
from django.shortcuts import get_object_or_404

from checkout.models import Order, OrderLineItem
from products.models import Product, Price, Size, Type

from products.tests.test_data import build_test_data


class TestOrderSignals(TestCase):
    """A class to test the Product signals"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_order_lineitem_updates_order_total(self):
        """
        Test order total is updated correctly
        when  lineitems are added and deleted
        """
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        typeobj2 = get_object_or_404(Type, type="Coarse")
        size = get_object_or_404(Size, size="250g")
        price = get_object_or_404(Price, product=product, size=size)
        order = Order.objects.create(
            full_name="Test Name",
            email="test@gmail.com",
            phone_number="123456789",
            address_1="Test Address 1",
            town_or_city="Town Or City",
            country="GB",
            discount=Decimal(0.0),
            stripe_pid="Test Stripe PID")
        orderlineitem = OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=3)
        self.assertEqual(order.grand_total, 24.75)
        OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj2,
            quantity=3)
        self.assertEqual(order.grand_total, 45.0)
        orderlineitem.delete()
        self.assertEqual(order.grand_total, 24.75)
