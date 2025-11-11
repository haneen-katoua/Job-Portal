from django.contrib import admin
from .models import Job , SavedJob , Notification

# Register your models here.

admin.site.register(Job)
admin.site.register(SavedJob)
admin.site.register(Notification)
