# create file: quotes/urls.py

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.home_page, name="home_page"),
    path(r'quote', views.home_page, name="home_page"),
    path(r'about', views.about, name="about_page"),
    path(r'show_all', views.show_all, name="show_all_page")
]