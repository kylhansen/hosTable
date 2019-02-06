# users/models.py

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first = models.CharField(default="", max_length=100)
    last = models.CharField(default="", max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'pk': self.pk})
