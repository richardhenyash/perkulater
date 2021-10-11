from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents

import stripe


def checkout(request):

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "Your basket is currently empty")
        return redirect(reverse('products'))

    current_basket = basket_contents(request)
    total = current_basket['grand_total']
    stripe_total = round(total * 100)

    print(current_basket)
    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JM8lzKh2NPVXDhnC338M3XSsmGOLlWr7zkOKb2CEr45oZUDgBs7lUmwCeOloW7CKPykSN4hbsDMUPdkE8GtOCVv00R738RD2m',
        'client_secret': 'test_client_secret',
    }
    return render(request, template, context)
