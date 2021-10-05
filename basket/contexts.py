from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Category, Product, Price, Offer, Size


def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})
    for product_key, product_quantity in basket.items():
        product_info_array = product_key.split("_")
        product_id = product_info_array[0]
        product_size = product_info_array[1]
        product_type = product_info_array[2]
        product = get_object_or_404(Product, pk=product_id)
        product_category = get_object_or_404(Category, name=product.category)
        size = get_object_or_404(Size, size=product_size)
        queryset = Price.objects.filter(product=product_id, size=size.id)
        product_price = get_object_or_404(queryset)
        line_item_price = product_price.price * product_quantity
        basket_items.append({
            'product': product,
            'product_id': product.id,
            'product_category': product_category,
            'product_quantity': product_quantity,
            'product_size': product_size,
            'product_type': product_type,
            'product_price': product_price.price,
            'line_item_price': line_item_price,
        })
    print(basket_items)
    offer = get_object_or_404(Offer, description="Delivery")
    free_delivery_amount = offer.get_free_delivery_amount()
    delivery_percentage = offer.get_delivery_percentage()

    if total < free_delivery_amount:
        delivery = total * (Decimal(delivery_percentage / 100))
        free_delivery_delta = free_delivery_amount - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_amount': free_delivery_amount,
        'delivery_percentage': delivery_percentage,
        'free_delivery_delta': free_delivery_delta,
        'grand_total': grand_total,
    }
    return context
