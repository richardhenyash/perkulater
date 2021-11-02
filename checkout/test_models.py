from decimal import Decimal
from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import Order, OrderLineItem
from products.models import Product, Price, Size, Type

from products.test_data import build_test_data


class TestOrderModel(TestCase):
    """A class to test the Order model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_order_str(self):
        """Test order string method"""
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
            stripe_pid="Test Stripe PID",)
        self.assertIsInstance(str(order), str)
        self.assertEqual(len(str(order)), 32)

    def test_order_generate_order_number_on_save(self):
        """Test generate order number on save method"""
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
            stripe_pid="Test Stripe PID",)
        self.assertIsInstance(order.order_number, str)
        self.assertEqual(len(order.order_number), 32)

    def test_order_discount_applied(self):
        """Test discount is applied to order"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        price = get_object_or_404(Price, product=product, size=size)
        order = Order.objects.create(
            full_name="Test Name",
            email="test@gmail.com",
            phone_number="123456789",
            address_1="Test Address 1",
            town_or_city="Town Or City",
            country="GB",
            discount=Decimal(7.5),
            stripe_pid="Test Stripe PID",)
        OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=10)
        self.assertEqual(order.grand_total, 67.5)
        self.assertEqual(order.previous_total, 75.0)
        self.assertEqual(order.order_total, 67.5)

    def test_order_no_discount_applied(self):
        """Test no discount is applied to order"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
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
            stripe_pid="Test Stripe PID",)
        OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=10)
        self.assertEqual(order.grand_total, 75.0)
        self.assertEqual(order.previous_total, 75.0)
        self.assertEqual(order.order_total, 75.0)

    def test_order_free_delivery_applied(self):
        """Test free delivery is applied to order"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
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
            stripe_pid="Test Stripe PID",)
        OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=10)
        self.assertEqual(order.grand_total, 75.0)
        self.assertEqual(order.delivery_cost, 0.0)

    def test_order_delivery_minimum_applied(self):
        """Test minimum delivery charge is applied to order"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
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
            stripe_pid="Test Stripe PID",)
        OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=2)
        self.assertEqual(order.grand_total, 17.0)
        self.assertEqual(order.delivery_cost, 2.0)

    def test_order_delivery_percentage_applied(self):
        """Test delivery percentage charge is applied to order"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
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
            stripe_pid="Test Stripe PID",)
        OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=3)
        self.assertEqual(order.grand_total, 24.75)
        self.assertEqual(order.delivery_cost, 2.25)


class TestOrderLineItemModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_order_lineitem_total(self):
        """Test lineitem_total method"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
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
        self.assertEqual(orderlineitem.lineitem_total, 22.5)

    def test_order_lineitem_str(self):
        """Test order lineitem string method"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        price = get_object_or_404(Price, product=product, size=size)
        order = Order.objects.create(
            full_name="Test Name",
            email="test@gmail.com",
            phone_number="123456789",
            address_1="Test Address 1",
            town_or_city="Town Or City",
            country="GB",
            order_total=22.50,
            delivery_cost=2.00,
            grand_total=27.50,
            stripe_pid="Test Stripe PID")
        orderlineitem = OrderLineItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            type=typeobj,
            quantity=3)
        self.assertEqual(
            (str(orderlineitem)),
            f"SKU TEST SKU on order {order.order_number}")
