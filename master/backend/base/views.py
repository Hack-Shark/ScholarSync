from .forms import PrefAddForm
from django.http import JsonResponse
from .models import Preference
def pref_add(request):
    if request.method == 'POST':
        form = PrefAddForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            prefs=Preference.objects.filter(user=request.user).values()
            pref_data=list(prefs)[::-1]
            return JsonResponse({'status':'Save','pref_data':pref_data})
        else:
            return JsonResponse({'status':0})
def get_pref(request):
    if request.method=='GET' :
        prefs=Preference.objects.filter(user=request.user).values()
        pref_data=list(prefs)[::-1]
        return JsonResponse({'status':'Get','pref_data':pref_data})
    else:
        return JsonResponse({'status':0})
    