# menus/forms.py

from .models import Menu, Food
from django import forms
from django.contrib.auth.models import User


class MenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MenuCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Menu Name'
        # Fix so that the user can select a food item from a list of foods which they have created
        self.fields['foods'] = forms.ModelMultipleChoiceField(
            Food.objects.filter(creator=user),
            widget=forms.CheckboxSelectMultiple(),
            required=False)

    class Meta:
        model = Menu
        fields = [
            'name',
            'foods',
        ]


class FoodCreateForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = [
            'name',
            'recipe_link',
            'food_tags',
        ]
