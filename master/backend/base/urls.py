from django.urls import path
from . import views

urlpatterns = [
    path('', views.pref_add, name='pref_add'),
    path('get-pref',views.get_pref,name='get_pref'),
    path('del-pref',views.del_pref,name='del_pref'),
    path('edit-pref',views.edit_pref,name='edit_pref'),
]