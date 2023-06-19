from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, EmailTimeForm
from django.contrib.auth.models import User
from base.forms import PrefAddForm
from base.models import Preference
from django.contrib import messages
from .models import EmailTime,Frequency
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.conf import settings
# home view
def home(request):
    form=PrefAddForm()
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        pref_data=Preference.objects.filter(user=request.user).values()
        pref_data=list(pref_data)[::-1]
        return render(request, 'home.html',{'form':form,'pref_data':pref_data})
    
# login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj=User.objects.filter(email=email).first()
            if(user_obj is not None):
                user = authenticate(request,username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('home') 
                else:
                    messages.success(request, 'Password invalid')
            else:
                messages.success(request, 'Email or Password invalid')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')  
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'title':'Register','form': form})

frequency, created = Frequency.objects.get_or_create(freq="daily", time=timedelta(days=1))
# profile view
@login_required
def profile_view(request):
    email_time, created = EmailTime.objects.get_or_create(user=request.user)
    email_time.email = request.user.email if request.user.email else settings.DEFAULT_EMAIL
    email_time.freq = frequency
    email_time.save()
    if request.method == 'POST':
        form = EmailTimeForm(request.POST, instance=email_time)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        form = EmailTimeForm(instance=email_time)
    return render(request, 'users/profile.html', {'title':'Profile','user': request.user, 'form': form})
