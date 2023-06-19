import time
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailTime
from datetime import timedelta
from datetime import datetime
def send_email(email, subject, message):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def schedule_emails():
    email_times = EmailTime.objects.all()
    print("hi")
    while True:
        current_time = time.strftime('%H:%M:%S')  

        for email_time in email_times:
            time_to_send = email_time.time.strftime('%H:%M:%S')
            frequency = email_time.freq.time
            email = email_time.email
            subject = "Your email subject"
            message = "Your email message"

            if current_time == time_to_send:
                send_email(email=email, subject=subject, message=message)

                # Update the time to send for the next email
                new_time = (datetime.combine(datetime.today(), email_time.time) + frequency).time()
                email_time.time = new_time
                email_time.save()

        time.sleep(1)  

