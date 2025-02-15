
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    # path(r'', views.show_form, name="show_form"),
    path(r'', views.main_page, name="main_page"),
    path(r'main', views.main_page, name="main_page"),
    path(r'order', views.order_page, name="order_page"),
    # path(r'confirmation', views.confirmation_page, name="confirmation_page"),
    path(r'confirmation', views.submit, name="submit"), ## new
]
