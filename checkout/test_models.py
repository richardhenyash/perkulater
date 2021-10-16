from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import Order, OrderLineItem
from products.models import Category, Offer, Product, Price, Size, Type


class TestOrderModel(TestCase):
    """A class to test the Order model"""
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name="Test Coffee")
        category = Category.objects.create(
            name="Coffee"
        )
        Offer.objects.create(
            description="Delivery",
            free_delivery_amount=30.00,
            delivery_minimum=2.00,
            delivery_percentage=10.00
        )
        Type.objects.create(
            category=category,
            type="Whole Bean"
        )
        size= Size.objects.create(
            category=category,
            size="250g")
        Price.objects.create(
            product=product,
            size=size,
            price=7.50,
            sku="TEST SKU")

    def test_order_generate_order_number(self):
        """Test get short description method"""
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


class TestOrderLineItemModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name="Test Coffee")
        category = Category.objects.create(
            name="Coffee"
        )
        Offer.objects.create(
            description="Delivery",
            free_delivery_amount=30.00,
            delivery_minimum=2.00,
            delivery_percentage=10.00
        )
        Type.objects.create(
            category=category,
            type="Whole Bean"
        )
        size= Size.objects.create(
            category=category,
            size="250g")
        Price.objects.create(
            product=product,
            size=size,
            price=7.50,
            sku="TEST SKU")

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
        self.assertEqual(orderlineitem.lineitem_total, 22.5)

    def test_order_lineitem_str(self):
        """Test string method"""
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
        self.assertEqual((str(orderlineitem)), f"SKU TEST SKU on order {order.order_number}")
