# menus/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from taggit.managers import TaggableManager


class Food(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_link = models.URLField(max_length=200, blank=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return self.name


class Proportion(models.Model):
    tag = TaggableManager()
    proportion = models.IntegerField()
