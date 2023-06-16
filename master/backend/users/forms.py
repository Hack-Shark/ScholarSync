from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmailTime

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','id':'emailid'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'password'}))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1', 'password2')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control','id':'userid'}),
            'email' : forms.EmailInput(attrs={'class':'form-control','id':'emailid'}),
            'password1' : forms.PasswordInput(attrs={'class':'form-control','id':'pass1'}),
            'password2' : forms.PasswordInput(attrs={'class':'form-control','id':'pass2'}),
        }

class EmailTimeForm(forms.ModelForm):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    freq = forms.ChoiceField(label='Frequency of mails', choices=FREQUENCY_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'freq','disabled':'True'}))
    time = forms.TimeField(label='Time to mail',widget=forms.TimeInput(attrs={'class': 'form-control', 'id': 'timeid', 'type': 'time', 'disabled':'True'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'emailid','placeholder':'if not to registered mail', 'disabled':'True'}))
    
    class Meta:
        model = EmailTime
        fields = ('email', 'time', 'freq')