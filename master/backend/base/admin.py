from django.contrib import admin
from .models import Preference,CombinedText

# Register your models here.
admin.site.register(Preference)
admin.site.register(CombinedText)
