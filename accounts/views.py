from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserVerifyCodeForm, UserLoginForm
from .models import OtpCode, User
import random
from utils import send_otp_code
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = random.randint(1000, 9999)
            sms_status = send_otp_code(cd['phone_number'], code)
            if sms_status != 'ok':
                messages.error(request, sms_status, "danger")
                return render(request, self.template_name, {'form': form})
            OtpCode.objects.create(phone_number=cd['phone_number'], code=code)
            request.session['user_registration_info'] = {
                'email': cd['email'],
                'phone_number': cd['phone_number'],
                'full_name': cd['full_name'],
                'password': cd['password'],
            }
            messages.success(request, "Code send to Your phone number", "success")
            return redirect("accounts:verify_code")
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = UserVerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_info = request.session['user_registration_info']
            code_instance = OtpCode.objects.get(phone_number=user_info['phone_number'])
            if cd['code'] == code_instance.code:
                current_time = timezone.now()
                otp_code_time = code_instance.created
                if current_time > otp_code_time + timedelta(minutes=5):
                    code_instance.delete()
                    messages.error(request, "verify code expired. try another time", "danger")
                    return redirect("accounts:user_register")
                else:
                    User.objects.create_user(user_info['phone_number'], user_info['email'], user_info['full_name']
                                             , user_info['password'])
                    code_instance.delete()
                    messages.success(request, "user created successfully", "success")
                    return redirect("home:home")
            else:
                messages.error(request, "code is wrong", "danger")
                return redirect("accounts:verify_code")

        return redirect("home:home")


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You Logged out Successfully")
        return redirect("home:home")


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "User Logged in Successfully", "success")
                return redirect("home:home")
            messages.error(request, "Phone number or password is wrong!", "danger")
            return redirect("accounts:login")
        return render(request, self.template_name, {"form": form})
