from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
import os


class Command(BaseCommand):
    help = "help"

    def handle(self, *args, **options):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        if not User.objects.filter(username="admin").exists():
            supassword = os.environ.get('SU_PASSWORD')
            User.objects.create_superuser("admin", "elias@taskoftheday.com.com", supassword)
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
