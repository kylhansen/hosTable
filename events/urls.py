# events/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    EventDetailView,
    EventCreateView,
    EventGuestListView,
    EventHostListView,
    EventUpdateView,
    InvitationResponseView,
    InvitationFoodView,
)


urlpatterns = [
    path('create/',
         EventCreateView.as_view(template_name='events/create.html'),
         name='event-create'),
    path('update/<int:pk>',
         EventUpdateView.as_view(template_name='events/update.html'),
         name='event-update'),
    path('view/<int:pk>',
         EventDetailView.as_view(template_name='events/view.html'),
         name='event-view'),
    path('view/list/guest/<str:RSVP_status>/<int:user_id>',
         EventGuestListView.as_view(template_name='events/list.html'),
         name='event-list-guest'),
    path('view/list/host/<int:user_id>',
         EventHostListView.as_view(template_name='events/list.html'),
         name='event-list-host'),
    path('RSVP/<int:pk>',
         InvitationResponseView.as_view(template_name='events/invitations/response.html'),
         name='event-response'),
    path('RSVP/<int:pk>/food',
         InvitationFoodView.as_view(template_name='events/invitations/food.html'),
         name='event-response-food'),
]
