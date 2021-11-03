from django import forms
from .widgets import CustomClearableFileInput
from .models import Category, Coffee, Product, Price, Review


class ProductForm(forms.ModelForm):
    """
    A form for products.
    """
    class Meta:
        model = Product
        fields = (
            'category', 'name', 'friendly_name',
            'friendly_price', 'description_full',
            'description_short', 'description_delimiter',
            'image'
        )

        labels = {
            'friendly_name': 'Display Name',
            'friendly_price': 'Display Price',
            'description_full': 'Full Description',
            'description_short': 'Short Description',
            'description_delimiter': 'Description Delimiter',
            'image': 'Image',
        }

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(category.id, category.get_friendly_name()) for category in categories]
        self.fields['category'].choices = friendly_names
        placeholders = {
            'name': 'Name',
            'friendly_name': 'Friendly Name',
            'friendly_price': 'Friendly Price',
            'description_full': 'Full Description',
            'description_short': 'Short Description',
            'description_delimiter': 'Description Delimiter',
        }
        for field_name, placeholder in placeholders.items():
            if self.fields[field_name].required:
                placeholder_text = placeholder + "*"
            else:
                placeholder_text = placeholder
            self.fields[field_name].widget.attrs[
                'placeholder'] = placeholder_text
            self.fields[field_name].widget.attrs[
                'class'] = 'product-input'


class CoffeeForm(forms.ModelForm):
    """
    A form for Coffees.
    """
    class Meta:
        model = Coffee
        fields = (
            'country', 'farm', 'owner',
            'variety', 'altitude',
            'town', 'region',
            'flavour_profile'
        )
        labels = {
            'country': 'Country Of Origin',
            'flavour_profile': 'Flavour Profile',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
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

        self.fields['country'].widget.attrs['autofocus'] = True
        for field_name, placeholder in placeholders.items():
            if self.fields[field_name].required:
                placeholder_text = placeholder + "*"
            else:
                placeholder_text = placeholder
            self.fields[field_name].widget.attrs[
                'placeholder'] = placeholder_text
            self.fields[field_name].widget.attrs[
                'class'] = 'coffee-input'


class PriceForm(forms.ModelForm):
    """
    A form for Prices.
    """
    class Meta:
        model = Price
        fields = ('size', 'price')
        labels = {
            'size': 'Size',
            'price': 'Price £',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on price field
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
        model = Review
        fields = ('rating', 'review')
        labels = {
            'rating': 'Rating',
            'review': 'Review',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'rating': 'Rating',
            'review': 'Review',
        }

        self.fields['review'].widget.attrs['autofocus'] = True
        for field_name, placeholder in placeholders.items():
            if self.fields[field_name].required:
                placeholder_text = placeholder + "*"
            else:
                placeholder_text = placeholder
            self.fields[field_name].widget.attrs[
                'placeholder'] = placeholder_text
            self.fields[field_name].widget.attrs[
                'class'] = 'review-input'
