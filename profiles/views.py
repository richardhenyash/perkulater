from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPException

from .models import UserProfile
from .forms import UserForm, UserProfileForm, OrderContactForm
from checkout.models import Order


@login_required
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
        if user_profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(
                request,
                "Profile successfully updated",
                extra_tags='admin'
            )
        else:
            messages.error(
                request,
                "Profile update failed - please check profile form.",
                extra_tags='admin'
            )
    else:
        user_profile_form = UserProfileForm(instance=user_profile)
        user_form = UserForm(instance=userobj)
    orders = user_profile.orders.all().order_by('-date')

    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'orders': orders,
    }
    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order_date = order.date.strftime('%d/%m/%Y')
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        f'A confirmation email was sent on {order_date}.'
    ), extra_tags='admin')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def order_contact(request, order_number):
    contact_email_sent = False
    if request.method == 'POST':
        order_contact_form = OrderContactForm(
            request.POST)
        if order_contact_form.is_valid():
            userobj = User.objects.get(username=request.user)
            contact_message = (order_contact_form.cleaned_data['message'])
            email = EmailMessage(
                f"Order contact - order number: {order_number}",
                contact_message,
                userobj.email,
                [settings.DEFAULT_FROM_EMAIL],
                reply_to=[userobj.email],
            )
            try:
                email.send(fail_silently=False)
                messages.success(
                    request, "Order contact email sent succesfully.",
                    extra_tags='admin')
                contact_email_sent = True
            except SMTPException as smtp_error:
                errstr = 'Error sending order contact email, ' + smtp_error
                messages.error(request, errstr, extra_tags='admin')

    if contact_email_sent:
        return redirect(reverse('order_history', args=[order_number]))

    order = get_object_or_404(Order, order_number=order_number)
    order_contact_form = OrderContactForm
    template = 'profiles/order_contact.html'
    context = {
        'order': order,
        'order_contact_form': order_contact_form,
    }

    return render(request, template, context)
