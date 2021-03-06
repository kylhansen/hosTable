# menus/view.py

from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from .models import Menu, Food
from .forms import MenuCreateForm, FoodCreateForm, ProportionMenuFormSet, ProportionalMenuCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class MenuCreateView(LoginRequiredMixin, CreateView):

    form_class = MenuCreateForm

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(MenuCreateView, self).get_form_kwargs()
        form_kwargs.update({
            'user': user,
        })
        return form_kwargs

    def get_success_url(self):
        messages.success(self.request, 'Your menu has been created!')
        return reverse('home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class MenuUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Menu
    fields = [
        'name',
        'categories',
    ]


class FoodCreateView(CreateView):

    form_class = FoodCreateForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Your food item has been created!')
        return reverse('home')


class ProporitionMenuCreateView(CreateView):

    form_class = ProportionalMenuCreateForm

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(ProporitionMenuCreateView, self).get_form_kwargs()
        form_kwargs.update({
            'user': user,
        })
        return form_kwargs

    def get_context_data(self, **kwargs):
        data = super(ProporitionMenuCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['proportions'] = ProportionMenuFormSet(self.request.POST)
        else:
            data['proportions'] = ProportionMenuFormSet()
        return data

    def form_valid(self, form):
        form.instance.creator = self.request.user
        context = self.get_context_data()
        proportions = context['proportions']
        self.object = form.save()

        if proportions.is_valid():
            proportions.instance = self.object
            proportions.save()
        return super(ProporitionMenuCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Your menu has been created!')
        return reverse('home')

    '''
    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['add_category_url'] = reverse('menu-category-add')

    def update_project_filter(request):
        current_url = request.get_full_path()
        request.session['create_menu_url'] = current_url



class CategoryCreateView(CreateView):
    model = Category
    fields = [
        'name',
    ]


    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['add_food_url'] = reverse('menu-food-add')

    def update_project_filter(request):
        current_url = request.get_full_path()
        request.session['add_category_url'] = current_url

    def update_project(request):
        context = RequestContext(request)
        context['cancel_url'] = request.session['create_menu_url']
    '''

    '''
    success_url = reverse('menu-category-view')

    def update_project(request):
        context = RequestContext(request)
        context['cancel_url'] = request.session['add_category_url']
    '''
