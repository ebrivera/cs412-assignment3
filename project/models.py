# File: ./project/models.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/18/25
# Description: this File creates a the classes necessary
# in order for coffee bags to be reviewed by people with specific tags

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 

# Create your models here.


class CoffeeBag(models.Model):
    """Encapsulate the idea of a CoffeeBag with unique information information."""
    company = models.TextField(blank=True)
    roast = models.TextField(blank=True)
    origin = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    tags = models.ManyToManyField('Tag', through='CoffeeBagTag', blank=True)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.company} {self.roast} {self.origin}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('profile', kwargs={'pk':self.pk})
    
    def get_review(self):
        """return a queryset of reviews of this coffee bag"""
        reviews = Review.objects.filter(coffee_bag=self)
        return reviews
    
    def get_average_rating(self):
        """return the average rating of this coffee bag"""
        reviews = self.get_review()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return round(total_rating / reviews.count(), 2)
        return 0


class Review(models.Model):
    """Encapsulate the idea of a Review with unique information."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffee_bag = models.ForeignKey(CoffeeBag, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    review_text = models.TextField(blank=True)
    brew_method = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.user.first_name} {self.coffee_bag.company} {self.rating}'

class Tag(models.Model):
    """tag object."""
    name = models.TextField(blank=True)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.name}'

class CoffeeBagTag(models.Model):
    """coffee bag tag relationships."""
    coffee_bag = models.ForeignKey(CoffeeBag, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.coffee_bag} {self.tag}'

class CoffeeEnthusiast(models.Model):
    """encpasulate the idea of a profile w/ unique info"""
    profile_image = models.ImageField(blank=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coffee_profile')
    favorite_coffee_bags = models.ManyToManyField(CoffeeBag, blank=True)

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.user.username}'


def has_coffee_profile(self):
    """Check if user has a coffee profile safely."""
    try:
        # debugging statements + using hasattr to check if coffee_profile exists
        print(f"Checking has_coffee_profile for user {self.username}")
        has_profile = hasattr(self, 'coffee_profile')
        print(f"hasattr result: {has_profile}")
        
        # make sure that coffee_profile is not None
        if has_profile:
            profile_exists = self.coffee_profile is not None
            print(f"Profile is not None: {profile_exists}")
            return profile_exists
        return False # at this point, its false because the user does not have a profile
    except Exception as e: #extra layer of debugging
        print(f"Exception in has_coffee_profile: {e}")
        return False




# coolest part of this entire project was learning about monkey patching 
# this will run at runtime in order to make sure that the user model has the coffee_profile property
User.has_coffee_profile = property(has_coffee_profile)