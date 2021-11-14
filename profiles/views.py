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
    # Get UserProfile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    # Get User
    userobj = User.objects.get(username=request.user)

    if request.method == 'POST':
        # Instantiate UserForm and UserProfileForm using POST data
        user_form = UserForm(
            request.POST, instance=userobj)
        user_profile_form = UserProfileForm(
            request.POST, instance=user_profile)
        # Check if forms are valid
        if user_profile_form.is_valid() and user_form.is_valid():
            # Save forms
            user_form.save()
            user_profile_form.save()
            # Display success message
            messages.success(
                request,
                "Profile successfully updated",
                extra_tags='admin'
            )
        # Display error message
        else:
            messages.error(
                request,
                "Profile update failed - please check profile form.",
                extra_tags='admin'
            )
    else:
        # Instantiate UserProfileForm with UserProfile object
        user_profile_form = UserProfileForm(instance=user_profile)
        # Instantiate UserForm with User object
        user_form = UserForm(instance=userobj)
    # Get Orders linked to UserProfile
    orders = user_profile.orders.all().order_by('-date')
    # Set template
    template = 'profiles/profile.html'
    # Set context
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'orders': orders,
    }
    # Render profile page
    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """
    Display Order history for the given Order number
    """
    # Get Order
    order = get_object_or_404(Order, order_number=order_number)
    # Set template, based on checkout success template
    template = 'checkout/checkout_success.html'
    # Set context
    context = {
        'order': order,
        'from_profile': True,
    }
    # Render order history page, based on checkout success template
    return render(request, template, context)


@login_required
def order_contact(request, order_number):
    """
    Contact about a specific Order
    """
    contact_email_sent = False
    if request.method == 'POST':
        # Instantiate OrderContacForm using POST data
        order_contact_form = OrderContactForm(
            request.POST)
        # Check if form is valid
        if order_contact_form.is_valid():
            # Get User
            userobj = User.objects.get(username=request.user)
            # Get message from cleaned form data
            contact_message = (order_contact_form.cleaned_data['message'])
            # Instantiate EmailMessage from form, User object and settings
            email = EmailMessage(
                f"Order contact - order number: {order_number}",
                contact_message,
                userobj.email,
                [settings.DEFAULT_FROM_EMAIL],
                reply_to=[userobj.email],
            )
            # Try to send email
            try:
                email.send(fail_silently=False)
                # Success message
                messages.success(
                    request, "Order contact email sent successfully.",
                    extra_tags='admin')
                contact_email_sent = True
            except SMTPException as smtp_error:
                # Error message
                errstr = 'Error sending order contact email, ' + smtp_error
                messages.error(request, errstr, extra_tags='admin')

    if contact_email_sent:
        # Redirect to Order history
        return redirect(reverse('order_history', args=[order_number]))

    # Get Order
    order = get_object_or_404(Order, order_number=order_number)
    # Instantiate blank OrderContactForm
    order_contact_form = OrderContactForm
    # Set template
    template = 'profiles/order_contact.html'
    # Set context
    context = {
        'order': order,
        'order_contact_form': order_contact_form,
    }
    # Render Order contact page
    return render(request, template, context)
