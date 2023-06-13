from .forms import PrefAddForm
from django.http import JsonResponse
from .models import Preference
from backend.settings import EMAIL_HOST_USER
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def pref_add(request):
    if request.method == 'POST':
        form = PrefAddForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            prefs=Preference.objects.filter(user=request.user).values()
            pref_data=list(prefs)[::-1]
            print(pref_data)
            return JsonResponse({'status':'Save','pref_data':pref_data})
        else:
            for field, errors in form.errors.items():
                print(f"{field}: {', '.join(errors)}")
            return JsonResponse({'status':0})

def get_pref(request):
    if request.method=='GET' :
        prefs=Preference.objects.filter(user=request.user).values()
        pref_data=list(prefs)[::-1]
        # mail_send(data={'data':"Hi from moki"},website="bahubali",recipents=['mssrinu004@gmail.com'])
        return JsonResponse({'status':'Get','pref_data':pref_data})
    else:
        return JsonResponse({'status':0})

def mail_send(data,recipents,website):
    sub=f"Your weekly feed from {website}"
    html_message = render_to_string('email.html', data)
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(
    subject=sub,
    body=plain_message,
    from_email=EMAIL_HOST_USER,
    to=recipents,
    )
    email.attach_alternative(html_message,"text/html")
    email.send()