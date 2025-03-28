from django import forms
from .models import RadioShow

class RadioShowForm(forms.ModelForm):
    class Meta:
        model = RadioShow
        fields = ['email', 'host_name', 'show_name', 'genre1', 'genre2', 'genre3', 'socials', 'show_date', 'show_image_url', 'pre_record_url']
        widgets = {
            'show_image_url': forms.HiddenInput(),
            'pre_record_url': forms.HiddenInput(),  # Hide URL field, handle file upload in view
        }
