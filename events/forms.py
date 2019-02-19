from .models import Event, Invitation
from menus.models import Menu
from django import forms
from django.contrib.auth.models import User


class EventCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(EventCreateForm, self).__init__(*args, **kwargs)
        self.fields['guests'] = forms.ModelMultipleChoiceField(User.objects.exclude(id=request.user.id),
                                                               widget=forms.CheckboxSelectMultiple(),
                                                               required=False)
        menus = Menu.objects.filter(creator=request.user)
        self.fields['menu'] = forms.ModelChoiceField(queryset=menus)

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

    attending = forms.BooleanField(required=False)

    def save(self, commit=True):
        instance = super(InvitationResponseForm, self).save(commit=False)
        instance.replied = True
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Invitation
        widgets = {
            'attending': forms.RadioSelect
        }
        fields = [
            'attending'
        ]


class InvitationFoodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        foods = kwargs.pop('foods')
        super(InvitationFoodForm, self).__init__(*args, **kwargs)
        self.fields['food'] = forms.ModelChoiceField(queryset=foods)

    class Meta:
        model = Invitation
        fields = [
            'food'
        ]
