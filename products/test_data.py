from .models import Category, Coffee, Offer, Price, Product, Review, Size, Type
from django.contrib.auth.models import User


def build_test_data():
    """Function to buld the test database, run before unit tests"""
    # Create admin user for unit tests
    adminuser = User.objects.create_superuser(
        'unittestadmin', 'unittestadmin@test.com', 'unittestadminpassword')
    # Creaet standard user for unit tests
    user = User.objects.create_user(
        'unittestuser', 'unittestuser@test.com', 'unittestuserpassword')
    category = Category.objects.create(
        name="Coffee",
        friendly_name="Coffee",
        description="Test description",
        size_description="Size",
        size_information="Test Size Information Line 1;Test Size Information Line 2;Test Size Information Line 3",
        type_description="Grind",
        type_information="Test Type Information Line 1;Test Type Information Line 2;Test Type Information Line 3",
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
        image="jump-leads-front-transparent.png",
    )
    Type.objects.create(
        category=category,
        type="Coarse"
    )
    Type.objects.create(
        category=category,
        type="Medium"
    )
    Type.objects.create(
        category=category,
        type="Fine"
    )
    Type.objects.create(
        category=category,
        type="Whole Bean"
    )
    size_small = Size.objects.create(
        category=category,
        size="250g",
        default_price=7.50)
    size_large = Size.objects.create(
        category=category,
        size="1kg",
        default_price=25.50)
    Price.objects.create(
        product=product,
        size=size_small,
        price=7.50,
        sku="TEST SKU")
    Price.objects.create(
        product=product,
        size=size_large,
        price=25.50,
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
        delivery_percentage=10.00,
        display_in_banner=True
    )
    Offer.objects.create(
        description="Review",
        description_full="Add a review to get 10% off your next order",
        free_delivery_amount=0.00,
        discount=10.00,
        display_in_banner=True
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
    Review.objects.create(
        product=product,
        user=adminuser,
        rating=5,
        review="Awesome tasting coffee - the best!"
    )
    Review.objects.create(
        product=product,
        user=user,
        rating=1,
        review="Not great - don't buy it!"
    )