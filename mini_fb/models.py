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
    profile_image = models.ImageField(blank=True) # an actual image

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
    
    def get_friends(self):
        """return a queryset that will return a list of friend's profiles"""
        friend1 = Friend.objects.filter(profile1=self)
        friend2 = Friend.objects.filter(profile2=self)

        friends = []

        # self cld be friend 1, so we need to return the profile2
        for friend in friend1:
            friends.append(friend.profile2)

        # self cld be friend 2, so we need to return the profile1
        for friend in friend2:
            friends.append(friend.profile1)
        
        return friends

    def add_friend(self, other):
        """Add a friend relationship between two nodes (Creating a friendship between this Profile and another)"""

        # this is seeing if p1 has friend p2
        potential1 = Friend.objects.filter(profile1=self, profile2=other)
        # this is seeing if p2 has friend p1
        potential2 = Friend.objects.filter(profile1=other, profile2=self)

        # exists() returns true or false, and then we need to check if p1==p1
        if potential1.exists() or potential2.exists() or self==other:
            return
        else: # else actually add them
            Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        # get friends
        current_friends = self.get_friends()

        #getting all the pks for the friends
        current_friend_ids = [f.pk for f in current_friends]
        
        # this is to exclude the current pk you'll see in the next ine
        current_friend_ids.append(self.pk)
        return Profile.objects.exclude(pk__in=current_friend_ids)
        
        



class StatusMessage(models.Model):
    """Encapsulate the idea of a status message w/ timestamp, message content and profile relationship."""

    # define the data attributes of the StatusMessage object
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of the status message"""
        return f'{self.message}'
    
    def get_images(self):
        """return a queryset of images associated with this status message"""

        # all status images for this message
        status_images = StatusImage.objects.filter(status_message=self)

        images = []

        for status_image in status_images:
            images.append(status_image.image)

        
        return images
    
class Image(models.Model):
    image_file = models.ImageField(blank=False) # an actual image
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of the status message"""
        return f'{self.profile} posted this image at {self.timestamp}'

class StatusImage(models.Model):
    """Encapsulate the idea of a message being an Image, two FK"""

    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image = models.ForeignKey("Image", on_delete=models.CASCADE)

    def __str__(self):
        """return a string representation of the status message"""
        return f"This image was attached to {self.status_message.profile}'s page"


class Friend(models.Model):
    """Encapsulate the idea of an edge connecting two nodes within the social network"""
    
    profile1 = models.ForeignKey("Profile", related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey("Profile", related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.profile1} & {self.profile2}'