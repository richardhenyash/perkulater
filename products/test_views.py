from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import resolve
from django.contrib.auth.models import User
from profiles.models import Reward
from .models import Category, Coffee, Product, Price, Review, Size

from .test_data import build_test_data


class TestProductViews(TestCase):
    """A class to test products views"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_resolve_products(self):
        """Test resolving products view"""
        found = resolve('/products/')
        self.assertEqual(found.url_name, "products")

    def test_resolve_product_detail(self):
        """Test resolving product detail view"""
        product = get_object_or_404(Product, name="Test Coffee")
        found = resolve(f'/products/{product.id}/')
        self.assertEqual(found.url_name, "product_detail")

    def test_resolve_add_product(self):
        """Test resolving add product view"""
        found = resolve('/products/add/')
        self.assertEqual(found.url_name, "add_product")

    def test_resolve_edit_product(self):
        """Test resolving edit product view"""
        product = get_object_or_404(Product, name="Test Coffee")
        found = resolve(f'/products/edit/{product.id}/')
        self.assertEqual(found.url_name, "edit_product")

    def test_resolve_delete_product(self):
        """Test resolving delete product view"""
        product = get_object_or_404(Product, name="Test Coffee")
        found = resolve(f'/products/delete/{product.id}/')
        self.assertEqual(found.url_name, "delete_product")

    def test_resolve_edit_prices(self):
        """Test resolving editing prices for a product"""
        product = get_object_or_404(Product, name="Test Coffee")
        found = resolve(f'/products/edit_prices/{product.id}/')
        self.assertEqual(found.url_name, "edit_prices")

    def test_resolve_review_product(self):
        """Test resolving product review"""
        product = get_object_or_404(Product, name="Test Coffee")
        found = resolve(f'/products/review_product/{product.id}/')
        self.assertEqual(found.url_name, "review_product")

    def test_resolve_delete_review(self):
        """Test resolving delete review"""
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        user = get_object_or_404(User, username='unittestuser')
        found = resolve(f'/products/delete_review/{product.id}/{user.id}/')
        self.assertEqual(found.url_name, "delete_review")

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
        self.assertRedirects(response, '/products/')

    def test_get_category(self):
        """Test returning all products in a category"""
        response = self.client.get('/products/', {'q': 'category=Coffee'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')

    def test_get_product_details(self):
        """Test returning product detail view"""
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/{product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_add_product(self):
        """Test returning add product view"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        response = self.client.get('/products/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/add_product.html")

    def test_post_add_product(self):
        """Test adding a product"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        category = get_object_or_404(Category, name="Coffee")
        response = self.client.post(
            '/products/add/',
            {
                'category': category.id,
                'name': 'Test New Coffee',
                'friendly_name': "Test New Coffee Friendly Name",
                'friendly_price': "£7.50 - 250g",
                'description_full': (
                    "Test Full Description Paragraph 1;" +
                    "Test Full Description Paragraph 2;" +
                    "Test Full Description Paragraph 3"),
                'description_short': (
                    "Test Short Description Line 1;" +
                    "Test Short Description Line 2"),
                'description_delimiter': ";",
                'rating': 4.50,
                'country': "Test Country",
                'farm': "Test Farm",
                'owner': "Test Owner",
                'variety': "Test Variety",
                'altitude': "Test Variety",
                'town': "Test Town",
                'region': "Test Region",
                'flavour_profile': "Test Flavour Profile",
            })
        # Get sizes
        size_small = get_object_or_404(Size, size="250g")
        size_large = get_object_or_404(Size, size="1kg")
        # Get new product
        product_new = get_object_or_404(Product, name="Test New Coffee")
        # Get new coffee
        coffee_new = get_object_or_404(Coffee, product=product_new)
        # Get new prices
        price_small = get_object_or_404(
            Price, product=product_new, size=size_small)
        price_large = get_object_or_404(
            Price, product=product_new, size=size_large)
        # Perform tests
        self.assertEqual(price_small.price, 7.50)
        self.assertEqual(price_large.price, 25.50)
        self.assertEqual(product_new.name, "Test New Coffee")
        self.assertEqual(coffee_new.country, "Test Country")
        self.assertEqual(response.status_code, 302)
        url = f'/products/{product_new.id}/'
        self.assertRedirects(response, url)

    def test_get_edit_product(self):
        """Test returning edit product view"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/edit/{product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/edit_product.html")

    def test_post_edit_product(self):
        """Test editing a product"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        category = get_object_or_404(Category, name="Coffee")
        url = f'/products/edit/{product.id}/'
        response = self.client.post(
            url,
            {
                'category': category.id,
                'name': 'Test Updated Coffee',
                'friendly_name': "Test Updated Coffee Friendly Name",
                'friendly_price': "£7.50 - 250g",
                'description_full': (
                    "Test Full Description Paragraph 1;" +
                    "Test Full Description Paragraph 2;" +
                    "Test Full Description Paragraph 3"),
                'description_short': (
                    "Test Short Description Line 1;" +
                    "Test Short Description Line 2"),
                'description_delimiter': ";",
                'rating': 4.50,
                'country': "Test Updated Country",
                'farm': "Test Farm",
                'owner': "Test Owner",
                'variety': "Test Variety",
                'altitude': "Test Variety",
                'town': "Test Town",
                'region': "Test Region",
                'flavour_profile': "Test Flavour Profile",
            })
        # Get updated product
        product_updated = get_object_or_404(
            Product, name="Test Updated Coffee")
        # Get updated coffee
        coffee_updated = get_object_or_404(
            Coffee, product=product_updated)
        # Perform tests
        self.assertEqual(product_updated.name, "Test Updated Coffee")
        self.assertEqual(
            product_updated.friendly_name, "Test Updated Coffee Friendly Name")
        self.assertEqual(coffee_updated.country, "Test Updated Country")
        self.assertEqual(response.status_code, 302)
        url = f'/products/{product_updated.id}/'
        self.assertRedirects(response, url)

    def test_post_delete_product(self):
        """Test deleting a product"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        response = self.client.post(f'/products/delete/{product.id}/')
        product_deleted = Product.objects.filter(name="Test Coffee")
        # Perform tests
        self.assertEqual(len(product_deleted), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')

    def test_get_edit_prices(self):
        """Test returning edit prices view for a product"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/edit_prices/{product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/edit_prices.html")

    def test_post_edit_prices(self):
        """Test editing prices for a product"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        size_small = get_object_or_404(Size, size="250g")
        url = f'/products/edit_prices/{product.id}/'
        response = self.client.post(
            url,
            {
                'size': size_small.id,
                'price': 9.50,
            })
        # Get updated price
        price_updated = get_object_or_404(
            Price, product=product, size=size_small)
        # Perform tests
        self.assertEqual(price_updated.price, 9.50)
        self.assertEqual(response.status_code, 302)
        url = f'/products/{product.id}/'
        self.assertRedirects(response, url)

    def test_get_review(self):
        """Test returning review for a product"""
        # login as standard user
        loginresponse = self.client.login(
            username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/review_product/{product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/review_product.html")

    def test_post_edit_review(self):
        """Test editing a user review for a product"""
        # login as standard user
        loginresponse = self.client.login(
            username='unittestuser', password='unittestuserpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        user = get_object_or_404(User, username='unittestuser')
        url = f'/products/review_product/{product.id}/'
        response = self.client.post(
            url,
            {
                'rating': 5,
                'review': "Awesome coffee!",
            })
        # Get updated review
        review_updated = get_object_or_404(
            Review, product=product, user=user)
        # Perform tests
        self.assertEqual(review_updated.rating, 5)
        self.assertEqual(review_updated.review, "Awesome coffee!")
        self.assertEqual(response.status_code, 302)
        url = f'/products/{product.id}/'
        self.assertRedirects(response, url)

    def test_post_add_new_review(self):
        """
        Test adding a new user review for a product
        Test that user reward is correctly added
        """
        # Create a test user
        user = User.objects.create_user(
            'johndoe', 'johndoe@test.com', 'johndoepassword')
        user.first_name = "John"
        user.last_name = "Doe"
        user.save()
        # login as the test user
        loginresponse = self.client.login(
            username='johndoe', password='johndoepassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        url = f'/products/review_product/{product.id}/'
        response = self.client.post(
            url,
            {
                'rating': 5,
                'review': "Awesome coffee!",
            })
        # Get new review
        review_new = get_object_or_404(
            Review, product=product, user=user)
        # Perform tests
        self.assertEqual(review_new.rating, 5)
        self.assertEqual(review_new.review, "Awesome coffee!")
        self.assertEqual(response.status_code, 302)
        url = f'/products/{product.id}/'
        self.assertRedirects(response, url)
        # Get user reward
        reward = get_object_or_404(
            Reward, user=user)
        # Check reward has been applied after adding new review
        self.assertEqual(reward.discount, 10.00)

    def test_post_delete_user_review(self):
        """Test deleting a user review for a product"""
        # login as admin user
        loginresponse = self.client.login(
            username='unittestadmin', password='unittestadminpassword')
        self.assertTrue(loginresponse)
        product = get_object_or_404(Product, name="Test Coffee")
        # get standard user review
        user = get_object_or_404(User, username='unittestuser')
        url = f'/products/delete_review/{product.id}/{user.id}/'
        response = self.client.post(url)
        # Perform tests
        review_deleted = Review.objects.filter(product=product, user=user)
        # Perform tests
        self.assertEqual(len(review_deleted), 0)
        self.assertEqual(response.status_code, 302)
        url = f'/products/{product.id}/'
        self.assertRedirects(response, url)
