from django.urls import path

from . import views

urlpatterns = [
    path('', views.pref_add, name='pref_add'),
    path('get',views.get_pref,name='get_pref')
]