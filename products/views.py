from django.shortcuts import render, get_object_or_404
from .models import Product, Size, Type, Price, Coffee

# Create your views here.


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    coffee_detail = get_object_or_404(Coffee, pk=product_id)
    if coffee_detail:
        context = {
            'product': product,
            'coffee_detail': coffee_detail,
        }
    else:
        context = {
            'product': product,
        }

    return render(request, 'products/product_detail.html', context)
