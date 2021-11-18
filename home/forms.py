from django import forms


class ContactForm(forms.Form):
    """
    A general contact form
    """
    def __init__(self, *args, **kwargs):
        """
        Set placeholders
        """
        super().__init__(*args, **kwargs)
        self.fields['from_email'].widget.attrs['placeholder'] = 'Email'
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'

    from_email = forms.EmailField(required=True, max_length=254, label='Email')
    subject = forms.CharField(required=True, max_length=100)
    message = forms.CharField(required=True, widget=forms.Textarea)
