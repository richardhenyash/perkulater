from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "Your basket is currently empty")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JM8lzKh2NPVXDhnC338M3XSsmGOLlWr7zkOKb2CEr45oZUDgBs7lUmwCeOloW7CKPykSN4hbsDMUPdkE8GtOCVv00R738RD2m',
        'client_secret': 'test_client_secret',
    }
    return render(request, template, context)
