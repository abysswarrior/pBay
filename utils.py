from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI(f'{settings.OTP_SECRET}')
        params = {
            'sender': '10008663',
            'receptor': phone_number,
            'message': f'Your verify code is {code}'
        }
        response = api.sms_send(params)
        print(response)
        return 'ok'
    except APIException as e:
        print(e)
        return 'SMS API Error'
    except HTTPException as e:
        print(e)
        return 'SMS Network Error'


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

