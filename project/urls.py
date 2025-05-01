# File: ./project/urls.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/24/25
# Description: This allows all the pages to be hyper linked, and shows
# the path so people can enter it in via url, or so it can be accessed 
# from other files

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', ShowAllCoffees.as_view(), name='show_all_coffees'), # generic class-based view
    path('coffee-bag/<int:pk>', ShowCoffeBagView.as_view(), name='coffee_bag'),
    path('coffee-bag/create', CreateCoffeeBagView.as_view(), name='create_coffee_bag'),
    path('coffee-bag/<int:pk>/create-review', CreateReviewView.as_view(), name='create_review'),
    path('coffee-enthusiast/<int:pk>', ShowCoffeeEnthusiast.as_view(), name='coffee_enthusiast'),
    path('coffee-enthusiast/create', CreateCoffeeEnthusiastView.as_view(), name='create_coffee_enthusiast'),
    path('coffee-enthusiast/<int:pk>/update', UpdateCoffeeEnthusiastView.as_view(), name='update_coffee_enthusiast'),
    
    path('coffee-enthusiast/all', ShowAllCoffeeEnthusiasts.as_view(), name='show_all_coffee_enthusiasts'),

    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="logout_confirmation"), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    # path('register/', UserRegistrationView.as_view(), name='register'),

]