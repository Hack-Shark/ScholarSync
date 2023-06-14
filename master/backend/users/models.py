from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     forget_password_token=models.CharField(max_length=100)
#     created_at=models.DateTimeField(auto_now_add=True)
    
#     def __str__(self) -> str:
#         return self.user.username

class EmailTime(models.Model):
    email = models.EmailField()
    time = models.TimeField()
    pref = models.TextField()

    def __str__(self):
        return f'{self.pref}\t{self.time}\t{self.email}'