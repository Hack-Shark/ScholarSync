import time
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import EmailTime
from datetime import datetime
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from base.cache_builder import get_links
from base.models import CombinedText
from base.utils import process_articles,article_data


def send_email(email, subject,link_data):
    # Render the HTML template
    html_content = render_to_string('email.html', {'link_data': link_data})
    # Strip HTML tags for the text version of the email
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    # Attach the HTML content to the email
    msg.attach_alternative(html_content, "text/html")

    msg.send()


def schedule_emails():
    print('sending mails')
    while True:
        current_time = datetime.now().time()
        current_hour = current_time.hour
        # current_minute = current_time.minute

        email_times = EmailTime.objects.all()

        for email_time in email_times:
            email = email_time.email
            email_hour = email_time.time.hour
            # email_minute = email_time.time.minute

            if current_hour == email_hour:
                user=email_time.user
                mailing_time = time.time()
                text=CombinedText.objects.get(user=user).combined_text
                related_links=get_links(text)
                print(f'time to get links = {time.time()-mailing_time}')
                top5_links=process_articles(related_links,user)
                print(f'time to process links = {time.time()-mailing_time}')                
                link_data=[]
                for link in top5_links:
                    link_data.append(article_data(link))
                print(link_data)
                print(f'time to get link_data = {time.time()-mailing_time}')
                print(f'got links in {time.time()-mailing_time}')
                subject = "Your weekly feed from Scholar Sync"
                message = "Your weekly feed from Scholar Sync"

                send_email(email=email, subject=subject,link_data=link_data)
                print(f'sent mail to {email} at {current_time} in {time.time()-mailing_time}')
            # Update the time to send for the next email
            new_time = (datetime.combine(datetime.today(), email_time.time) + email_time.freq.time).time()
            email_time.time = new_time
            email_time.save()

        time.sleep(60)  # Sleep for 1 minute

