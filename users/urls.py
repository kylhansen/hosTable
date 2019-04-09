# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserCreateView, UserUpdateView, ProfileUpdateView, ProfileDetailView, activate
from django.conf.urls import url

urlpatterns = [
    path('<int:pk>/',
         ProfileDetailView.as_view(template_name='users/view.html'),
         name='user-view'),
    path('<int:pk>/update',
         UserUpdateView.as_view(template_name='users/update.html'),
         name='user-update'),
    path('<int:pk>/profile/update',
         ProfileUpdateView.as_view(template_name='users/update.html'),
         name='user-profile-update'),
    path('register/',
         UserCreateView.as_view(template_name='users/register.html'),
         name='user-register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='user-login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='user-logout'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password-reset'),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]
