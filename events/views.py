# events/views.py

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event
from .forms import EventCreateForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class EventCreateView(LoginRequiredMixin, CreateView):
  template_name = "events/create.html"
  form_class = EventCreateForm

  def form_valid(self, form):
    form.instance.host = self.request.user
    return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Event
  template_name = "events/update.html"
  fields = ['title',
            'event_location',
            'event_date',
            'event_time',
            'RSVP_date',
            ]

  def form_valid(self, form):
    form.instance.host = self.request.user
    return super().form_valid(form)


class EventDetailView(DetailView):
  model = Event
  template_name = 'events/view.html'
