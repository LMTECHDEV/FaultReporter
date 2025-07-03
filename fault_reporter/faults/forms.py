from django import forms
from .models import Fault

class FaultForm(forms.ModelForm):
    class Meta:
        model = Fault
        fields = ['location', 'description', 'image1', 'image2', 'image3', 'image4', 'image5']