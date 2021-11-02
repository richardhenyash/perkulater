from django.shortcuts import (
    get_object_or_404, HttpResponse, redirect,
    render, reverse)
from django.contrib import messages
from products.models import Category, Product, Size, Type
from profiles.models import Reward


def view_basket(request):
    """ A view to return the basket contents page """

    categories_all = Category.objects.all()
    user_reward = None
    if request.user.is_authenticated:
        user_reward = Reward.objects.filter(user=request.user).first()
    template = 'basket/basket.html'
    context = {
        'categories_all': categories_all,
        'user_reward': user_reward,
    }
    return render(request, template, context)


def add_to_basket(request, product_id):
    """
    Add a product to the basket based on product id,
    product size and product type
    """
    product = get_object_or_404(Product, pk=product_id)
    product_size = request.POST.get('product-size')
    product_type = request.POST.get('product-type')
    size = get_object_or_404(Size, size=product_size)
    typeobj = get_object_or_404(Type, type=product_type)
    size_id = str(size.id)
    type_id = str(typeobj.id)
    product_quantity = int(request.POST.get('product-quantity'))
    product_key = product_id + "_" + size_id + "_" + type_id

    redirect_url = request.POST.get('redirect_url')

    basket = request.session.get('basket', {})

    if product_key in list(basket.keys()):
        basket[product_key] += product_quantity
        messages.success(
            request, f'Added another {product.name} to your basket')
    else:
        basket[product_key] = product_quantity
        messages.success(request, f'Added {product.name} to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def adjust_basket(request, product_key):
    """
    Update the quantity of the specified product in the basket
    """
    product_id = int(product_key.split("_")[0])
    product = get_object_or_404(Product, pk=product_id)
    product_quantity = int(request.POST.get('product-quantity'))
    basket = request.session.get('basket', {})

    if product_quantity > 0:
        basket[product_key] = product_quantity
        messages.success(
            request, f'Updated quantity of {product.name} in your basket')
    else:
        basket.pop(product_key)
        messages.success(
            request, f'Removed {product.name} from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, product_key):
    """
    Remove the specified product from the basket
    """
    product_id = int(product_key.split("_")[0])
    product = get_object_or_404(Product, pk=product_id)
    basket = request.session.get('basket', {})
    basket.pop(product_key)
    messages.success(request, f'Removed {product.name} from your basket')
    request.session['basket'] = basket

    try:
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
        messages.error(request, f'Error removing item: {e}')
