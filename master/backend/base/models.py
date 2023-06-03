from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
import uuid 
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Preference(models.Model):
    category=models.ForeignKey(Category,related_name='category',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user_pref',on_delete=models.CASCADE)
    preference=models.CharField(max_length=100,blank=False)
    id=models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at= models.DateField(default=date.today)
    after= models.DateField(blank=False)
    def __str__(self):
        return f'{self.user}\t{self.category}\t{self.preference}\t{self.after}'
    