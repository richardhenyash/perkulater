from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Product, Size, Type, Price, Coffee, Offer

# Create your views here.


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    product_offers = get_list_or_404(Offer, display_in_banner=True)

    context = {
        'products': products,
        'product_offers': product_offers,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    product_sizes = get_list_or_404(Size, category=product.category)
    product_types = get_list_or_404(Type, category=product.category)
    product_prices = get_list_or_404(Price, product=product.id)
    product_offers = get_list_or_404(Offer, display_in_banner=True)

    context = {
        'product': product,
        'product_sizes': product_sizes,
        'product_types': product_types,
        'product_prices': product_prices,
        'product_offers': product_offers,
    }

    coffee_detail = get_object_or_404(Coffee, pk=product_id)
    if coffee_detail:
        context['coffee_detail'] = coffee_detail

    return render(request, 'products/product_detail.html', context)
