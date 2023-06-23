import os
import subprocess
from django.contrib.auth import get_user_model
from decouple import config
from users.scheduler import schedule_emails
User = get_user_model()
username = config('USERNAME')
email = config('EMAIL')
password = config('PASSWORD')

def mails():
    try:
        user = User.objects.get(username=username)
        print('Superuser already exists.')
    except User.DoesNotExist:
        user = User.objects.create_superuser(username, email, password)
        print('Superuser created successfully:', user)
    
    schedule_emails()

    print("Done")

mails()
