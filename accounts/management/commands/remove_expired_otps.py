from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import timedelta, datetime
import pytz


class Command(BaseCommand):
    help = "Remove all expired otp codes"

    def handle(self, *args, **options):
        expire_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=10)
        OtpCode.objects.filter(created__lt=expire_time).delete()
        self.stdout.write(self.style.SUCCESS("All expired otp code deleted successfully"))