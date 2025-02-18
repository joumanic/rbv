from django import forms
from .models import RadioShow

class RadioShowForm(forms.ModelForm):
    class Meta:
        model = RadioShow
        fields = ['host_name', 'show_name', 'genre1', 'genre2', 'genre3', 'socials', 'show_date', 'show_image']
        widgets = {
            'show_image': forms.HiddenInput(),  # Hide URL field, handle file upload in view
        }
