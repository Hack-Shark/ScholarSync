from .forms import PrefAddForm
from django.http import JsonResponse
from .models import Preference
from .cache_builder import compare_user_input_with_tags
import time

def pref_add(request):
    print(request)
    print(request.POST)
    if request.method == 'POST':
        form = PrefAddForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            start_time =time.time()
            # print(get_links(obj.text))
            validity = compare_user_input_with_tags(obj.text)
            print(validity)
            print(time.time()-start_time)
            if validity == 'valid':
                obj.save()
                prefs=Preference.objects.filter(user=request.user).values()
                pref_data=list(prefs)[::-1]
                # print(pref_data)
                message=f'"{obj.text}" added to your prefernces'
                return JsonResponse({'status':'Save','pref_data':pref_data,'message':message})
            else:
                prefs=Preference.objects.filter(user=request.user).values()
                pref_data=list(prefs)[::-1]
                message=f'No records found for the input "{obj.text}"'
                return JsonResponse({'status':'invalid','pref_data':pref_data,'message':message})
        else:
            for field, errors in form.errors.items():
                print(f"{field}: {', '.join(errors)}")
            return JsonResponse({'status':0})

# def get_pref(request):
#     if request.method=='GET' :
#         prefs=Preference.objects.filter(user=request.user).values()
#         pref_data=list(prefs)[::-1]
        
#         # mail_send(data={'data':"Hi from moki"},website="bahubali",recipents=['mssrinu004@gmail.com'])
#         return JsonResponse({'status':'Get','pref_data':pref_data})
#     else:
#         return JsonResponse({'status':0})
    
def del_pref(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        print(id)
        dp = Preference.objects.filter(user=request.user).get(id=id)
        dp.delete()
        prefs=Preference.objects.filter(user=request.user).values()
        pref_data=list(prefs)[::-1]
        return JsonResponse({'status':1,'pref_data':pref_data})
    else:
        return JsonResponse({'status':0})

def edit_pref(request):
    if request.method == 'POST':
        print(request.POST)
        id = request.POST.get('id','')
        text = request.POST.get('text','')
        date = request.POST.get('date','')
        pref= Preference.objects.filter(user=request.user).get(id=id)
        print(pref)
        pref.text=text
        pref.after=date
        pref.save()
        return JsonResponse({'success':"Updated"})
