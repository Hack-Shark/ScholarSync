import time
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import EmailTime
from datetime import datetime, timedelta
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from base.cache_builder import get_links
from base.models import CombinedText
from base.utils import process_articles, article_data


def send_email(email, subject, link_data):
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

        email_times = EmailTime.objects.filter(time__hour=current_hour)

        for email_time in email_times:
            email = email_time.email
            user = email_time.user
            mailing_time = time.time()
            text = CombinedText.objects.get(user=user).combined_text
            related_links = get_links(text)
            print(f'time to get links = {time.time()-mailing_time}')
            top5_links = process_articles(related_links, user)
            print(f'time to process links = {time.time()-mailing_time}')
            link_data = [article_data(link) for link in top5_links]
            print(link_data)
            print(f'time to get link_data = {time.time()-mailing_time}')
            print(f'got links in {time.time()-mailing_time}')
            subject = "Your Daily feed from Scholar Sync"

            send_email(email=email, subject=subject, link_data=link_data)
            print(f'sent mail to {email} at {current_time} in {time.time()-mailing_time}')

            # Update the time to send for the next email
            next_email_time = datetime.combine(datetime.today(), email_time.time) + email_time.freq.time
            email_time.time = next_email_time.time()
            email_time.save()

        # Calculate the remaining time until the next mailing
        next_mailing_time = EmailTime.objects.filter(time__hour=current_hour).order_by('time').first()
        if next_mailing_time:
            remaining_time = datetime.combine(datetime.today(), next_mailing_time.time) - datetime.now()
        else:
            # No email time found for the current hour, sleep for 1 minute and check again
            remaining_time = timedelta(minutes=1)

        # Sleep for the remaining time until the next mailing
        sleep_duration = max(remaining_time.total_seconds(), 60)
        time.sleep(sleep_duration)

