from django.test import TestCase
from django.urls import resolve
from django.contrib.messages import get_messages

from products.tests.test_data import build_test_data


class TestHomeViews(TestCase):
    """A class to test home views"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_resolve_home(self):
        """Test resolving home view"""
        found = resolve('/')
        self.assertEqual(found.url_name, "home")

    def test_resolve_contact(self):
        """Test resolving contact view"""
        found = resolve('/contact/')
        self.assertEqual(found.url_name, "contact")

    def test_get_home(self):
        """Test returning home page view"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_get_contact(self):
        """Test returning contact page view"""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/contact.html")

    def test_post_contact(self):
        """Test successfully submitting the contact form"""
        response = self.client.post(
            '/contact/',
            {
                'from_email': 'test@test.com',
                'subject': 'Test contact message subject',
                'message': 'Test contact message content.'
            }
        )
        self.assertEqual(response.status_code, 302)
        redirect_url = '/products/'
        self.assertRedirects(response, redirect_url)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(
            all_messages[0].message,
            "Contact email sent successfully.")
