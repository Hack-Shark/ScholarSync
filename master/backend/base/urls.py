from django.urls import path

from . import views

urlpatterns = [
    path('', views.pref_add, name='pref_add'),
]