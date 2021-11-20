from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile, Reward
from checkout.models import Order, OrderLineItem
from products.models import (
    Category, Coffee, Offer, Price,
    Product, Review, Size, Type
)


def build_test_data():
    """Function to buld the test database, run before unit tests"""
    # Create admin user for unit tests
    adminuser = User.objects.create_superuser(
        'unittestadmin', 'unittestadmin@test.com', 'unittestadminpassword')
    adminuser.first_name = "Test"
    adminuser.last_name = "Admin"
    adminuser.save()
    # Create standard user for unit tests
    user = User.objects.create_user(
        'unittestuser', 'unittestuser@test.com', 'unittestuserpassword')
    user.first_name = "Test"
    user.last_name = "User"
    user.save()
    # Create a second standard user for unit tests
    user2 = User.objects.create_user(
        'joebloggs', 'joebloggs@test.com', 'joebloggspassword')
    user2.first_name = "Joe"
    user2.last_name = "Bloggs"
    user2.save()
    size_info = ("Test Size Information Line 1;"
                 "Test Size Information Line 2;"
                 "Test Size Information Line 3")
    type_info = ("Test Type Information Line 1;"
                 "Test Type Information Line 2;"
                 "Test Type Information Line 3")
    desc_full = ("Test Full Description Paragraph 1;"
                 "Test Full Description Paragraph 2;"
                 "Test Full Description Paragraph 3")
    desc_short = ("Test Short Description Line 1;"
                  "Test Short Description Line 2")
    category = Category.objects.create(
        name="Coffee",
        friendly_name="Coffee",
        description="Test description",
        size_description="Size",
        size_information=size_info,
        type_description="Grind",
        type_information=type_info,
        information_delimiter=";"
    )
    product = Product.objects.create(
        category=category,
        name="Test Coffee",
        friendly_name="Test Coffee Friendly Name",
        friendly_price="£7.50 - 250g",
        description_full=desc_full,
        description_short=desc_short,
        description_delimiter=";",
        rating=4.50,
        image="jump-leads-front-transparent.webp",
        image_alt="jump-leads-front-transparent.png",
        discontinued=False,
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
    type = Type.objects.create(
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
    price_small = Price.objects.create(
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
    Reward.objects.create(
        user=user,
        discount=10.00
    )
    Reward.objects.create(
        user=user2,
        discount=10.00
    )
    Reward.objects.create(
        user=adminuser,
        discount=10.00
    )
    user_profile = get_object_or_404(UserProfile, user=user)
    order = Order.objects.create(
        user_profile=user_profile,
        full_name="Test Name",
        email="test@gmail.com",
        phone_number="123456789",
        address_1="Test Address 1",
        town_or_city="Town Or City",
        country="GB",
        order_total=15.00,
        delivery_cost=2.00,
        grand_total=17.00,
        stripe_pid="Test Stripe PID",
    )
    OrderLineItem.objects.create(
        order=order,
        product=product,
        size=size_small,
        type=type,
        price=price_small,
        quantity=2,
    )
