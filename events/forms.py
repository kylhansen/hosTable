from .models import Event, Invitation
from menus.models import Menu, Proportion, Food
from menus.forms import MenuCreateForm
from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from datetime import date
from taggit.models import Tag
from crispy_forms.helper import FormHelper


class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s %s (%s)" % (obj.first_name, obj.last_name, obj.username)


class EventCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(EventCreateForm, self).__init__(*args, **kwargs)
        self.fields['guests'] = MyModelMultipleChoiceField(
            User.objects.exclude(id=request.user.id),
            widget=forms.CheckboxSelectMultiple(),
            required=False)
        menus = Menu.objects.filter(creator=request.user)
        self.fields['menu'] = forms.ModelChoiceField(queryset=menus)
        self.fields['event_date'] = forms.DateField(
            widget=forms.SelectDateWidget,
            initial=date.today())
        self.fields['event_time'] = forms.TimeField(input_formats=('%I:%M %p',))
        self.fields['event_time'].help_text = "Please use the format <em>HH:MM (AM/PM)</em>."
        self.fields['RSVP_date'] = forms.DateField(
            widget=forms.SelectDateWidget,
            initial=date.today())

    def clean(self):
        cleaned_data = super().clean()
        RSVP_date = cleaned_data.get('RSVP_date')
        event_date = cleaned_data.get('event_date')
        try:
            if not RSVP_date < event_date:
                self.add_error(None, ValidationError('RSVP date must be prior to event date.'))
        except:
            pass
        return cleaned_data

    def save(self, commit=True):
        instance = super(EventCreateForm, self).save(commit=True)
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


class EventUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        # uninvited_users = kwargs.pop('uninvited_users')
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        self.fields['guests'] = forms.ModelMultipleChoiceField(
            User.objects.exclude(id=request.user.id),
            widget=forms.CheckboxSelectMultiple(),
            required=False)

    '''    def save(self, commit=True):
        instance = super(EventUpdateForm, self).save(commit=True)
        # instance.guests.add(instance.host)
        if commit:
            instance.save()
        return instance'''

    class Meta:
        model = Event
        fields = ['guests',
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
        self.menu = kwargs.pop('menu')
        try:
            self.tags = kwargs.pop('tags')
        except:
            pass
        super(InvitationFoodForm, self).__init__(*args, **kwargs)
        self.fields['food'] = forms.ModelChoiceField(queryset=foods)

    def clean(self):
        cleaned_data = super().clean()
        food = cleaned_data.get('food')
        tags = self.tags
        used_tags = set()
        food_tags = food.tags.values_list('name', flat=True)
        for tag in food_tags:
            tag = Tag.objects.get(name=tag)
            if tag in tags:
                used_tags.add(tag)
        menu = self.menu
        proportions = Proportion.objects.filter(menu=menu).all()
        portion_used = 1.0 / len(used_tags)
        for tag in used_tags:
            item = proportions.filter(tag=tag)
            proportion = item.first().proportion
            new_value = max(proportion - portion_used, 0)
            item.update(proportion=new_value)
        return cleaned_data

    class Meta:
        model = Invitation
        fields = [
            'food'
        ]
