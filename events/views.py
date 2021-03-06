# events/views.py

import operator
from functools import reduce
from django.shortcuts import render, redirect, reverse
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from .models import Event, Invitation
from .forms import EventCreateForm, InvitationResponseForm, InvitationFoodForm, EventUpdateForm
from users.models import Profile, RestrictionTag
from menus.models import Food, Proportion
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from taggit.models import Tag
import math
import itertools


def get_top_guests(host, max_num):
    past_events = Event.objects.filter(host=host)
    top_guests = Invitation.objects.exclude(guest=host).filter(event__in=past_events) \
        .values('guest') \
        .annotate(num_invites=Count('guest')) \
        .order_by('-num_invites')
    result = top_guests[:max_num].values_list('guest', flat=True)
    return result


class EventCreateView(LoginRequiredMixin, CreateView):
    form_class = EventCreateForm

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        host = self.request.user
        top_guests = get_top_guests(host, 5)
        # top_guest_names = top_guests.values_list('username')
        top_guests = User.objects.filter(id__in=top_guests)
        context['top_guests'] = list(top_guests.values_list('username', flat=True))  # top_guest_names
        return context

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
            if not rsvp_date < event_date:
                raise forms.ValidationError(
                    'RSVP date must be prior to event date.'
                )
        except:
            if rsvp_date is None:
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
            # possible_invitations = Invitation.objects.filter(Q(event=event), Q(replied=False) | Q(replied=True, attending=True))
        else:
            unresponsive = Invitation.objects.filter(event=event, replied=False)
            attending = Invitation.objects.filter(event=event, replied=True, attending=True)
            context['invitations_unresponsive'] = unresponsive
            context['invitations_attending'] = attending
            context['invitations_not_attending'] = Invitation.objects.filter(event=event, replied=True, attending=False)
            potential_profiles = Profile.objects.filter(Q(user__in=unresponsive.values_list('guest').distinct())
                                                        | Q(user__in=attending.values_list('guest').distinct()))
            context['restrictions'] = RestrictionTag.objects.filter(id__in=potential_profiles.values_list('restrictions').distinct())
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
        menu = self.get_object().event.menu
        menu_foods = menu.foods.all()
        menu_proportions = Proportion.objects.filter(menu=menu)
        if menu_proportions:
            # TODO : FIX THE TAG SELECTORS AND MAKE SURE THIS FILTERS ONLY THOSE TAGS IN USE
            valid_tags = get_valid_tags(menu, menu_proportions)
            tags = list()
            for tag in valid_tags:
                tags.append(Tag.objects.get(id=tag))
            try:
                required_tags = get_required_tags(menu)
                theme = list()
                for tag in required_tags:
                    theme.append(Tag.objects.get(id=tag))
                context['theme'] = theme
            except:
                pass
            context['tags'] = tags
            context['tagged_event'] = True
        return context

    def test_func(self):
        user = self.request.user
        invitation = self.get_object()
        if user == invitation.guest and invitation.attending:
            return True
        return False

    def get_form_kwargs(self, **kwargs):
        kwargs = super(InvitationFoodView, self).get_form_kwargs()
        invitations = Invitation.objects.filter(event=self.get_object().event).filter(food__isnull=False)
        menu = self.get_object().event.menu
        kwargs.update({'menu': menu})
        menu_foods = menu.foods.all()
        menu_proportions = Proportion.objects.filter(menu=menu)
        if menu_proportions:
            valid_tags = get_valid_tags(menu, menu_proportions)
            tags = list()
            for tag in valid_tags:
                tags.append(Tag.objects.get(id=tag))
            kwargs.update({'tags': tags})
            foods = Food.objects.filter(creator=self.request.user, tags__in=valid_tags).distinct()
            try:
                required_tags = get_required_tags(menu)
                for tag in required_tags:
                    foods = foods.filter(tags__in=[tag])
            except:
                pass
            kwargs.update({'foods': foods})
        else:
            used_foods = menu_foods.filter(id__in=invitations.values_list('food')).distinct()
            foods = menu_foods.exclude(id__in=[food.id for food in used_foods])
            kwargs.update({'foods': foods})
        return kwargs


# I'm not actually sure what's going on here.
def get_valid_tags(menu, menu_proportions):
    # Returns a set of tag ids that will be considered "valid" <- how did I do this?
    #   a valid tag is one which does not already have too many
    #   sign ups on that tag already.
    # How is it determined if a tag has too many people signed up for it? TBD

    # Potential ways to determine:
    # 1) if tag "A" has a value of "x",
    #       "A" can only get "x" items before it is no longer valid,
    #       or until all other tags fulfill their limit, then the cycle begins again
    min_ratio = math.inf
    for menu_proportion in menu_proportions.all():
        min_ratio = min(min_ratio, menu_proportion.ratio())

    id_list = list()
    for menu_proportion in menu_proportions.all():
        if menu_proportion.ratio() <= min_ratio:
            id_list.append(menu_proportion.id)

    unfilled_tags = menu_proportions.filter(id__in=id_list)
    menu_tags = unfilled_tags.values_list('tag').all()
    # Is there a better way to do this?
    tags = set()
    for tag_tuple in menu_tags:
        for tag in tag_tuple:
            tags.add(tag)
    return tags


def get_required_tags(menu):
    tags_qs = menu.theme.all()
    required_tags = set()
    for tag in tags_qs:
        required_tags.add(tag.id)
    return required_tags  # .values_list('theme', flat=True))
