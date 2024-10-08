from django.contrib import admin
from .models import Profile, Contact, AppAccessTime, ContactView

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(AppAccessTime)
admin.site.register(ContactView)
