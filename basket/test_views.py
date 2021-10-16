from django.test import TestCase
from django.urls import resolve
from django.shortcuts import get_object_or_404

from products.models import Category, Coffee, Offer, Product, Price, Size, Type


class TestBasketViews(TestCase):
    """A class to test basket views"""
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

    def test_resolve_basket(self):
        """Test resolving basket view"""
        found = resolve('/basket/')
        self.assertEqual(found.url_name, "view_basket")

    def test_resolve_add_to_basket(self):
        """Test resolving add to basket view"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/basket/add/{product.id}/'
        found = resolve(url)
        self.assertEqual(found.url_name, "add_to_basket")

    def test_resolve_adjust_basket(self):
        """Test resolving adjust basket view"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        found = resolve(f'/basket/adjust/{product_key}/')
        self.assertEqual(found.url_name, "adjust_basket")

    def test_resolve_remove_from_basket(self):
        """Test resolving remove from basket view"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        found = resolve(f'/basket/remove/{product_key}/')
        self.assertEqual(found.url_name, "remove_from_basket")

    def test_get_basket(self):
        """Test returning basket view"""
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "basket/basket.html")

    def test_add_to_basket(self):
        """Test add to basket"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/basket/add/{product.id}/'
        form_data = {
            'product-size': "250g",
            'product-type': "Whole Bean",
            'product-quantity': "1",
            'redirect_url': "/products/"
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)

    def test_adjust_basket(self):
        """Test adjust basket"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        url = f'/basket/adjust/{product_key}/'
        form_data = {
            'product-quantity': "2",
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)

    def test_remove_from_basket(self):
        """Test remove from basket"""
        product = get_object_or_404(Product, name="Test Coffee")
        typeobj = get_object_or_404(Type, type="Whole Bean")
        size = get_object_or_404(Size, size="250g")
        product_id = str(product.id)
        size_id = str(size.id)
        type_id = str(typeobj.id)
        product_key = product_id + "_" + size_id + "_" + type_id
        url = f'/basket/add/{product.id}/'
        form_data = {
            'product-size': "250g",
            'product-type': "Whole Bean",
            'product-quantity': "1",
            'redirect_url': "/products/"
        }
        response = self.client.post(url, form_data)
        url = f'/basket/remove/{product_key}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

