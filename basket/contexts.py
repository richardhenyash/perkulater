from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Category, Product, Price, Offer, Size, Type
from profiles.models import Reward
from .models import Basket


def basket_contents(request):
    """
    Context processor for Basket
    """

    basket_items = []
    total = 0
    # Clear basket if flag has been set by webhook handler
    if request.user.is_authenticated:
        # Get user's Basket object
        basketobj = Basket.objects.filter(user=request.user).first()
        if basketobj:
            # Check if clear_basket is set
            if basketobj.clear_basket:
                if 'basket' in request.session:
                    # clear basket
                    del request.session['basket']
                    basketobj.clear_basket = False
                    basketobj.save()

    # Get basket from session
    basket = request.session.get('basket', {})
    # Initialise array of products to be deleted from basket
    delete_array = []
    for product_key, product_quantity in basket.items():
        # Split product_key out into id, size and type
        product_info_array = product_key.split("_")
        product_id = product_info_array[0]
        product_size_id = product_info_array[1]
        product_type_id = product_info_array[2]
        # product = get_object_or_404(Product, pk=product_id)
        product = Product.objects.filter(pk=product_id).first()
        # If product exists in database
        if product:
            # Get Product Category, Size and Type
            product_category = get_object_or_404(Category, name=product.category)
            product_size = get_object_or_404(Size, id=product_size_id)
            product_type = get_object_or_404(Type, id=product_type_id)
            # Get Product Price
            queryset = Price.objects.filter(
                product=product_id, size=product_size.id)
            product_price = get_object_or_404(queryset)
            # Calculate line item price
            line_item_price = product_price.price * product_quantity
            product_sku = product_price.sku
            # Add to total
            total = total + line_item_price
            # Append to basket_items
            basket_items.append({
                'product': product,
                'product_id': product.id,
                'product_key': product_key.strip(),
                'product_category': product_category,
                'product_quantity': product_quantity,
                'product_size': product_size,
                'product_type': product_type,
                'product_price': product_price,
                'product_sku': product_sku,
                'line_item_price': line_item_price,
            })
        else:
            # Append product key to delete array
            delete_array.append(product_key)
    # If products have been deleted from database, remove from the basket
    if len(delete_array) > 0:
        for product_id in delete_array:
            # Remove product from basket
            basket.pop(product_key)
        # Update basket in session
        request.session['basket'] = basket
    # Get delivery Offer object
    offer = get_object_or_404(Offer, description="Delivery")
    # Set delivery variables
    free_delivery_amount = offer.get_free_delivery_amount()
    delivery_percentage = offer.get_delivery_percentage()
    delivery_minimum = offer.get_delivery_minimum()
    # Calculate delivery charge
    if total < free_delivery_amount:
        delivery = total * (Decimal(delivery_percentage / 100))
        if delivery < delivery_minimum:
            delivery = delivery_minimum
        else:
            delivery = round(delivery, 2)
        free_delivery_delta = free_delivery_amount - total
    else:
        delivery = 0
        free_delivery_delta = 0

    # Apply reward
    discount = 0.0
    user_reward = None
    previous_total = None
    # Get user Reward if user is authenticated
    if request.user.is_authenticated:
        user_reward = Reward.objects.filter(user=request.user).first()
    if user_reward:
        if user_reward.discount:
            if user_reward.discount > 0:
                # Set discount
                discount = (total * user_reward.discount / 100)
                discount = round(discount, 2)
                previous_total = total
                total = round((total - discount), 2)
    # Calculate grand total
    grand_total = delivery + total
    # Set context
    context = {
        'basket_items': basket_items,
        'total': total,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'discount': discount,
        'previous_total': previous_total,
        'grand_total': grand_total,
    }
    return context
