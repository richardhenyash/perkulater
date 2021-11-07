from django.test import TestCase
from django.shortcuts import get_object_or_404

from products.forms import ProductForm, CoffeeForm, PriceForm, ReviewForm
from products.models import Category, Product, Size

from .test_data import build_test_data


class TestProductForm(TestCase):
    """A class to test the Product form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_name_is_required(self):
        """Test to check name is required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': '',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "£7.50 - 250g",
            'description_full': desc_full,
            'description_short': desc_short,
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')

    def test_friendly_name_is_required(self):
        """Test to check friendly name is required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "",
            'friendly_price': "£7.50 - 250g",
            'description_full': desc_full,
            'description_short': desc_short,
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('friendly_name', form.errors.keys())
        self.assertEqual(
            form.errors['friendly_name'][0], 'This field is required.')

    def test_friendly_price_is_required(self):
        """Test to check friendly price is required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "",
            'description_full': desc_full,
            'description_short': desc_short,
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('friendly_price', form.errors.keys())
        self.assertEqual(
            form.errors['friendly_price'][0], 'This field is required.')

    def test_full_description_is_required(self):
        """Test to check full description is required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "£7.50 - 250g",
            'description_full': "",
            'description_short': desc_short,
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('description_full', form.errors.keys())
        self.assertEqual(
            form.errors['description_full'][0], 'This field is required.')

    def test_short_description_is_required(self):
        """Test to check short description is required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "£7.50 - 250g",
            'description_full': desc_full,
            'description_short': "",
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('description_short', form.errors.keys())
        self.assertEqual(
            form.errors['description_short'][0], 'This field is required.')

    def test_description_delimiter_is_required(self):
        """Test to check description delimiter is required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "£7.50 - 250g",
            'description_full': desc_full,
            'description_short': desc_short,
            'image': "",
            'rating': "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('description_delimiter', form.errors.keys())
        self.assertEqual(
            form.errors['description_delimiter'][0], 'This field is required.')

    def test_image_is_not_required(self):
        """Test to check image is not required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "£7.50 - 250g",
            'description_full': desc_full,
            'description_short': desc_short,
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertTrue(form.is_valid())

    def test_rating_is_not_required(self):
        """Test to check rating is not required"""
        category = get_object_or_404(Category, name="Coffee")
        desc_full = ("Test Full Description Paragraph 1;"
                     "Test Full Description Paragraph 2;"
                     "Test Full Description Paragraph 3")
        desc_short = ("Test Short Description Line 1;"
                      "Test Short Description Line 2")
        form = ProductForm({
            'category': category,
            'name': 'Test New Coffee',
            'friendly_name': "Test New Coffee Friendly Name",
            'friendly_price': "£7.50 - 250g",
            'description_full': desc_full,
            'description_short': desc_short,
            'description_delimiter': ";",
            'image': "",
            'rating': "",
        })
        self.assertTrue(form.is_valid())

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = ProductForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'category', 'name', 'friendly_name',
            'friendly_price', 'description_full',
            'description_short', 'description_delimiter',
            'image'])

    def test_fields_are_explicit_in_form_metaclass(self):
        """Test to check fields are explicit in form metaclass"""
        form = ProductForm()
        self.assertEqual(form.Meta.fields, (
            'category', 'name', 'friendly_name',
            'friendly_price', 'description_full',
            'description_short', 'description_delimiter',
            'image'))


class TestCoffeeForm(TestCase):
    """A class to test the Product form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_country_is_required(self):
        """Test to check country is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': '',
            'farm': 'Test Farm',
            'owner': 'Test Owner',
            'variety': 'Test Variety',
            'altitude': 'Test Altitude',
            'town': 'Test Town',
            'region': 'Test Region',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(form.errors['country'][0], 'This field is required.')

    def test_farm_is_required(self):
        """Test to check farm is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': '',
            'owner': 'Test Owner',
            'variety': 'Test Variety',
            'altitude': 'Test Altitude',
            'town': 'Test Town',
            'region': 'Test Region',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('farm', form.errors.keys())
        self.assertEqual(form.errors['farm'][0], 'This field is required.')

    def test_owner_is_required(self):
        """Test to check owner is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': 'Test Farm',
            'owner': '',
            'variety': 'Test Variety',
            'altitude': 'Test Altitude',
            'town': 'Test Town',
            'region': 'Test Region',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('owner', form.errors.keys())
        self.assertEqual(form.errors['owner'][0], 'This field is required.')

    def test_variety_is_required(self):
        """Test to check variety is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': 'Test Farm',
            'owner': 'Test Owner',
            'variety': '',
            'altitude': 'Test Altitude',
            'town': 'Test Town',
            'region': 'Test Region',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('variety', form.errors.keys())
        self.assertEqual(form.errors['variety'][0], 'This field is required.')

    def test_altitude_is_required(self):
        """Test to check altitude is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': 'Test Farm',
            'owner': 'Test Owner',
            'variety': 'Test Variety',
            'altitude': '',
            'town': 'Test Town',
            'region': 'Test Region',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('altitude', form.errors.keys())
        self.assertEqual(form.errors['altitude'][0], 'This field is required.')

    def test_town_is_required(self):
        """Test to check town is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': 'Test Farm',
            'owner': 'Test Owner',
            'variety': 'Test Variety',
            'altitude': 'Test Altitude',
            'town': '',
            'region': 'Test Region',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('town', form.errors.keys())
        self.assertEqual(form.errors['town'][0], 'This field is required.')

    def test_region_is_required(self):
        """Test to check region is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': 'Test Farm',
            'owner': 'Test Owner',
            'variety': 'Test Variety',
            'altitude': 'Test Altitude',
            'town': 'Test Town',
            'region': '',
            'flavour_profile': 'Test Flavour Profile',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('region', form.errors.keys())
        self.assertEqual(form.errors['region'][0], 'This field is required.')

    def test_flavour_profile_is_required(self):
        """Test to check region is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        form = CoffeeForm({
            'product': product,
            'country': 'Test Country',
            'farm': 'Test Farm',
            'owner': 'Test Owner',
            'variety': 'Test Variety',
            'altitude': 'Test Altitude',
            'town': 'Test Town',
            'region': 'Test Region',
            'flavour_profile': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('flavour_profile', form.errors.keys())
        self.assertEqual(
            form.errors['flavour_profile'][0], 'This field is required.')

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = CoffeeForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'country', 'farm', 'owner',
            'variety', 'altitude',
            'town', 'region',
            'flavour_profile'])

    def test_fields_are_explicit_in_form_metaclass(self):
        """Test to check fields are explicit in form metaclass"""
        form = CoffeeForm()
        self.assertEqual(form.Meta.fields, (
            'country', 'farm', 'owner',
            'variety', 'altitude',
            'town', 'region',
            'flavour_profile'))


class TestPriceForm(TestCase):
    """A class to test the Price form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_price_is_required(self):
        """Test to check price is required"""
        product = get_object_or_404(Product, name="Test Coffee")
        size = Size.objects.filter(category=product.category).first()
        form = PriceForm({
            'size': size,
            'price': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors['price'][0], 'This field is required.')

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = PriceForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'size', 'price'])


class TestReviewForm(TestCase):
    """A class to test the Review form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_rating_is_required(self):
        """Test to check rating is required"""
        form = ReviewForm({
            'rating': '',
            'review': 'Great coffee!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors.keys())
        self.assertEqual(form.errors['rating'][0], 'This field is required.')

    def test_review_is_required(self):
        """Test to check review is required"""
        form = ReviewForm({
            'rating': 5,
            'review': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('review', form.errors.keys())
        self.assertEqual(form.errors['review'][0], 'This field is required.')

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = ReviewForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'rating', 'review'])
