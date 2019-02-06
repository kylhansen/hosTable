from .models import Event
from django import forms
from django.forms.widgets import DateInput
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class EventCreateForm(forms.ModelForm):

  class Meta:
    model = Event
    fields = ['title',
              'event_location',
              'event_date',
              'event_time',
              'RSVP_date',
              ]
    # event_date = forms.DateField(
    #    widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"))
    #)
    # event_time = forms.TimeField(
    #    forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    #)
    # RSVP_date = forms.DateField(
    #    widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"))
    #)
