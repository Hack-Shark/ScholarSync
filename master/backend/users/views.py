from django.shortcuts import render, redirect
from .forms import SignupForm, EmailTimeForm
from base.forms import PrefAddForm
from base.models import Preference
from django.contrib import messages
from .models import EmailTime
from django.contrib.auth.decorators import login_required

def home(request):
    form=PrefAddForm()
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        pref_data=Preference.objects.filter(user=request.user).values()
        pref_data=list(pref_data)[::-1]
        return render(request, 'home.html',{'form':form,'pref_data':pref_data})

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

# profile view
@login_required
def profile_view(request):
    email_time, created = EmailTime.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EmailTimeForm(request.POST, instance=email_time)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        form = EmailTimeForm(instance=email_time)
    return render(request, 'users/profile.html', {'title':'Profile','user': request.user, 'form': form})
