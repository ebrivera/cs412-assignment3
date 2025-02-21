# File: ./mini_fb/urls.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 2/21/25
# Description: This allows all the pages to be hyper linked, and shows
# the path so people can enter it in via url, or so it can be accessed 
# from other files

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView # our view class definition 

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
    path('show_all_profiles', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='profile'),
]