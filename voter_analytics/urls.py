# File: ./voter_analytics/urls.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/4/25
# Description: This allows all the pages to be hyper linked, and shows
# the path so people can enter it in via url, or so it can be accessed 
# from other files
from django.urls import path
from . import views 

urlpatterns = [
    # map the URL (empty string) to the view
	path('', views.VotersListView.as_view(), name='voters'),
    path('results', views.VotersListView.as_view(), name='voter_list'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
    path('graphs', views.GraphListView.as_view(), name='graphs'),
    

]
