from django.shortcuts import render, get_list_or_404
from products.models import Product, Offer


def index(request):
    """ A view to return the index page """

    products = Product.objects.all()
    product_offers = get_list_or_404(Offer, display_in_banner=True)

    context = {
        'products': products,
        'product_offers': product_offers,
    }
    return render(request, 'home/index.html', context)
