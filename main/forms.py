from django import forms
from .models import Paths


class PathsForm(forms.ModelForm):
    dest_url = forms.CharField(required=True)
    
    class Meta:
        model = Paths
        fields = ['dest_url']
