from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Size, Type, Price, Coffee, Offer
from .helpers import get_product_offer_str

# Create your views here.

def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'product_search': query,
    }

    return render(request, 'products/products.html', context)


def coffees(request):
    """ A view to show coffees """

    products = get_list_or_404(Product, category=1)
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
    product_sizes = get_list_or_404(Size, category=product.category)
    product_types = get_list_or_404(Type, category=product.category)
    product_prices = get_list_or_404(Price, product=product.id)

    # Build dictionary of sizes and prices for the product
    product_price_dict = {}
    for priceobj in product_prices:
        product_price_dict[priceobj.get_size()] = priceobj.get_price()

    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    context = {
        'product': product,
        'product_category': product_category,
        'product_sizes': product_sizes,
        'product_types': product_types,
        'product_prices': product_prices,
        'product_price_dict': product_price_dict,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
    }

    coffee_detail = get_object_or_404(Coffee, pk=product_id)

    if coffee_detail:
        context['coffee_detail'] = coffee_detail

    return render(request, 'products/product_detail.html', context)

