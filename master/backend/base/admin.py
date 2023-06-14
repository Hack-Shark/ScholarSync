from django.contrib import admin
from .models import Preference
from users.models import EmailTime
# Register your models here.
admin.site.register(Preference)
admin.site.register(EmailTime)