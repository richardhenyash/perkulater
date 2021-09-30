from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Offer


def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0

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
