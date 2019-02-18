# users/views.py

# Email sending template taken from:
#   https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, UserUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your hostable account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, f'Please check your email to validate your account!')
                return redirect('user-login')
        else:
            form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Profile

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f'Your account has been verified. You may now log in.')
        return redirect('user-login')
    else:
        return HttpResponse('Activation link is invalid!')
