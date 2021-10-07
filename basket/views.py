from django.shortcuts import redirect, render, reverse, get_object_or_404
from products.models import Product, Size, Type

def view_basket(request):
    """ A view to return the basket contents page """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):
    """
    Add a product to the basket based on product id,
    product size and product type
    """
    product_size = request.POST.get('product-size')
    product_type = request.POST.get('product-type')
    size = get_object_or_404(Size, size=product_size)
    type = get_object_or_404(Type, type=product_type)
    size_id = str(size.id)
    type_id = str(type.id)
    product_quantity = int(request.POST.get('product-quantity'))
    product_key = product_id + "_" + size_id + "_" + type_id

    redirect_url = request.POST.get('redirect_url')

    basket = request.session.get('basket', {})

    if product_key in list(basket.keys()):
        basket[product_key] += product_quantity
    else:
        basket[product_key] = product_quantity

    request.session['basket'] = basket
    # request.session['basket'] = {}
    return redirect(redirect_url)


def adjust_basket(request, product_key):
    """
    Update the quantity of a specific product in the basket
    """
    product_quantity = int(request.POST.get('product-quantity'))
    print(product_quantity)
    basket = request.session.get('basket', {})

    if product_quantity > 0:
        basket[product_key] = product_quantity
    else:
        basket.pop(product_key)

    request.session['basket'] = basket
    # request.session['basket'] = {}
    return redirect(reverse('view_basket'))
