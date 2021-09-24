from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Category, Product, Size, Type, Price, Coffee, Offer
from .helpers import get_product_offer_str

# Create your views here.

def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")
    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    product_category = get_object_or_404(Category, name=product.category)
    print(product_category)
    print(product_category.size_description)
    print(product_category.type_description)
    product_sizes = get_list_or_404(Size, category=product.category)
    product_types = get_list_or_404(Type, category=product.category)
    product_prices = get_list_or_404(Price, product=product.id)
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    context = {
        'product': product,
        'product_category': product_category,
        'product_sizes': product_sizes,
        'product_types': product_types,
        'product_prices': product_prices,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
    }

    coffee_detail = get_object_or_404(Coffee, pk=product_id)
    if coffee_detail:
        context['coffee_detail'] = coffee_detail

    return render(request, 'products/product_detail.html', context)

