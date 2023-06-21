from django.contrib import admin
from .models import Preference,CombinedText,Article,UserArticle

# Register your models here.
admin.site.register(Preference)
admin.site.register(CombinedText)
admin.site.register(Article)
admin.site.register(UserArticle)