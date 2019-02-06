# events/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import EventDetailView, EventCreateView

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('view/<int:pk>', EventDetailView.as_view(), name='event-view'),
]
