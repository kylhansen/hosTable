# menus/forms.py

from .models import Menu, Food, Proportion
from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory


class MenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MenuCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Menu Name'
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


class ProportionalMenuCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProportionalMenuCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Menu Name'
        self.fields['theme'].label = 'Theme'
        self.fields['theme'].help_text = 'a comma-sepparated list of tags which <b>every</b> food item must contain.'

    class Meta:
        model = Menu
        fields = [
            'name',
            'theme'
        ]


class FoodCreateForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = [
            'name',
            'recipe_link',
            'tags',
        ]


class ProportionCreateForm(forms.ModelForm):
    proportion = forms.IntegerField()

    class Meta:
        fields = [
            'tag',
            'proportion',
        ]


ProportionMenuFormSet = inlineformset_factory(Menu, Proportion,
                                              form=ProportionCreateForm, extra=4)
