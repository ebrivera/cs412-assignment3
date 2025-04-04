# File: ./mini_fb/views.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 2/21/25
# Description:This is the django part that returns 
# all views for all the instances of Profile(s), status messages, friends, 
# images status images (ListView, and
# DetailView). This allows us to render objects with context

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.http import HttpResponseRedirect
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW



import random

# view for ALL the profiles
class ShowAllProfilesView(ListView):
    """Define a view class to show all fb profiles."""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)


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

        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user)
        form.instance.user = user
		# delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """provides context variables to the template."""
        context = super().get_context_data()

        context['user_form'] = UserCreationForm

        return context




class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """A view to create a message to a profile"""

    form_class=CreateStatusMessageForm
    template_name="mini_fb/create_status_form.html"

    def get_success_url(self):
        """Provide a url to redirect to after creating a successful message"""

        # retrive pk from profile
        profile = Profile.objects.get(user=self.request.user)
        # call reverse  to generate the URL for this profile
        return reverse('profile', kwargs={'pk':profile.pk})

    
    def form_valid(self, form):
        '''
        This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Message
        object before saving it to the database.
        '''

        # retrive pk from profile
        profile = Profile.objects.get(user=self.request.user)

        # attach profile to message
        form.instance.profile = profile

        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            # make image 
            img = Image(image_file=file, profile=profile, caption=f"status imaige for msg {profile}'s profile")
            img.save()
            # make status image
            status_image = StatusImage(status_message=sm, image=img)
            status_image.save()
        # delegate work to superclass method form_valid
        return super().form_valid(form)
    
    def get_context_data(self):
        """
            Return the dictionary of context variables for use in the template.
        """

        # calling the superclass method
        context = super().get_context_data()


        profile = Profile.objects.get(user=self.request.user)

        context['profile'] = profile
        return context
    

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        """return the profile for a user that is logged in"""
        return Profile.objects.get(user=self.request.user)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
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
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        """return the profile for a user that is logged in"""
        return Profile.objects.get(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to block from updating this profile.'''
        profile = Profile.objects.get(user=self.request.user)

        if profile.user != request.user:
            return HttpResponseRedirect(reverse('profile', kwargs={'pk':profile.pk}))
        
        return super().dispatch(request, *args, **kwargs)


class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view to update a StatusMessage and save it to the database.'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission to create a new update to sm object.
        '''
        print(f'UpdateStatusMessageForm: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)
    
    def get_context_data(self):
        """
            Return the dictionary of context variables for use in the template.
        """

        # calling the superclass method
        context = super().get_context_data()

        pk = self.kwargs['pk']

        status_message = StatusMessage.objects.get(pk=pk)
        context['status_message'] = status_message
        context['profile'] = status_message.profile
        return context
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this comment
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        profile = message.profile
        
        # reverse to show the article page
        return reverse('profile', kwargs={'pk':profile.pk})
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to block others from deleting 
        status message thats not theirs.'''
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        profile = Profile.objects.get(user=self.request.user)

        if message.profile.user != request.user:
            return HttpResponseRedirect(reverse('profile', kwargs={'pk':profile.pk}))
        
        return super().dispatch(request, *args, **kwargs)
        
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a status message and remove it from the database.'''

    template_name = "mini_fb/delete_status_form.html"
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
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to block others from deleting 
        status message thats not theirs.'''
        pk = self.kwargs.get('pk')
        message = StatusMessage.objects.get(pk=pk)
        profile = Profile.objects.get(user=self.request.user)

        if message.profile.user != request.user:
            return HttpResponseRedirect(reverse('profile', kwargs={'pk': profile.pk}))
        
        return super().dispatch(request, *args, **kwargs)


class AddFriendView(View):
    """A view to create a Friend relationship between to profiles"""

    def dispatch(self, request, *args, **kwargs):
        other_pk = kwargs['other_pk']

        profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=other_pk)
        profile.add_friend(other_profile)
        return HttpResponseRedirect(reverse('profile', kwargs={'pk':profile.pk}))
    
    def get_object(self):
        """return the profile for a user that is logged in"""
        return Profile.objects.get(user=self.request.user)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """A view to show the suggested friends of a specific profile"""
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    def get_object(self):
        """return the profile for a user that is logged in"""
        return Profile.objects.get(user=self.request.user)
        ## bc of this objects.get we never need dispatch
    
    

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """A view to show the status messages in your newsfeed from your profile and your friends"""
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        """return the profile for a user that is logged in"""
        return Profile.objects.get(user=self.request.user)
        ## bc of this objects.get we never need dispatch

class UserRegistrationView(CreateView):
    """Process and show the creation of a user"""

    template_name = "mini_fb/register.html"
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')

class LogoutConfirmationView(TemplateView):
    """Simple view to display logout confirmation"""
    template_name = "mini_fb/logged_out.html"
