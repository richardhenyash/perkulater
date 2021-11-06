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

    products = Product.objects.all()
    categories_all = Category.objects.all()
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    products = products.order_by("name")

    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'categories_all': categories_all,
    }
    return render(request, 'home/index.html', context)


def contact(request):
    """ A view to return the contact page """

    contact_email_sent = False
    if request.method == 'POST':
        contact_form = ContactForm(
            request.POST)
        if contact_form.is_valid():
            email = (contact_form.cleaned_data['from_email'])
            subject = (contact_form.cleaned_data['subject'])
            contact_message = (contact_form.cleaned_data['message'])
            email = EmailMessage(
                subject,
                contact_message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                reply_to=[email],
            )
            try:
                email.send(fail_silently=False)
                messages.success(
                    request, "Contact email sent succesfully.",
                    extra_tags='admin')
                contact_email_sent = True
            except SMTPException as smtp_error:
                errstr = 'Error sending contact email, ' + smtp_error
                messages.error(request, errstr, extra_tags='admin')

    if contact_email_sent:
        return redirect(reverse('products'))
    if request.user.is_authenticated:
        userobj = User.objects.get(username=request.user)
        contact_form = ContactForm(initial={'from_email': userobj.email})
    else:
        contact_form = ContactForm

    template = 'home/contact.html'
    context = {
        'contact_form': contact_form,
    }

    return render(request, template, context)
