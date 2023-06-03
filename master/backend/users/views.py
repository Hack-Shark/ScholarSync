from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'home.html')
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home') 
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

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
