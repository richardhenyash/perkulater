from django import forms


class ContactForm(forms.Form):
    """
    A general contact form
    """

    from_email = forms.EmailField(required=True, max_length=254, label='Email')
    subject = forms.CharField(required=True, max_length=100)
    message = forms.CharField(required=True, widget=forms.Textarea)
