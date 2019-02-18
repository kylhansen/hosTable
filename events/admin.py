from django.contrib import admin
from .models import Event, Invitation, SignUp

admin.site.register(Event)
admin.site.register(Invitation)
admin.site.register(SignUp)
