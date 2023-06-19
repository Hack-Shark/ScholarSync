from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import timedelta

class Frequency(models.Model):
    freq=models.CharField(max_length=10)
    time = models.DurationField(default=timedelta(days=1))
    def __str__(self):
        return f'{self.time}\t{self.freq}'
class EmailTime(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    email = models.EmailField()
    time = models.TimeField(default=datetime.time())
    freq = models.ForeignKey(Frequency, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.time}\t{self.email}\t{self.freq}'