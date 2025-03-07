# File: ./mini_fb/admin.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 2/21/25
# Description: Allows us to create an admin instance where
# we can see all of the different profile instances

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)