from django.test import TestCase
from django.urls import resolve

class TestHomeViews(TestCase):
    """A class to test home views"""

    def test_resolve_home(self):
        """Test resolving home view"""
        found = resolve('/')
        self.assertEqual(found.url_name, "home")
