from django.test import TestCase

from checkout.forms import OrderForm


class TestOrderForm(TestCase):
    """A class to test the Order form"""

    def test_full_name_is_required(self):
        """Test to check full name is required"""
        form = OrderForm({
            'full_name': '',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': 'GB'
            })
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(
            form.errors['full_name'][0], 'This field is required.')

    def test_email_is_required(self):
        """Test to check email is required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': '',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': 'GB'
            })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(
            form.errors['email'][0], 'This field is required.')

    def test_phone_number_is_required(self):
        """Test to check phone number is required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': 'GB'
            })
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors.keys())
        self.assertEqual(
            form.errors['phone_number'][0], 'This field is required.')

    def test_address_1_is_required(self):
        """Test to check address 1 is required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '',
            'town_or_city': 'Somewhere',
            'country': 'GB'
            })
        self.assertFalse(form.is_valid())
        self.assertIn('address_1', form.errors.keys())
        self.assertEqual(
            form.errors['address_1'][0], 'This field is required.')

    def test_town_or_city_is_required(self):
        """Test to check town or city is required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': '',
            'country': 'GB'
            })
        self.assertFalse(form.is_valid())
        self.assertIn('town_or_city', form.errors.keys())
        self.assertEqual(
            form.errors['town_or_city'][0], 'This field is required.')

    def test_country_is_required(self):
        """Test to check country is required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': ''
            })
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(
            form.errors['country'][0], 'This field is required.')

    def address_2_is_not_required(self):
        """Test to check address 2 is not required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': ''
            })
        self.assertTrue(form.is_valid())

    def county_is_not_required(self):
        """Test to check county is not required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': ''
            })
        self.assertTrue(form.is_valid())

    def postcode_is_not_required(self):
        """Test to check postcode is not required"""
        form = OrderForm({
            'full_name': 'Mr User',
            'email': 'test@gmail.com',
            'phone_number': '+442080000000',
            'address_1': '22 Acacia Road',
            'town_or_city': 'Somewhere',
            'country': ''
            })
        self.assertTrue(form.is_valid())

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = OrderForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'full_name', 'email',
            'phone_number',
            'address_1', 'address_2',
            'town_or_city', 'county',
            'postcode', 'country'])

    def test_fields_are_explicit_in_form_metaclass(self):
        """Test to check fields are explicit in form metaclass"""
        form = OrderForm()
        self.assertEqual(form.Meta.fields, (
            'full_name', 'email',
            'phone_number',
            'address_1', 'address_2',
            'town_or_city', 'county',
            'postcode', 'country'))
