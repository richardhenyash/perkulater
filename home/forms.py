from django import forms


class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True, max_length=100)
    message = forms.CharField(required=True, widget=forms.Textarea)
