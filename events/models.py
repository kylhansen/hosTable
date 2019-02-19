# events/models.py

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from menus.models import Menu, Food


class Event(models.Model):
    title = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu')
    guests = models.ManyToManyField(User)
    event_location = models.CharField(max_length=100, blank=True, null=True, default="TBD")
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    RSVP_date = models.DateField()

    def __str__(self):
        return self.title

    def clean(self):
        if self.RSVP_date > self.event_date:
            raise ValidationError({'RSVP_date': 'RSVP deadline must not be after the event.'})

    def get_absolute_url(self):
        return reverse('event-view', kwargs={'pk': self.id})


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    replied = models.BooleanField(default=False, blank=True, null=True)
    attending = models.BooleanField(default=False, blank=True, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('event', 'guest')

    def clean(self):
        if self.food:
            if not self.attending:
                raise ValidationError({'attending': 'A guest must attend in order to sign up for a food item.'})
            if not self.food in self.event.menu.foods.all():
                raise ValidationError({'food': 'The specified food item does not exist in the menu for this event.'})

    def __str__(self):
        return ('Event: ' + self.event.title + ' -- Guest: ' + self.guest.username)

    def get_absolute_url(self):
        return reverse('event-list-guest',
                       kwargs={'RSVP_status': 'attending',
                               'guest_id': self.guest.id})
