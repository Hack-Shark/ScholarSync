from django import forms
from .models import Preference

class PrefAddForm(forms.ModelForm):
    class Meta:
        model =  Preference
        fields = ['text','after']
        widgets = {
            'text' : forms.TextInput(attrs={'class':'form-control','id':'text'}),
            'after' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id':'after'}),
        }