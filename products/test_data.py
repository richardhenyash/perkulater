from .models import Category, Coffee, Offer, Price, Product, Size, Type


def build_test_data():
    """Function to buld the test database, run before unit tests"""
    category = Category.objects.create(
        name="Coffee",
        friendly_name="All of our top quality coffees",
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
