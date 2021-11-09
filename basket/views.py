from django.shortcuts import (
    get_object_or_404, HttpResponse, redirect,
    render, reverse)
from django.contrib import messages
from products.models import Category, Product, Size, Type
from profiles.models import Reward


def view_basket(request):
    """
    Return the basket contents page
    """

    # Get Categories
    categories_all = Category.objects.all()
    # Get user Reward if user is authenticated
    user_reward = None
    if request.user.is_authenticated:
        user_reward = Reward.objects.filter(user=request.user).first()
    # Set template
    template = 'basket/basket.html'
    # Set context
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
    # Get Product
    product = get_object_or_404(Product, pk=product_id)
    # Get Product Size and Type
    product_size = request.POST.get('product-size')
    product_type = request.POST.get('product-type')
    size = get_object_or_404(Size, size=product_size)
    typeobj = get_object_or_404(Type, type=product_type)
    size_id = str(size.id)
    type_id = str(typeobj.id)
    # Get Product Quantity
    product_quantity = int(request.POST.get('product-quantity'))
    # Set Product Key
    product_key = product_id + "_" + size_id + "_" + type_id
    # Set redirect url
    redirect_url = request.POST.get('redirect_url')
    # Get basket
    basket = request.session.get('basket', {})
    # Update Product quantity if product key is in basket
    if product_key in list(basket.keys()):
        basket[product_key] += product_quantity
        messages.success(
            request, f'Added another {product.name} to your basket')
    # Else add product key to basket
    else:
        basket[product_key] = product_quantity
        messages.success(request, f'Added {product.name} to your basket')

    # Set basket in session
    request.session['basket'] = basket
    # Redirect to redirect_url
    return redirect(redirect_url)


def adjust_basket(request, product_key):
    """
    Update the quantity of the specified product in the basket
    """
    # Get product id from product_key
    product_id = int(product_key.split("_")[0])
    # Get Product
    product = get_object_or_404(Product, pk=product_id)
    # Get Product quantity
    product_quantity = int(request.POST.get('product-quantity'))
    # Get basket from session
    basket = request.session.get('basket', {})

    # If new product quantity is greater than 0, set product key in basket
    if product_quantity > 0:
        basket[product_key] = product_quantity
        messages.success(
            request, f'Updated quantity of {product.name} in your basket')
    # Else remove product key form basket
    else:
        basket.pop(product_key)
        messages.success(
            request, f'Removed {product.name} from your basket')
    # Set basket in session
    request.session['basket'] = basket
    # Redirect to view_basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, product_key):
    """
    Remove the specified product from the basket
    """
    # Get product id from product key
    product_id = int(product_key.split("_")[0])
    # Get Product
    product = get_object_or_404(Product, pk=product_id)
    # Get basket from session
    basket = request.session.get('basket', {})
    # Remove product key from basket
    basket.pop(product_key)
    messages.success(request, f'Removed {product.name} from your basket')
    # Set basket in session
    request.session['basket'] = basket
    # Try to return success
    try:
        return HttpResponse(status=200)
    # Return error if there is an exception
    except Exception as e:
        return HttpResponse(status=500)
        messages.error(request, f'Error removing item: {e}')
