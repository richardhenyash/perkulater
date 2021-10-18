from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from .models import UserProfile
from .forms import UserForm, UserProfileForm
from checkout.models import Order


def profile(request):
    """
    Display the signed in user's profile
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    userobj = User.objects.get(username=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(
            request.POST, instance=userobj)
        user_profile_form = UserProfileForm(
            request.POST, instance=user_profile)
        if user_profile_form.is_valid and user_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, "Profile successfully updated")

    user_profile_form = UserProfileForm(instance=user_profile)
    user_form = UserForm(instance=userobj)
    orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'orders': orders,
        'on_profile_page': True,
    }
    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order_date = order.date.strftime('%d/%m/%Y')
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        f'A confirmation email was sent on {order_date}.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
