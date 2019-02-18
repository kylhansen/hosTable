# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserCreateView, UserUpdateView, UserDetailView, activate
from django.conf.urls import url

urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(template_name='users/view.html'), name='user-view'),
    path('<int:pk>/update', UserUpdateView.as_view(template_name='users/update.html'), name='user-update'),
    path('register/', UserCreateView.as_view(template_name='users/register.html'), name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='user-logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
