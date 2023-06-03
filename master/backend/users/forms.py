from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username or password.")
        return cleaned_data

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')