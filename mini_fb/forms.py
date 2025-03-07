from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """A form to add a profile in the db"""

    class Meta:
        """associate this form with a model from our db"""
        model = Profile
        fields = [
            'first_name', 
            'last_name', 
            'city',
            'email', 
            'profile_image',
        ]
class UpdateProfileForm(forms.ModelForm):
    '''A form to update a quote to the database.'''

    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['city', 'email', 'email', 'profile_image']  # which fields from model should we use

    
class CreateStatusMessageForm(forms.ModelForm):
    """A form to send a message to a profile"""

    class Meta:
        """associate this form with a model from our database."""
        model = StatusMessage
        fields = [
            'message',

        ]


