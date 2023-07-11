from django import forms
from .models import Preference
from datetime import date

class PrefAddForm(forms.ModelForm):
    YEARS_CHOICES =[(None, 'Enter the Year')]+[(year, year) for year in range(1900, date.today().year + 1)]
    
    after = forms.ChoiceField(choices=YEARS_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'after'}))

    class Meta:
        model = Preference
        fields = ['text', 'after']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'id': 'text'}),
        }
