# File: ./mini_fb/views.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 2/21/25
# Description:This is the django part that returns 
# all views for all the instances of Profile(s) (ListView, and
# DetailView). This allows us to render objects with context

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
import random

# view for ALL the profiles
class ShowAllProfilesView(ListView):
    """Define a view class to show all fb profiles."""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

# view for singular profile
class ShowProfilePageView(DetailView):
    """Display a single profile"""

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

## this is from class, which i assume will be implemented to some extent later which is
## why i am keeping it for now
# class RandomProfileView(DetailView):
#     """Display a single profile view at random"""

#     model = Profile
#     template_name = "mini_fb/profile.html"
#     context_object_name = "profile" #singular

#     # method
#     def get_object(self):
#         """return one instance of the Profile object at random"""

#         all_profiles = Profile.objects.all()
#         profile = random.choice(all_profiles)
#         return profile