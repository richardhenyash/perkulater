from django.test import TestCase
from products.test_data import build_test_data
from .forms import UserForm, UserProfileForm, OrderContactForm


class TestUserForm(TestCase):
    """A class to test the User form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_first_name_is_not_required(self):
        """Test to check first name is not required"""
        form = UserForm({
            'first_name': '',
            'last_name': 'Bloggs'
            })
        self.assertTrue(form.is_valid())

    def test_last_name_is_not_required(self):
        """Test to check last name is not required"""
        form = UserForm({
            'first_name': 'Joe',
            'last_name': ''
            })
        self.assertTrue(form.is_valid())

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = UserForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'first_name', 'last_name'])

    def test_fields_are_explicit_in_form_metaclass(self):
        """Test to check fields are explicit in form metaclass"""
        form = UserForm()
        self.assertEqual(form.Meta.fields, (
            'first_name', 'last_name'))


class TestUserProfileForm(TestCase):
    """A class to test the UserProfile form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_phone_number_is_not_required(self):
        """Test to check phone number is not required"""
        form = UserProfileForm({
            'phone_number': '',
            'address_1': 'Test Address 1',
            'address_2': 'Test Address 2',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'SE255XX',
            'country': 'GB'
            })
        self.assertTrue(form.is_valid())

    def test_address_1_is_not_required(self):
        """Test to check address 1 is not required"""
        form = UserProfileForm({
            'phone_number': '123456789',
            'address_1': '',
            'address_2': 'Test Address 2',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'SE255XX',
            'country': 'GB'
            })
        self.assertTrue(form.is_valid())

    def test_address_2_is_not_required(self):
        """Test to check address 2 is not required"""
        form = UserProfileForm({
            'phone_number': '123456789',
            'address_1': 'Test Address 1',
            'address_2': '',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'SE255XX',
            'country': 'GB'
            })
        self.assertTrue(form.is_valid())

    def test_town_or_city_is_not_required(self):
        """Test to check town or city is not required"""
        form = UserProfileForm({
            'phone_number': '123456789',
            'address_1': 'Test Address 1',
            'address_2': 'Test Address 1',
            'town_or_city': '',
            'county': 'Test County',
            'postcode': 'SE255XX',
            'country': 'GB'
            })
        self.assertTrue(form.is_valid())

    def test_county_is_not_required(self):
        """Test to check county is not required"""
        form = UserProfileForm({
            'phone_number': '123456789',
            'address_1': 'Test Address 1',
            'address_2': 'Test Address 1',
            'town_or_city': 'Test Town',
            'county': '',
            'postcode': 'XXXXXXX',
            'country': 'GB'
            })
        self.assertTrue(form.is_valid())

    def test_postcode_is_not_required(self):
        """Test to check post code is not required"""
        form = UserProfileForm({
            'phone_number': '123456789',
            'address_1': 'Test Address 1',
            'address_2': 'Test Address 1',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': '',
            'country': 'GB'
            })
        self.assertTrue(form.is_valid())

    def test_country_is_not_required(self):
        """Test to check country is not required"""
        form = UserProfileForm({
            'phone_number': '123456789',
            'address_1': 'Test Address 1',
            'address_2': 'Test Address 1',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'XXXXXXX',
            'country': ''
            })
        self.assertTrue(form.is_valid())

    def test_fields_in_form_metaclass(self):
        """Test to check fields in form metaclass"""
        form = UserProfileForm()
        form_fields = [field.name for field in form]
        self.assertEqual(form_fields, [
            'phone_number', 'address_1',
            'address_2', 'town_or_city',
            'county', 'postcode',
            'country'])

    def test_fields_are_explicit_in_form_metaclass(self):
        """Test to check fields are explicit in form metaclass"""
        form = UserProfileForm()
        self.assertEqual(form.Meta.fields, (
            'phone_number', 'address_1',
            'address_2', 'town_or_city',
            'county', 'postcode',
            'country'))


class TestOrderContactForm(TestCase):
    """A class to test the OrderContact form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_message_is_required(self):
        """Test to check message is required"""
        form = OrderContactForm({
            'message': '',
            })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors.keys())
        self.assertEqual(form.errors['message'][0], 'This field is required.')
