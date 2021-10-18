from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Order, OrderLineItem
from products.models import Price, Product, Size, Type
from profiles.models import UserProfile

import json
import time


class Stripe_WebHook_Handler:
    """Class to handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email on checkout"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
   
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received from Stripe: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Set empty data fields in the shipping details to None
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.phone_number = shipping_details.phone
                profile.address_1 = shipping_details.address.line1
                profile.address_2 = shipping_details.address.line2
                profile.town_or_city = shipping_details.address.city
                profile.county = shipping_details.address.state
                profile.postcode = shipping_details.address.postal_code
                profile.country = shipping_details.address.country
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    address_1__iexact=shipping_details.address.line1,
                    address_2__iexact=shipping_details.address.line2,
                    town_or_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    address_1=shipping_details.address.line1,
                    address_2=shipping_details.address.line2,
                    town_or_city=shipping_details.address.city,
                    county=shipping_details.address.state,
                    postcode=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                basket = json.loads(basket)
                for product_key, product_quantity in basket.items():                    
                    product_info_array = product_key.split("_")
                    product_id = product_info_array[0]
                    product_size_id = product_info_array[1]
                    product_type_id = product_info_array[2]
                    # Get product, size and type from product key
                    product = get_object_or_404(Product, pk=product_id)
                    product_size = get_object_or_404(Size, id=product_size_id)
                    product_type = get_object_or_404(Type, id=product_type_id)
                    queryset = Price.objects.filter(product=product_id, size=product_size.id)
                    product_price = get_object_or_404(queryset)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        size=product_size,
                        type=product_type,
                        price=product_price,
                        quantity=product_quantity,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received from Stripe: {event["type"]}',
            status=200)
