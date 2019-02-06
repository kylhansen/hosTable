# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserCreateView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='user-logout'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='user-profile'),
    path('<int:pk>/update', ProfileUpdateView.as_view(), name='user-update'),
]
