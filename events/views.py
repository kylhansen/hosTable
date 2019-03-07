# events/views.py

from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from .models import Event, Invitation
from .forms import EventCreateForm, InvitationResponseForm, InvitationFoodForm, EventUpdateForm
from users.models import Profile, RestrictionTag
from menus.models import Food
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
        rsvp_date = form.instance.RSVP_date
        event_date = form.instance.event_date
        try:
            if not RSVP_date < event_date:
                raise forms.ValidationError(
                    'RSVP date must be prior to event date.'
                )
        except:
            if RSVP_date is None:
                raise forms.ValidationError(
                    'RSVP date is not a valid date.'
                )
            if event_date is None:
                raise forms.ValidationError(
                    'Event date is not a valid date.'
                )
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Your event has been updated!')
        return reverse('event-list-host', args=(self.request.user.id,))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(EventUpdateView, self).get_form_kwargs()
        event = self.get_object()
        # invited_users = event.guests.all().distinct()
        # uninvited_users = User.objects.exclude(id__in=[guest.id for guest in invited_users] + [self.request.user.id])
        kwargs.update({'request': self.request})  # , 'uninvited_users': uninvited_users})
        return kwargs

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
        if event.host == user:
            context['hosting'] = True
            unresponsive = Invitation.objects.filter(event=event, replied=False)
            attending = Invitation.objects.filter(event=event, replied=True, attending=True)
            context['invitations_unresponsive'] = unresponsive
            context['invitations_attending'] = attending
            context['invitations_not_attending'] = Invitation.objects.filter(event=event, replied=True, attending=False)
            potential_profiles = Profile.objects.filter(Q(user__in=unresponsive.values_list('guest').distinct())
                                                        | Q(user__in=attending.values_list('guest').distinct()))
            context['restrictions'] = RestrictionTag.objects.filter(id__in=potential_profiles.values_list('restrictions').distinct())
            # TODO:
            #  get the profile of each guest in attendance
            #  use this profile to get the dietary restrictions of each guest
            #  and then pass that list on to the context
            #possible_invitations = Invitation.objects.filter(Q(event=event), Q(replied=False) | Q(replied=True, attending=True))
        else:
            rsvp = Invitation.objects.get(event=event, guest=user)
            context['food'] = rsvp.food
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
        instance = self.get_object()
        if not instance.attending:
            messages.success(self.request, 'You have declined this event. Check out your other events below!')
            return reverse('event-list-guest', args=('attending', self.request.user.id))
        else:
            messages.success(self.request, 'Your response has been saved. Please select a food item to provide.')
            return reverse('event-response-food', args=(instance.pk,))

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


class InvitationFoodView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invitation
    form_class = InvitationFoodForm

    def get_success_url(self):
        messages.success(self.request, 'Your RSVP is complete!')
        return reverse('event-list-guest', args=('attending', self.request.user.id))

    def get_context_data(self, **kwargs):
        context = super(InvitationFoodView, self).get_context_data(**kwargs)
        context['event'] = self.get_object().event
        return context

    def test_func(self):
        user = self.request.user
        invitation = self.get_object()
        if user == invitation.guest and invitation.attending:
            return True
        return False

    def get_form_kwargs(self, **kwargs):
        kwargs = super(InvitationFoodView, self).get_form_kwargs()
        menu_foods = self.get_object().event.menu.foods.all()
        invitations = Invitation.objects.filter(event=self.get_object().event).filter(food__isnull=False)
        used_foods = menu_foods.filter(id__in=invitations.values_list('food')).distinct()
        foods = menu_foods.exclude(id__in=[food.id for food in used_foods])
        kwargs.update({'foods': foods})
        return kwargs
