from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from app.form import LoginForm, RegisterForm, ForgotPasswordForm, send_email


# def login_view(request):
#     form = LoginForm()
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:
#         if request.method == "POST":
#             form = LoginForm(request.POST)
#             if form.is_valid():
#                 user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
#                 if user:
#                     if user.is_active:
#                         login(request, user)
#                         return redirect('index')
#                     else:
#                         messages.add_message(
#                             request,
#                             level=messages.WARNING,
#                             message='user is not active'
#                         )
#                         return redirect('login')
#
#     return render(request, 'app/auth/login.html', {"form":form})


class LoginMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(self,request, *args, **kwargs)


class LoginPage(LoginMixin, LoginView):
    form_class = LoginForm
    template_name = 'app/auth/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return render(request, 'app/auth/logout.html')


# def register_view(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             send_email(form.data.get('email'), request, 'register')
#             messages.add_message(
#                 request,
#                 level=messages.WARNING,
#                 message='Successfully send your email, please activate your profile'
#             )
#             return redirect('register')
#
#     return render(request, 'app/auth/register.html', {"form":form})


class RegisterPage(LoginMixin, FormView):
    form_class = RegisterForm
    template_name = 'app/auth/register.html'
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        form.save()
        current_site = get_current_site(self.request)
        send_email(form.data.get('email'), self.request, 'register')
        messages.add_message(
            self.request,
            level=messages.WARNING,
            message='Successfully send your email, please activate your profile'
        )
        return super().form_valid(form)


class ForgotPasswordView(FormView):
    form_class = ForgotPasswordForm
    template_name = 'app/auth/forgot_password.html'
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     form.send_email()
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     send_email(form.data.get('email'), self.request, 'forgot')
    #     return super().form_valid(form)

    def form_valid(self, form):
        current_site = get_current_site(self.request)
        send_email(form.data.get('email'), self.request, 'forgot')
        return super().form_valid(form)




# def confirm(request):
#     return render(request, 'app/auth/confirm_email.html')




