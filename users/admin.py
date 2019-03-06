from django.contrib import admin
from .models import Profile, RestrictionTag, TaggedRestriction

admin.site.register(Profile)
admin.site.register(RestrictionTag)
admin.site.register(TaggedRestriction)
