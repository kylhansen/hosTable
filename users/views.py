# users/viess.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save(*args, **kwargs)
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('user-login')
        else:
            form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form = ProfileUpdateForm
    template_name = 'users/update.html'
    fields = ['first', 'last']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    '''
    def post(self, request, *args, **kwargs):
        u_form_class = UserUpdateForm
        p_form_class = ProfileUpdateForm
        if request.method == 'POST':
            u_form = self.u_form_class(request.POST, instance=request.user)
            p_form = self.p_form_class(request.POST, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save(*args, **kwargs)
                p_form.save(*args, **kwargs)
                messages.success(request, f'Your account has been updated!')
                return redirect('users-profile')
        else:
            u_form = self.u_form_class(instance=request.user)
            p_form = self.p_form_class(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'profile': request.user.profile,
        }
        return render(request, 'users/profile.html', context)
    '''

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False
