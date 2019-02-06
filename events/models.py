# users/models.py

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Event(models.Model):
    title = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return reverse('event-view', kwargs={'pk': self.pk})


'''
class Invitation(Event):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.title + self.guest.username)

    def get_absolute_url(self):
        return reverse('event-invitation', kwargs={'pk': self.pk})
'''
