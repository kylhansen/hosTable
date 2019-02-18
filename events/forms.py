from .models import Event, Invitation
from django import forms
from django.contrib.auth.models import User


class EventCreateForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    request = kwargs.pop('request')
    super(EventCreateForm, self).__init__(*args, **kwargs)
    self.fields['guests'] = forms.ModelMultipleChoiceField(User.objects.exclude(id=request.user.id),
                                                           widget=forms.CheckboxSelectMultiple(),
                                                           required=False)

  def save(self, commit=True):
    instance = super(EventCreateForm, self).save(commit=True)
    instance.guests.add(instance.host)
    if commit:
      instance.save()
    return instance

  class Meta:
    model = Event
    fields = ['title',
              'event_location',
              'menu',
              'guests',
              'event_date',
              'event_time',
              'RSVP_date',
              ]


class InvitationResponseForm(forms.ModelForm):

  attending = forms.TypedChoiceField(
      choices=((False, 'Regretfully Decline'),
               (True, 'Will Attend')),
      widget=forms.RadioSelect
  )

  def save(self, commit=True):
    instance = super(InvitationResponseForm, self).save(commit=True)
    instance.replied = True
    if commit:
      instance.save()
    return instance

  class Meta:
    model = Invitation
    fields = [
        'attending'
    ]
