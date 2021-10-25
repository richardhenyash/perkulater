import json
from decimal import Decimal
from django.shortcuts import get_object_or_404, HttpResponse, render, redirect, reverse
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
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
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
    categories_all = Category.objects.all()
    stripe_public_key = settings.STRIPE_PUBLIC_KEY    
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
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

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            current_basket = basket_contents(request)
            order.discount = current_basket['discount']
            print(order.discount)
            order.save()
            for product_key, product_quantity in basket.items():
                product_info_array = product_key.split("_")
                product_id = product_info_array[0]
                product_size_id = product_info_array[1]
                product_type_id = product_info_array[2]
                try:
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
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found \
                        in our database. Please call for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_basket'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            return redirect(reverse('checkout'))
            messages.error(request, 'There was an error submitting your form. \
                Please check the information provided.')

    else:

        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is currently empty")
            return redirect(reverse('products'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # if user is signed in populate information from user profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
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
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment varibables?')

        template = "checkout/checkout.html"
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'categories_all': categories_all,
        }
        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    categories_all = Category.objects.all()

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Reset Reward after checkout
        if request.user.is_authenticated:
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
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

            userobj = User.objects.get(username=request.user)
            user_data = {
                'first_name': order.full_name.split(" ")[0],
                'last_name': order.full_name.split(" ")[1]
            }
            user_form = UserForm(user_data, instance=userobj)
            if user_form.is_valid():
                user_form.save()
    
    messages.success(request, f'Your order has been successfully \
        processed! Your order number is {order_number}. \
        A confirmation email will be sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'categories_all': categories_all,        
    }

    return render(request, template, context)
