from django import forms
from datetime import timedelta
from django.contrib import admin
from .models import Frequency, EmailTime


class FrequencyAdminForm(forms.ModelForm):
    time = forms.DurationField(label='Time to mail', initial=timedelta(days=30))
    class Meta:
        model = Frequency
        fields = ('time', 'freq')

class FrequencyAdmin(admin.ModelAdmin):
    form = FrequencyAdminForm

admin.site.register(Frequency,FrequencyAdmin)
admin.site.register(EmailTime)

