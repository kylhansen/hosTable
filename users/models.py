# users/models.py

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user-view', kwargs={'pk': self.pk})
