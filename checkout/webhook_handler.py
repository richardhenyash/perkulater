"""
Checkout application webhook handler module
"""
from decimal import Decimal
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .models import Order, OrderLineItem
from basket.models import Basket
from products.models import Price, Product, Size, Type
from profiles.models import UserProfile, Reward

import json
import time


class Stripe_WebHook_Handler:
    """Class to handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email on checkout"""
        # Get email address from order
        cust_email = order.email
        # Set email subject from email template
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        # Set email body from email template
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        # Send email
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
        # Get intent from event
        intent = event.data.object
        # Get stripe pid from intent
        pid = intent.id
        # Get basket from intent
        basket = intent.metadata.basket
        # Get save_info from intent
        save_info = intent.metadata.save_info
        # Get order discount from intent
        order_discount = intent.metadata.discount
        order_discount = Decimal(order_discount)
        order_discount = round(order_discount, 2)
        # Get billing details from intent
        billing_details = intent.charges.data[0].billing_details
        # Get shipping details from intent
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)
        profile = None
        username = intent.metadata.username
        # If user is authenticated
        if username != 'AnonymousUser':
            # Get UserProfile
            profile = UserProfile.objects.get(user__username=username)
            # Update UserProfile if save_info was checked
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
        # Attempt to get Order from database
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
        # If Order exists in database
        if order_exists:
            # Send confirmation email
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} \
                    | SUCCESS: Verified order already in database',
                status=200)
        # Else try to create Order
        else:
            order = None
            try:
                # Instantiate Order object from webhook data
                order = Order(
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
                order.discount = order_discount
                order.save()
                # Get basket from webhook data
                basket = json.loads(basket)
                # Create OrderlineItem for each item in basket
                for product_key, product_quantity in basket.items():
                    product_info_array = product_key.split("_")
                    product_id = product_info_array[0]
                    product_size_id = product_info_array[1]
                    product_type_id = product_info_array[2]
                    # Get Product, Size and Type from product key
                    product = get_object_or_404(Product, pk=product_id)
                    product_size = get_object_or_404(Size, id=product_size_id)
                    product_type = get_object_or_404(Type, id=product_type_id)
                    # Get Price
                    queryset = Price.objects.filter(
                        product=product_id, size=product_size.id)
                    product_price = get_object_or_404(queryset)
                    # Instantitate OrderLineItem object
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        size=product_size,
                        type=product_type,
                        price=product_price,
                        quantity=product_quantity,
                    )
                    # Save OrderLineItem object
                    order_line_item.save()
                # If user is authenticated
                if username != 'AnonymousUser':
                    # Reset Reward after checkout
                    user = get_object_or_404(User, username=username)
                    user_reward = Reward.objects.filter(user=user).first()
                    user_reward.discount = 0.00
                    user_reward.save()
                    # Set flag to clear basket on successful order creation
                    basketobj = Basket.objects.filter(user=user).first()
                    if basketobj:
                        basketobj.clear_basket = True
                        basketobj.save()
                    else:
                        newbasketobj = Basket(user=user, clear_basket=True)
                        newbasketobj.save()

            except Exception as e:
                # Delete Order if it exists
                if order:
                    order.delete()
                # Return response
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} \
                        | ERROR: {e}', status=500)
        # Send confirmation email
        self._send_confirmation_email(order)
        # Return response
        return HttpResponse(
            content=f'Webhook received: {event["type"]} \
                | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received from Stripe: {event["type"]}',
            status=200)
