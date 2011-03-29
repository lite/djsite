from django import forms

from models import Marker

class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        exclude = ('date')