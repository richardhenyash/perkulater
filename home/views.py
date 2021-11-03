from django.shortcuts import render, get_list_or_404
from products.models import Category, Product, Offer
from products.helpers import get_product_offer_str


def index(request):
    """ A view to return the index page """

    products = Product.objects.all()
    categories_all = Category.objects.all()
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    products = products.order_by("name")

    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'categories_all': categories_all,
    }
    return render(request, 'home/index.html', context)
