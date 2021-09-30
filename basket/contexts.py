from decimal import Decimal
from django.conf import settings


def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0
    free_delivery_amount = settings.FREE_DELIVERY_AMOUNT
    delivery_percentage = settings.STANDARD_DELIVERY_PERCENTAGE

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
        'free_delivery_delta': free_delivery_delta,
        'grand_total': grand_total,
    }
    return context
