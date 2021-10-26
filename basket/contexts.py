from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Category, Product, Price, Offer, Size, Type
from profiles.models import Reward


def basket_contents(request):

    basket_items = []
    total = 0
    basket = request.session.get('basket', {})
    for product_key, product_quantity in basket.items():
        product_info_array = product_key.split("_")
        product_id = product_info_array[0]
        product_size_id = product_info_array[1]
        product_type_id = product_info_array[2]
        product = get_object_or_404(Product, pk=product_id)
        product_category = get_object_or_404(Category, name=product.category)
        product_size = get_object_or_404(Size, id=product_size_id)
        product_type = get_object_or_404(Type, id=product_type_id)
        queryset = Price.objects.filter(product=product_id, size=product_size.id)
        product_price = get_object_or_404(queryset)
        line_item_price = product_price.price * product_quantity
        product_sku = product_price.sku
        total = total + line_item_price
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
    offer = get_object_or_404(Offer, description="Delivery")
    free_delivery_amount = offer.get_free_delivery_amount()
    delivery_percentage = offer.get_delivery_percentage()
    delivery_minimum = offer.get_delivery_minimum()

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

    # Apply rewards
    discount = 0.00
    user_reward = None
    previous_total = None
    if request.user.is_authenticated:
        user_reward = Reward.objects.filter(user=request.user).first()
    if user_reward:
        if user_reward.discount:
            if user_reward.discount > 0:
                discount = Decimal((total * user_reward.discount / 100))
                discount = round(discount, 2)
                previous_total = total
                total = round((total - discount), 2)

    grand_total = delivery + total

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
