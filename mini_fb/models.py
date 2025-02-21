# mini_fb/models.py
from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a Profile with personal information.'''

    # define the data attributes of the Profile object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.first_name}'