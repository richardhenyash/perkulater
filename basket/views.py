from django.shortcuts import redirect, render


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
    product_quantity = int(request.POST.get('product-quantity'))
    product_key = product_id + "_" + product_size + "_" + product_type

    redirect_url = request.POST.get('redirect_url')

    basket = request.session.get('basket', {})

    if product_key in list(basket.keys()):
        basket[product_key] += product_quantity
    else:
        basket[product_key] = product_quantity

    request.session['basket'] = basket
    return redirect(redirect_url)
