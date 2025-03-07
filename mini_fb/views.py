# File: ./mini_fb/views.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 2/21/25
# Description:This is the django part that returns 
# all views for all the instances of Profile(s) (ListView, and
# DetailView). This allows us to render objects with context

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.urls import reverse


import random

# view for ALL the profiles
class ShowAllProfilesView(ListView):
    """Define a view class to show all fb profiles."""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

# view for singular profile
class ShowProfilePageView(DetailView):
    """Display a single profile"""

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

# define a subclass of CreateView to handle creation of Profile objecets
class CreateProfileView(CreateView):
    """
    A view to handle creation of new Profile
    1: Display the html form to user (GET)
    2: process the form submission and store new Profile object (POST)
    """

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'CreateProfileView: form.cleaned_data={form.cleaned_data}')

		# delegate work to the superclass version of this method
        return super().form_valid(form)



class CreateStatusMessageView(CreateView):
    """A view to create a message to a profile"""

    form_class=CreateStatusMessageForm
    template_name="mini_fb/create_status_form.html"

    def get_success_url(self):
        """Provide a url to redirect to after creating a successful message"""

        # create and return url
        # return reverse('show_all_profiles')
        # retrive pk from url
        pk = self.kwargs['pk']
        # call reverse  to generate the URL for this profile
        return reverse('profile', kwargs={'pk':pk})

    
    def form_valid(self, form):
        '''
        This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Message
        object before saving it to the database.
        '''

        # retrive pk from url
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # attach profile to message
        form.instance.profile = profile

        # delegate work to superclass method form_valid
        return super().form_valid(form)
    
    def get_context_data(self):
        """
            Return the dictionary of context variables for use in the template.
        """

        # calling the superclass method
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context

class UpdateProfileView(UpdateView):
    '''A view to update a Profile and save it to the database.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)
    
class DeleteStatusMessageView(DeleteView):
    '''A view to delete a status message and remove it from the database.'''

    template_name = "mini_fb/delete_status_message_form.html"
    model = StatusMessage
    context_object_name = 'message'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this comment
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        profile = message.profile
        
        # reverse to show the article page
        return reverse('profile', kwargs={'pk':profile.pk})




## this is from class, which i assume will be implemented to some extent later which is
## why i am keeping it for now
# class RandomProfileView(DetailView):
#     """Display a single profile view at random"""

#     model = Profile
#     template_name = "mini_fb/profile.html"
#     context_object_name = "profile" #singular

#     # method
#     def get_object(self):
#         """return one instance of the Profile object at random"""

#         all_profiles = Profile.objects.all()
#         profile = random.choice(all_profiles)
#         return profile