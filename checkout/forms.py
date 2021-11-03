from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'address_1', 'address_2',
                  'town_or_city', 'county',
                  'postcode', 'country',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Post Code',
            'town_or_city': 'Town or City',
            'address_1': 'Street Address 1',
            'address_2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field_name, placeholder in placeholders.items():
            if self.fields[field_name].required:
                placeholder_text = placeholder + "*"
            else:
                placeholder_text = placeholder
            self.fields[field_name].widget.attrs[
                'placeholder'] = placeholder_text
            self.fields[field_name].widget.attrs[
                'class'] = 'checkout-input'
            self.fields[field_name].label = False
