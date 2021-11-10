from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    A form for Orders
    """
    class Meta:
        # Set model
        model = Order
        # Set field names
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
        # Set placeholders
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
        # Set autofocus to full_name field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Loop through fields, add placeholders
        for field_name, placeholder in placeholders.items():
            # Add a * to placeholder if field is required
            if self.fields[field_name].required:
                placeholder_text = placeholder + "*"
            else:
                placeholder_text = placeholder
            # Set placeholder
            self.fields[field_name].widget.attrs[
                'placeholder'] = placeholder_text
            # Add checkout-input class
            self.fields[field_name].widget.attrs[
                'class'] = 'checkout-input'
            # Switch label off
            self.fields[field_name].label = False
