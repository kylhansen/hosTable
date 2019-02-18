# events/views.py

from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Invitation
from .forms import EventCreateForm, InvitationResponseForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class EventCreateView(LoginRequiredMixin, CreateView):
    form_class = EventCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Your event has been created!')
        return reverse('event-list-host', args=(self.request.user.id,))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(EventCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title',
              'menu',
              'event_location',
              'event_date',
              'event_time',
              'RSVP_date',
              ]

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.host:
            return True
        return False


class EventDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Event

    def test_func(self):
        user = self.request.user
        event = Event.objects.get(id=self.kwargs['pk'])
        if user in event.guests.all() or user == event.host:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        event = Event.objects.get(id=self.kwargs['pk'])
        signups = SignUp.objects.get(event=event)
        if event.host == user:
            context['hosting'] = True
        else:
            rsvp = Invitation.objects.get(event=event, guest=user)
            context['RSVP_id'] = rsvp.id
            context['RSVP_replied'] = rsvp.replied
        return context


class EventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event

    def test_func(self):
        viewer = self.request.user
        user = User.objects.get(id=self.kwargs['user_id'])
        if viewer == user:
            return True
        return False


class EventHostListView(EventListView):

    def get_queryset(self):
        host = self.kwargs['user_id']
        return Event.objects.filter(host=host)

    def get_context_data(self, **kwargs):
        context = super(EventHostListView, self).get_context_data(**kwargs)
        context['status'] = 'hosting'
        return context


class EventGuestListView(EventListView):

    def get_queryset(self):
        RSVP_status = self.kwargs['RSVP_status']
        guest = self.kwargs['user_id']

        RSVP_filter = {
            'new': Invitation.objects.filter(guest=guest, replied=False),
            'attending': Invitation.objects.filter(guest=guest, attending=True),
            'all': Invitation.objects.filter(guest=guest),
        }
        invitation = RSVP_filter[RSVP_status]
        return Event.objects.filter(invitation__in=invitation)

    def get_context_data(self, **kwargs):
        context = super(EventGuestListView, self).get_context_data(**kwargs)
        context['status'] = self.kwargs.get('RSVP_status')
        return context


class InvitationResponseView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invitation
    form_class = InvitationResponseForm

    def get_success_url(self):
        messages.success(self.request, 'You have successfully RSVPed. Check out your current events below!')
        return reverse('event-list-guest', args=('attending', self.request.user.id))

    def get_context_data(self, **kwargs):
        context = super(InvitationResponseView, self).get_context_data(**kwargs)
        context['event'] = self.get_object().event
        return context

    def test_func(self):
        user = self.request.user
        invitation = self.get_object()
        if user == invitation.guest:
            return True
        return False
