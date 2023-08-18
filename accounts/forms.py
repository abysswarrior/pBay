from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        """
        Check that the two password entries match
        """
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password dose not match')
        return cd['password2']

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text=
                                         "You can change your password using <a href=\"../password/\">this link</a>")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    email = forms.EmailField()
    full_name = forms.CharField(max_length=100, label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        is_email_exists = User.objects.filter(email=email).exists()
        if is_email_exists:
            raise ValidationError("Email already exists")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        is_phone_number_exists = User.objects.filter(phone_number=phone_number).exists()
        if is_phone_number_exists:
            raise ValidationError('Phone number already exists')
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number


class UserVerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
