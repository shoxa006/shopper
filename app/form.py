from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.transaction import atomic
from django.forms import ModelForm, Form, EmailField, CharField
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.models import Product, User
from app.views.token import account_activation_token
from root.settings import EMAIL_HOST_USER


class ProductModelForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class LoginForm(AuthenticationForm):
    username = CharField(required=False)
    email = EmailField()
    password = CharField(max_length=155)

    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email not found')
        return email

    def clean_password(self):
        email = self.data.get('email')
        password = self.data.get('password')

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise ValidationError('This password not found')
        return password

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(Form):
    email = EmailField()
    password = CharField(max_length=155)
    confirm_password = CharField(max_length=155)

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Confirm password is wrong')
        return password

    @atomic
    def save(self):
        user = User.objects.create_user(
            email=self.cleaned_data.get('email'),
            is_active=False
        )
        user.set_password(self.cleaned_data.get('password'))
        user.save()


class ForgotPasswordForm(Form):
    email = EmailField()

    # def send_email(self):
    #     email = self.cleaned_data.get('email')
    #     subject = 'xabar'
    #     message = 'qanaqadir xabar'
    #     from_email = EMAIL_HOST_USER
    #     recipient_list = [email]
    #     result = send_mail(subject, message, from_email, recipient_list)
    #     print(result)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email is not registered')
        return email


def send_email(email, request, _type):

    user = User.objects.get(email=email)
    subject = 'Activate your account'
    current_site = get_current_site(request)
    message = render_to_string('app/auth/activation_account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
        'token': account_activation_token.make_token(user),
    })

    from_email = EMAIL_HOST_USER
    recipient_list = [email]

    result = send_mail(subject, message, from_email, recipient_list)
    print('Send to MAIL')

