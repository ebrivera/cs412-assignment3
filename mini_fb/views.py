# mini_fb/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
import random

# Create your views here.
class ShowAllProfilesView(ListView):
    """Define a view class to show all fb profiles."""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    """Display a single profile"""

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile" #singular

class RandomProfileView(DetailView):
    """Display a single profile view at random"""

    model = Profile
    template_name = "mini_fb/profile.html"
    context_object_name = "profile" #singular

    # method
    def get_object(self):
        """return one instance of the Profile object at random"""

        all_profiles = Profile.objects.all()
        profile = random.choice(all_profiles)
        return profile