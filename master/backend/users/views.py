from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from base.forms import PrefAddForm
from base.models import Preference
from django.http import JsonResponse
from .models import EmailTime
from .forms import EmailTimeForm

# Home page view
def home_view(request):
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
    return render(request, 'user/login.html', {'form': form})

# signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

# logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# email sending time view
def emailTime_view(request):
    if request.method == 'POST':
        form = EmailTimeForm(request.POST)
        if form.is_valid():
            pref = request.POST.get('pref')
            email = request.POST.get('email')
            time = request.POST.get('time')
            # Create an EmailTime object and save it
            email_time = EmailTime(email=email, time=time, pref=pref)
            email_time.save()
            time_data=EmailTime.objects.values()
            time_data=list(time_data)[::-1]
            return JsonResponse({'status': 1,'time_data':time_data})
    return JsonResponse({'status': 0})
