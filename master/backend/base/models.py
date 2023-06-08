from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
import uuid 

class Preference(models.Model):
    user=models.ForeignKey(User,related_name='user_pref',on_delete=models.CASCADE)
    text=models.CharField(max_length=100,blank=False)
    id=models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at= models.DateField(default=date.today)
    after= models.DateField(blank=False)
    def __str__(self):
        return f'{self.user}\t{self.text}\t{self.after}'
    