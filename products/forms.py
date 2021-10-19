from django import forms
from .models import Product, Category


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(category.id, category.get_friendly_name()) for category in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'product-input'
