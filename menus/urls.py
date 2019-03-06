# events/urls.py

from django.urls import path
from .views import MenuCreateView, MenuUpdateView, FoodCreateView, ProporitionMenuCreateView

urlpatterns = [
    path('create/',
         MenuCreateView.as_view(template_name='menus/create.html'),
         name='menu-create'),
    path('<int:pk>/',
         MenuUpdateView.as_view(template_name='menus/update.html'),
         name='menu-update'),
    path('create/food',
         FoodCreateView.as_view(template_name='menus/add_food.html'),
         name='menu-food-create'),
    path('create/proportional',
         ProporitionMenuCreateView.as_view(template_name='menus/create_proportional.html'),
         name='menu-proportion-create')
]
