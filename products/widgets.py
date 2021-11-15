from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInputDefault(ClearableFileInput):
    """
    Custom clearable file input for default image
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Default Image')
    input_text = _('')
    template_name = ('products/custom_widget_templates/'
                     'custom_clearable_file_input.html')


class CustomClearableFileInputAlt(ClearableFileInput):
    """
    Custom clearable file input for alternate image
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Alternate Image')
    input_text = _('')
    template_name = ('products/custom_widget_templates/'
                     'custom_clearable_file_input.html')
