"""
Checkout application views module
"""
import json
from django.shortcuts import (
    get_object_or_404, HttpResponse, render, redirect, reverse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents
from .models import Order, OrderLineItem
from products.models import Category, Product, Price, Size, Type
from profiles.models import UserProfile, Reward
from profiles.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User

import stripe


@require_POST
def cache_checkout_data(request):
    try:
        # Get stripe pid
        pid = request.POST.get('client_secret').split('_secret')[0]
        # Get stripe secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Set stripe payment intent
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'discount': request.POST.get('discount'),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Display the checkout page and allow checkout
    """
    # Get Categories
    categories_all = Category.objects.all()
    # Set stripe keys
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # Get basket from session
        basket = request.session.get('basket', {})
        # Get form data from session
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        # Instantiate OrderForm using form data
        order_form = OrderForm(form_data)
        # Check if order for is valid
        if order_form.is_valid():
            # Save OrderForm information to order object
            order = order_form.save(commit=False)
            # Get stripe pid from POST data
            pid = request.POST.get('client_secret').split('_secret')[0]
            # Set stripe pid on Order object
            order.stripe_pid = pid
            # Set original basket on Order object
            order.original_basket = json.dumps(basket)
            # Get curent basket
            current_basket = basket_contents(request)
            # Get discount
            order.discount = current_basket['discount']
            # Save Order
            order.save()
            # Loop through basket items, create OrderLineItem objects
            for product_key, product_quantity in basket.items():
                # Get product, size and type from product key
                product_info_array = product_key.split("_")
                product_id = product_info_array[0]
                product_size_id = product_info_array[1]
                product_type_id = product_info_array[2]
                try:
                    product = get_object_or_404(Product, pk=product_id)
                    product_size = get_object_or_404(Size, id=product_size_id)
                    product_type = get_object_or_404(Type, id=product_type_id)
                    # Get product price
                    queryset = Price.objects.filter(
                        product=product_id, size=product_size.id)
                    product_price = get_object_or_404(queryset)
                    # Instantiate OrderLineItem
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        size=product_size,
                        type=product_type,
                        price=product_price,
                        quantity=product_quantity,
                    )
                    # Save OrderLineItem
                    order_line_item.save()
                # If product does not exist
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found \
                        in our database. Please call for assistance!")
                    )
                    # Delete Order
                    order.delete()
                    # Redirect to view basket
                    return redirect(reverse('view_basket'))
            # Get save info from session
            request.session['save_info'] = 'save-info' in request.POST
            # Redirect to checkout success
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            # Redirect to checkout
            return redirect(reverse('checkout'))
            messages.error(request, 'There was an error submitting your form. \
                Please check the information provided.')

    else:
        # Get basket from session
        basket = request.session.get('basket', {})
        # If basket is empty
        if not basket:
            messages.error(request, "Your basket is currently empty")
            # Redirect to Products
            return redirect(reverse('products'))
        # Set current basket
        current_basket = basket_contents(request)
        # Set grand total
        total = current_basket['grand_total']
        # Set stripe total
        stripe_total = round(total * 100)
        # Set stripe api key
        stripe.api_key = stripe_secret_key
        # Create and set payment intent
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # if user is authenticated, populate information from user profile
        if request.user.is_authenticated:
            try:
                # Get UserProfile
                profile = UserProfile.objects.get(user=request.user)
                # Instantiate OrderForm based on UserProfile data
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'address_1': profile.address_1,
                    'address_2': profile.address_2,
                    'town_or_city': profile.town_or_city,
                    'county': profile.county,
                    'postcode': profile.postcode,
                    'country': profile.country,
                })
            # If UserProfile does not exist
            except UserProfile.DoesNotExist:
                # Instantiate blank OrderForm
                order_form = OrderForm()
        else:
            # Instantiate blank OrderForm
            order_form = OrderForm()
        # Check if stripe public key is set
        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment varibables?')
        # Set template
        template = "checkout/checkout.html"
        # Set context
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'categories_all': categories_all,
        }
        # Render template
        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    # Get save info from session
    save_info = request.session.get('save_info')
    # Get Order from Order number
    order = get_object_or_404(Order, order_number=order_number)
    # Get categories
    categories_all = Category.objects.all()
    # If user is authenticated
    if request.user.is_authenticated:
        # Get UserProfile
        profile = UserProfile.objects.get(user=request.user)
        # Attach the UserProfile to the order
        order.user_profile = profile
        # Save the Order
        order.save()

        # Reset Reward after successful checkout
        user_reward = Reward.objects.filter(user=request.user).first()
        if user_reward:
            user_reward.discount = 0.0
            user_reward.save()

        # Save the user's info if save info box is ticked
        if save_info:
            profile_data = {
                'phone_number': order.phone_number,
                'address_1': order.address_1,
                'address_2': order.address_2,
                'town_or_city': order.town_or_city,
                'county': order.county,
                'postcode': order.postcode,
                'country': order.country,
            }
            # Instantiate UserProfileForm with data from Order
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            # If UserProfileForm is valid
            if user_profile_form.is_valid():
                # Save form
                user_profile_form.save()
            # Get User object
            userobj = User.objects.get(username=request.user)
            # If first name and last name are given
            if len(order.full_name.split(" ")) > 1:
                # Set first name and last name
                user_data = {
                    'first_name': order.full_name.split(" ")[0],
                    'last_name': order.full_name.split(" ")[1]
                }
            # Else set first name
            else:
                user_data = {'first_name': order.full_name}
            # Instantiate UserForm
            user_form = UserForm(user_data, instance=userobj)
            # Check if UserForm is valid
            if user_form.is_valid():
                # Save UserForm
                user_form.save()
    # Display success messsage
    messages.success(request, f'Your order has been successfully \
        processed! Your order number is {order_number}. \
        A confirmation email will be sent to {order.email}.')

    # Delete basket from session
    if 'basket' in request.session:
        del request.session['basket']
    # Set template
    template = 'checkout/checkout_success.html'
    # Set context
    context = {
        'order': order,
        'categories_all': categories_all,
    }
    # Render template
    return render(request, template, context)
