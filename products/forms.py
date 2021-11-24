"""
Products application form configuration module
"""
from django import forms
from .widgets import (
    CustomClearableFileInputDefault,
    CustomClearableFileInputAlt)
from .models import Category, Coffee, Product, Price, Review


class ProductForm(forms.ModelForm):
    """
    A form for products.
    """
    class Meta:
        # Set model
        model = Product
        # Set field names
        fields = (
            'category', 'name', 'friendly_name',
            'friendly_price', 'description_full',
            'description_short', 'description_delimiter',
            'image', 'image_alt', 'discontinued',
        )
        # Set field labels
        labels = {
            'friendly_name': 'Display Name',
            'friendly_price': 'Display Price',
            'description_full': 'Full Description',
            'description_short': 'Short Description',
            'description_delimiter': 'Description Delimiter',
            'image': 'Image',
            'image_alt': 'Alternative Image',
            'discontinued': 'Discontinued',
        }
    # Set image field, use custom widget
    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInputDefault)

    # Set alternate image field, use custom widget
    image_alt = forms.ImageField(
        label='Alternative Image',
        required=False, widget=CustomClearableFileInputAlt)

    def __init__(self, *args, **kwargs):
        """
        Set category select, add placeholders and classes,
        set autofocus on country field.
        """
        super().__init__(*args, **kwargs)
        # Get Categories
        categories = Category.objects.all()
        # Get Category friendly names
        friendly_names = [
            (c.id, c.get_friendly_name()) for c in categories]
        # Set Category select choices to friendly names
        self.fields['category'].choices = friendly_names
        # Set placeholders
        placeholders = {
            'name': 'Name',
            'friendly_name': 'Friendly Name',
            'friendly_price': 'Friendly Price',
            'description_full': 'Full Description',
            'description_short': 'Short Description',
            'description_delimiter': 'Description Delimiter',
        }
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
            # Add product-input class
            self.fields[field_name].widget.attrs[
                'class'] = 'product-input'


class CoffeeForm(forms.ModelForm):
    """
    A form for Coffees.
    """
    class Meta:
        # Set model
        model = Coffee
        # Set field names
        fields = (
            'country', 'farm', 'owner',
            'variety', 'altitude',
            'town', 'region',
            'flavour_profile'
        )
        # Set field labels
        labels = {
            'country': 'Country Of Origin',
            'flavour_profile': 'Flavour Profile',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on country field
        """
        super().__init__(*args, **kwargs)
        # Set placeholders
        placeholders = {
            'country': 'Country Of Origin',
            'farm': 'Farm',
            'owner': 'Owner',
            'variety': 'Variety',
            'altitude': 'Altitude',
            'town': 'Town',
            'region': 'Region',
            'flavour_profile': 'Flavour Profile',
        }
        # Set autofocus to country field
        self.fields['country'].widget.attrs['autofocus'] = True
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
            # Add coffee-input class
            self.fields[field_name].widget.attrs[
                'class'] = 'coffee-input'


class PriceForm(forms.ModelForm):
    """
    A form for Prices.
    """
    class Meta:
        # Set model
        model = Price
        # Set field names
        fields = ('size', 'price')
        # Set field labels
        labels = {
            'size': 'Size',
            'price': 'Price £',
        }

    def __init__(self, *args, **kwargs):
        """
        Set autofocus, add class, remove empty label
        """
        super().__init__(*args, **kwargs)

        self.fields['size'].empty_label = None
        self.fields['price'].widget.attrs['autofocus'] = True
        self.fields['price'].widget.attrs['class'] = 'price-input'


class ReviewForm(forms.ModelForm):
    """
    A form for Reviews.
    """
    class Meta:
        # Set model
        model = Review
        # Set field names
        fields = ('rating', 'review')
        # Set field labels
        labels = {
            'rating': 'Rating',
            'review': 'Review',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, set autofocus on review field
        """
        super().__init__(*args, **kwargs)
        # Set placeholders
        placeholders = {
            'rating': 'Rating',
            'review': 'Review',
        }
        # Set autofocus to review field
        self.fields['review'].widget.attrs['autofocus'] = True
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
            # Add review-input class
            self.fields[field_name].widget.attrs[
                'class'] = 'review-input'
