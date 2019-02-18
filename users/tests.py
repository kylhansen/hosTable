# users/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .signals import create_profile, save_profile
from django.urls import reverse

'''
class TestSignals(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com')

    def test_create_profile_signal(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.first, '')
        self.assertEqual(profile.last, '')


class TestProfile(TestCase):

    def setUp(self):
        user = User.objects.create_user('kylhansen', 'kylhansen@westmont.edu')
        self.profile = Profile.objects.get(user=user)

    def test_string_representation(self):
        self.assertEqual(str(self.profile), self.profile.user.username)



class HomeViewTest(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ProfileDetailViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('kylhansen', 'kylhansen@westmont.edu', 'testing321')
        self.profile = Profile.objects.get(user=user)
        self.profile.first = 'Kyle'
        self.profile.last = 'Hansen'

    def test_redirect_if_not_logged_in(self):
        # TODO: Fix this so that the line below this gets the reverse url for the current 'profile' as above.
        response = self.client.get(reverse('user-profile', args=[self.profile.user.pk]))
        print(reverse('user-login') + '?next=' + self.profile.get_absolute_url())
        print(response)
        self.assertRedirects(response, reverse('user-login') + '?next=' + self.profile.get_absolute_url())

    def test_success_if_logged_in(self):
        login = self.client.login(username='kylhansen', password='testing321')
        response = self.client.get(reverse('user-profile', args=[self.profile.user.pk]))

        # Check our user is logged in
        self.assertEqual(response.context['user'], self.profile.user)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
'''
