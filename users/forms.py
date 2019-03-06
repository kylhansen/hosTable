from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, RestrictionTag

# Register a new user


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs['placeholder'] = 'Tell us about yourself!'
        self.fields['restrictions'] = forms.ModelMultipleChoiceField(
            RestrictionTag.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
            required=False)
        self.fields['restrictions'].help_text = 'Select your dietary restrictions from above. (Please contact an administrator if you do not see your restriction listed.)'

    class Meta:
        model = Profile
        fields = ['bio', 'restrictions']
