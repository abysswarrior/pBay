from celery import shared_task
from accounts.models import OtpCode
from datetime import timedelta, datetime
import pytz


@shared_task
def remove_expired_otp_codes():
    expire_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=10)
    OtpCode.objects.filter(created__lt=expire_time).delete()