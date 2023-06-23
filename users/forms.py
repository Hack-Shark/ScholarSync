from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmailTime
from .models import Frequency


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','id':'emailid'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'password'}))

class SignupForm(UserCreationForm):
    email=forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username','email','password1', 'password2')

class EmailTimeForm(forms.ModelForm):
    freq = forms.ModelChoiceField(
        label='Frequency of mails',
        queryset=Frequency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'freq', 'disabled': 'True'})
    )
    
    time = forms.TimeField(label='Time to mail',widget=forms.TimeInput(attrs={'class': 'form-control', 'id': 'timeid', 'type': 'time', 'disabled':'True'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'emailid','placeholder':'if not to registered mail', 'disabled':'True'}))
    
    class Meta:
        model = EmailTime
        fields = ('email', 'time', 'freq')
    
 