from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import resolve
from .models import Category, Coffee, Offer, Price, Product, Size, Type


class TestProductViews(TestCase):
    """A class to test product views"""
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

    def test_resolve_products(self):
        """Test resolving products view"""
        found = resolve('/products/')
        self.assertEqual(found.url_name, "products")

    def test_resolve_product_detail(self):
        """Test resolving product detail view"""
        product = Product.objects.create(
            name="Test Coffee")
        found = resolve(f'/products/{product.id}/')
        self.assertEqual(found.url_name, "product_detail")

    def test_get_all_products(self):
        """Test returning all products view"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_get_product_query(self):
        """Test returning a product query"""
        response = self.client.get('/products/', {'q': 'Coffee'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")

    def test_get_product_query_blank(self):
        """Test returning a blank product query"""
        response = self.client.get('/products/', {'q': ''})
        self.assertEqual(response.status_code, 302)
    
    def test_get_category(self):
        """Test returning all products in a category"""
        response = self.client.get('/products/', {'q': 'category=Coffee'})
        self.assertEqual(response.status_code, 302)

    def test_get_product_details(self):
        """Test returning product detail view"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/{product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
