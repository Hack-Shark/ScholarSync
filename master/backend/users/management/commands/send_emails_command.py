from django.core.management.base import BaseCommand
from users.scheduler import schedule_emails
class Command(BaseCommand):
    help = 'Schedules and sends emails'

    def handle(self, *args, **options):
        
        schedule_emails()
