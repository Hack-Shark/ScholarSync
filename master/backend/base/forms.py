from django import forms
from .models import Preference

class PrefAddForm(forms.ModelForm):
    class Meta:
        model =  Preference
        fields = ['text','after']