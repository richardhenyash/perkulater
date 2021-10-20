from django import forms
from .models import Category, Coffee, Price, Product


class ProductForm(forms.ModelForm):
    """
    A form for products.
    """
    class Meta:
        model = Product
        fields = ('category', 'name', 'friendly_name',
                  'friendly_price', 'description_full',
                  'description_short', 'description_delimiter',
                  'image')                
        labels = {
            'friendly_name': 'Display Name',
            'friendly_price': 'Display Price',
            'description_full': 'Full Description',
            'description_short': 'Short Description',
            'description_delimiter': 'Description Delimiter',
            'image': 'Image File',
            }

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
        self.fields['name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'category' and field != 'image':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'checkout-input'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'product-input'


class CoffeeForm(forms.ModelForm):
    """
    A form for Coffees.
    """
    class Meta:
        model = Coffee
        exclude = ['product']
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
        for field in self.fields:
            if field != 'product':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'coffee-input'
