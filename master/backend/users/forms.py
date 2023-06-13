from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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