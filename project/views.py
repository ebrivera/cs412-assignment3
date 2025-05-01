# File: ./project/views.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/24/25
# Description:This is the django part that returns 
# all views for all the instances of Profile(s), status messages, friends, 
# images status images (ListView, and
# DetailView). This allows us to render objects with context

from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from .models import CoffeeBag, CoffeeEnthusiast, Review, CoffeeBagTag, Tag
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.views.generic.edit import CreateView
from .forms import CreateCoffeeBagForm, CreateReviewForm, CreateEnthusiastForm, UpdateCoffeeEnthusiastForm




import random

# view for ALL the coffees
class ShowAllCoffees(ListView):
    """Define a view class to see all the recently rated coffee bags."""
    model = CoffeeBag
    template_name = "project/show_all_coffees.html"
    context_object_name = "coffee_bags"


    def get_context_data(self, **kwargs):
        """
            Return the dictionary of context variables for use in the template.
        """
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        # get all the coffee bags
        coffee_bags = CoffeeBag.objects.all()
        # add the coffee bags to the context
        context['all_tags'] = Tag.objects.all()
        context['all_roasts'] = CoffeeBag.objects.values_list('roast', flat=True).distinct()
        context['all_origins'] = CoffeeBag.objects.values_list('origin', flat=True).distinct()
        return context
    
    def get_queryset(self):
        """
            queryset to get coffee bags by roast and origin
        """
        # get all the coffee bags
        coffee_bags = CoffeeBag.objects.all()

        if 'roast' in self.request.GET:
            ## roast type
            roast = self.request.GET['roast']
            if roast and roast != '0' and roast != '':
                # filter the coffee bags by roast
                coffee_bags = coffee_bags.filter(roast=roast)

        if 'origin' in self.request.GET:
            ## origin type
            origin = self.request.GET['origin']
            if origin and origin != '0' and origin != '':
                # filter the coffee bags by origin
                coffee_bags = coffee_bags.filter(origin=origin)
        if 'tag' in self.request.GET:
            ## tag type
            tag = self.request.GET['tag']
            if tag and tag != '0' and tag != '':
                coffee_bags = coffee_bags.filter(tags__id=int(tag))

        return coffee_bags

class ShowCoffeBagView(DetailView):
    """Display a single coffee bag"""

    model = CoffeeBag
    template_name = "project/show_coffee_bag.html"
    context_object_name = "coffee_bag"

class CreateCoffeeBagView(LoginRequiredMixin, CreateView):
    """
    A view to handle creation of new CoffeeBag
    1: Display the html form to user (GET)
    2: process the form submission and store new Coffee Bag object (POST)
    """
    form_class = CreateCoffeeBagForm
    template_name = "project/create_coffee_bag_form.html"

    def get_success_url(self):
        """Redirect to the coffee bag detail page"""
        return reverse('coffee_bag', kwargs={'pk': self.object.pk})
    
    def get_login_url(self) -> str:
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''check if user is authenticated'''
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class CreateReviewView(LoginRequiredMixin, CreateView):
    """
    A view to handle creation of new Review
    1: Display the html form to user (GET)
    2: process the form submission and store new Review object (POST)
    """
    form_class = CreateReviewForm
    template_name = "project/create_review_form.html"


    def form_valid(self, form):
        """Process the form submission and store new Review object"""
        # get the coffee bag instance from the URL
        coffee_bag_pk = self.kwargs['pk']
        print(f'CreateReviewView: coffee_bag={coffee_bag_pk}')
        coffee_bag = CoffeeBag.objects.get(pk=coffee_bag_pk)
        form.instance.coffee_bag = coffee_bag
        form.instance.user = self.request.user
        self.object = form.save()


        if 'tags' in form.cleaned_data:
            if form.cleaned_data['tags']:
                for tag in form.cleaned_data['tags']:
                    existing = CoffeeBagTag.objects.filter(coffee_bag=coffee_bag, tag=tag).exists()
                    if not existing:
                        CoffeeBagTag.objects.create(coffee_bag=coffee_bag, tag=tag)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Redirect to the coffee bag detail page"""
        return reverse('coffee_bag', kwargs={'pk': self.kwargs['pk']})
    def get_login_url(self) -> str:
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''check if user is authenticated'''
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        """
            Return the dictionary of context variables for use in the template.
        """

        # calling the superclass method
        context = super().get_context_data(**kwargs)


        coffee_bag = CoffeeBag.objects.get(pk=self.kwargs['pk'])

        context['coffee_bag'] = coffee_bag

        context['tags'] = coffee_bag.tags.all()

        return context
    
class ShowCoffeeEnthusiast(DetailView):
    """Display a single coffee enthusiast"""

    model = CoffeeEnthusiast
    template_name = "project/show_coffee_enthusiast.html"
    context_object_name = "coffee_enthusiast"

    def get_context_data(self, **kwargs):
        """
            Return the dictionary of context variables for use in the template.
        """
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        # get the coffee enthusiast instance
        coffee_enthusiast = self.get_object()
        # get all the reviews for this coffee enthusiast
        reviews = Review.objects.filter(user=coffee_enthusiast.user)
        # add the reviews to the context
        context['reviews'] = reviews

        context['favorites'] = coffee_enthusiast.favorite_coffee_bags.all()

        return context


class CreateCoffeeEnthusiastView(CreateView):
    """
    A view to handle creation of new CoffeeEnthusiast
    1: Display the html form to user (GET)
    2: process the form submission and store new CoffeeEnthusiast object (POST)
    """
    form_class = CreateEnthusiastForm
    template_name = "project/create_coffee_enthusiast_form.html"

    def get_success_url(self):
        """Redirect to enthusiasts profile"""
        return reverse('coffee_enthusiast', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new CoffeeEnthusiast object.
        '''
        if self.request.user.is_authenticated:
            # if user is already authenticated
            form.instance.user = self.request.user
        else:
            # if user is not authenticated, create a new user
            user_form = UserCreationForm(self.request.POST)
            if user_form.is_valid():
                user = user_form.save()
                login(self.request, user)
                form.instance.user = user
            else:
                # handle the case where the form is not valid
                return self.form_invalid(form)
		# delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
            provides context variables to the template.
        """
        context = super().get_context_data()

        if not self.request.user.is_authenticated:
            context['user_form'] = UserCreationForm
            context['show_user_form']  = True
        else:
            context['show_user_form']  = False
        return context


class ShowAllCoffeeEnthusiasts(ListView):
    """Define a view class to see all the coffee enthusiasts."""
    model = CoffeeEnthusiast
    template_name = "project/show_all_coffee_enthusiasts.html"
    context_object_name = "coffee_enthusiasts"

    def get_context_data(self, **kwargs):
        """
            Return the dictionary of context variables for use in the template.
        """
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        # get all the coffee enthusiasts
        coffee_enthusiasts = CoffeeEnthusiast.objects.all()
        # add the coffee enthusiasts to the context
        context['coffee_enthusiasts'] = coffee_enthusiasts

        # get ppl with same favorites
        if self.request.user.is_authenticated:
            coffee_enthusiast = CoffeeEnthusiast.objects.get(user=self.request.user)
            # get all the coffee enthusiasts with the same favorite coffee bags
            similar_enthusiasts = CoffeeEnthusiast.objects.filter(favorite_coffee_bags__in=coffee_enthusiast.favorite_coffee_bags.all()).exclude(user=self.request.user).distinct()
            # add the similar enthusiasts to the context
            context['similar_enthusiasts'] = similar_enthusiasts

        return context
    
    def get_queryset(self):
        """
            queryset to get coffee enhusiasts by favorite
        """
        # get all the coffee enthusiasts
        coffee_enthusiasts = CoffeeEnthusiast.objects.all()

        if 'favorite_coffee' in self.request.GET:
            ## coffee bag id
            coffee_bag_id = self.request.GET['favorite_coffee']
            if coffee_bag_id and coffee_bag_id != '0' and coffee_bag_id != '':
                # filter the coffee enthusiasts by favorite coffee bag
                coffee_enthusiasts = coffee_enthusiasts.filter(favorite_coffee_bags__id=coffee_bag_id)
        return coffee_enthusiasts
    
class LogoutConfirmationView(TemplateView):
    """Simple view to display logout confirmation"""
    template_name = "project/logged_out.html"


class UpdateCoffeeEnthusiastView(LoginRequiredMixin, UpdateView):
    '''A view to update a Profile and save it to the database.'''
    model = CoffeeEnthusiast
    form_class = UpdateCoffeeEnthusiastForm
    template_name = "project/update_coffee_enthusiast_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to update a CoffeeEnthusiast object.
        '''
        print(f'UpdateCoffeeEnthusiastView: form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
            Return the dictionary of context variables for use in the template.
        """
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        # get the coffee enthusiast instance
        coffee_enthusiast = self.get_object()
        # add the coffee enthusiast to the context
        context['coffee_enthusiast'] = coffee_enthusiast

        return context

    def get_success_url(self):
        '''Redirect to the coffee enthusiast profile page'''
        return reverse('coffee_enthusiast', kwargs={'pk': self.object.pk})
    
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        """return the profile for a user that is logged in"""
        return CoffeeEnthusiast.objects.get(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to block from updating this profile.'''
        profile = CoffeeEnthusiast.objects.get(user=self.request.user)

        if profile.user != request.user:
            return HttpResponseRedirect(reverse('coffee-enthusiast', kwargs={'pk':profile.pk}))
        
        return super().dispatch(request, *args, **kwargs)