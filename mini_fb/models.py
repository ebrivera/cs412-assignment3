# File: ./mini_fb/models.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 2/21/25
# Description: this File creates a profile class for the table
# each instance of a profile has a first name, last name, city,
# email, and profile image url, which are all optional

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a Profile with personal information.'''

    # define the data attributes of the Profile object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    # profile_image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True) # an actual image

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.first_name}'
    

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('profile', kwargs={'pk':self.pk})
    
    def get_status_messages(self):
        """Return a queryset of messages to this profile"""
        messages = StatusMessage.objects.filter(profile=self)
        return messages


class StatusMessage(models.Model):
    """Encapsulate the idea of a status message w/ timestamp, message content and profile relationship."""

    # define the data attributes of the StatusMessage object
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of the status message"""
        return f'{self.message}'