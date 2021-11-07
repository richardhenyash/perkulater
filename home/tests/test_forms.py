from django.test import TestCase
from products.tests.test_data import build_test_data
from home.forms import ContactForm


class TestContactForm(TestCase):
    """A class to test the Contact form"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_email_is_required(self):
        """Test to check email is required"""
        form = ContactForm({
            'from_email': '',
            'subject': 'Test Subject',
            'message': 'Test message content.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('from_email', form.errors.keys())
        self.assertEqual(
            form.errors['from_email'][0], 'This field is required.')

    def test_subject_is_required(self):
        """Test to check subject is required"""
        form = ContactForm({
            'from_email': 'test@test.com',
            'subject': '',
            'message': 'Test message content.',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors.keys())
        self.assertEqual(
            form.errors['subject'][0], 'This field is required.')

    def test_subject_max_length(self):
        """Test to check subject maximum length is 100 characters"""
        long_subject = ("very long email title subject"
                        "very long email title subject"
                        "very long email title subject"
                        "very long email title subject")
        print(len(long_subject))
        form = ContactForm({
            'from_email': 'test@test.com',
            'subject': long_subject,
            'message': 'Test message content.',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors.keys())
        self.assertEqual(
            form.errors['subject'][0][:44],
            'Ensure this value has at most 100 characters'
        )

    def test_message_is_required(self):
        """Test to check message is required"""
        form = ContactForm({
            'from_email': 'test@test.com',
            'subject': 'Test Subject',
            'message': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors.keys())
        self.assertEqual(
            form.errors['message'][0], 'This field is required.')
