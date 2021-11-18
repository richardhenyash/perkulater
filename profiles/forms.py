from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    """
    A form for User
    """
    class Meta:
        # Set model
        model = User
        # Set field names
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        # Set placeholders
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        # Set autofocus to first_name field
        self.fields['first_name'].widget.attrs['autofocus'] = True
        # Loop through fields, add placeholders
        for field in self.fields:
            # Add a * to placeholder if field is required
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # Set placeholder
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add profile-input class
            self.fields[field].widget.attrs['class'] = 'profile-input'
            # Turn off label
            self.fields[field].label = False


class UserProfileForm(forms.ModelForm):
    """
    A form for UserProfile
    """
    class Meta:
        # Set model
        model = UserProfile
        # Set field names
        fields = ('phone_number',
                  'address_1', 'address_2',
                  'town_or_city', 'county',
                  'postcode', 'country',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes,
        and remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        # Set placeholders
        placeholders = {
            'phone_number': 'Phone Number',
            'address_1': 'Street Address 1',
            'address_2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County, State or Locality',
            'postcode': 'Post Code',
        }
        # Loop through fields, add placeholders
        for field in self.fields:
            # If field is not country
            if field != 'country':
                # Add a * to placeholder if field is required
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Set placeholder
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add profile-input class
            self.fields[field].widget.attrs['class'] = 'profile-input'
            # Turn off label
            self.fields[field].label = False


class OrderContactForm(forms.Form):
    """
    An Order contact form
    """
    def __init__(self, *args, **kwargs):
        """
        Set placeholders
        """
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['placeholder'] = 'Message'
    message = forms.CharField(required=True, widget=forms.Textarea)
