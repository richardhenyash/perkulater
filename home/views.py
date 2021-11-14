from django.shortcuts import redirect, render, reverse, get_list_or_404
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from smtplib import SMTPException

from products.models import Category, Product, Offer
from products.helpers import get_product_offer_str
from .forms import ContactForm


def index(request):
    """ A view to return the index page """
    # Get Products
    products = Product.objects.all()
    # Get Categories
    categories_all = Category.objects.all()
    # Get Offers
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    products = products.order_by("name")
    # Set context
    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'categories_all': categories_all,
    }
    # Render index page
    return render(request, 'home/index.html', context)


def contact(request):
    """ A view to return the contact page """

    contact_email_sent = False
    if request.method == 'POST':
        # Instantiate COntactForm from POST data
        contact_form = ContactForm(
            request.POST)
        # Check if form is valid
        if contact_form.is_valid():
            # Get email, subject and message from cleaned form data
            email = (contact_form.cleaned_data['from_email'])
            subject = (contact_form.cleaned_data['subject'])
            contact_message = (contact_form.cleaned_data['message'])
            # Instantiate EmailMessage object from cleaned form data
            email = EmailMessage(
                subject,
                contact_message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                reply_to=[email],
            )
            # Try to send email
            try:
                email.send(fail_silently=False)
                # Success message
                messages.success(
                    request, "Contact email sent successfully.",
                    extra_tags='admin')
                contact_email_sent = True
            except SMTPException as smtp_error:
                errstr = 'Error sending contact email, ' + smtp_error
                # Error message
                messages.error(request, errstr, extra_tags='admin')

    if contact_email_sent:
        # Redirect to all products
        return redirect(reverse('products'))
    # If user is authenticated
    if request.user.is_authenticated:
        # Get User object
        userobj = User.objects.get(username=request.user)
        # Instantiate ContactForm with email address populated from User object
        contact_form = ContactForm(initial={'from_email': userobj.email})
    else:
        # Instantiate blank ContactForm
        contact_form = ContactForm

    # Set template
    template = 'home/contact.html'
    # Set context
    context = {
        'contact_form': contact_form,
    }
    # Render contact page
    return render(request, template, context)
